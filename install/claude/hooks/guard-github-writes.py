#!/usr/bin/env python3
"""Claude Code PreToolUse hook: block pushes and GitHub writes in open-source work.

Install: ~/.claude/hooks/guard-github-writes.py, registered for the matchers
"Bash|Monitor|PowerShell" and "mcp__.*" (see install/claude/user-settings.hook-snippet.json).
Tests: test_guard.py next to this file (python3 -I test_guard.py).

Layer 2 of 4 (02-operating-model.md, section 7). This is a best-effort tripwire, not a
boundary: no parser can list every way a shell can run code. Layer 1 (no write credentials
in the environment) is what holds when this parser misses something.

How it decides (only when the session's cwd, or a path in the command, is under
OSS_GUARD_ROOT, default ~/oss):
- Any tool with a `command` input (Bash, Monitor, PowerShell): every word of every simple
  command is checked, so wrappers (timeout, nice, env -u X, sudo, xargs, find -exec) do not
  hide `git` or `gh`. Shell -c flag clusters (-c, -lc, -ec), eval, interpreter -c/-e code,
  `...` and $(...), here-strings, heredocs fed to a shell or an interpreter, and small text
  scripts run by a shell, `source`, `.` or an interpreter (anywhere on disk) are checked
  too. git aliases are resolved with `git config`. Text piped into a shell is denied,
  because the command cannot be seen.
- MCP: write-shaped tools (create/update/delete/merge/push/comment/...) on servers whose
  name looks like GitHub or GitLab are denied, whatever the server is called.
"""
import json
import os
import re
import shlex
import subprocess
import sys

ROOT = os.path.realpath(os.path.expanduser(os.environ.get("OSS_GUARD_ROOT", "~/oss")))
SHELLS = {"bash", "sh", "zsh", "dash", "ksh", "fish", "ash"}
INTERPRETERS = {"python", "python3", "node", "perl", "ruby", "php", "deno", "bun", "osascript", "scala-cli", "amm"}
STRING_RUNNERS = {"su", "script", "flock", "watch", "ssh", "runuser", "nohup", "setsid"}
HTTP_CLIENTS = {"curl", "wget", "http", "https", "xh", "httpie"}
GIT_OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--super-prefix", "--config-env", "--exec-path"}
GIT_WRITE = {"push", "send-pack", "http-push", "send-email", "request-pull"}
GIT_BUILTINS = set(
    "add am annotate apply archive bisect blame branch bundle cat-file check-ignore checkout cherry cherry-pick clean "
    "clone commit config count-objects describe diff diff-tree difftool fetch for-each-ref format-patch fsck gc grep "
    "help init log ls-files ls-remote ls-tree merge merge-base mergetool mv name-rev notes pull range-diff rebase reflog "
    "remote repack replace reset restore rev-list rev-parse revert rm shortlog show show-ref sparse-checkout stash "
    "status submodule switch symbolic-ref tag update-index update-ref var verify-commit version whatchanged worktree "
    "maintenance".split()
)
GH_WRITE = {
    "pr": {"create", "comment", "review", "merge", "close", "edit", "reopen", "ready", "lock", "unlock", "update-branch"},
    "issue": {"create", "comment", "close", "edit", "reopen", "delete", "transfer", "lock", "unlock", "pin", "unpin", "develop"},
    "release": {"create", "edit", "delete", "upload", "delete-asset"},
    "repo": {"create", "delete", "edit", "fork", "rename", "archive", "unarchive", "sync", "deploy-key", "set-default"},
    "gist": {"create", "edit", "delete"},
    "label": {"create", "edit", "delete", "clone"},
    "workflow": {"run", "enable", "disable"},
    "run": {"rerun", "cancel", "delete"},
    "secret": {"set", "delete"},
    "variable": {"set", "delete"},
    "cache": {"delete"},
    "project": {"create", "edit", "delete", "item-add", "item-edit", "item-delete", "close", "copy", "field-create", "field-delete", "link", "unlink", "mark-template"},
    "discussion": {"create", "comment", "edit", "close", "delete"},
    "auth": {"login", "refresh", "setup-git", "token"},
    "alias": {"set", "import"},  # an alias can hide a write action
}
HUB_WRITE = {"push", "pull-request", "fork", "create", "release", "issue", "api", "delete", "sync"}
MCP_WRITE_VERBS = {
    "create", "update", "delete", "merge", "push", "add", "fork", "submit", "write", "comment", "assign", "label",
    "close", "reopen", "request", "dismiss", "resolve", "unresolve", "enable", "disable", "trigger", "run", "rerun",
    "cancel", "edit", "set", "remove", "lock", "unlock", "star", "unstar", "transfer", "approve", "mark", "pin",
    "unpin", "rename", "archive", "unarchive", "sync", "dispatch", "upload", "post", "reply", "react",
}
CONTROL = {"&&", "||", ";", "|", "&", "|&", ";;", "(", ")"}
GH_HOSTS = re.compile(r"(api|uploads)\.github\.com|github\.com/[^\s'\"]+/(pulls|issues|git/refs)")


def substitutions(command):
    """Contents of `...` and $(...) (one level; nested ones are found recursively)."""
    out = re.findall(r"`([^`]*)`", command)
    depth, start = 0, None
    for i, ch in enumerate(command):
        if command.startswith("$(", i) and not command.startswith("$((", i):
            if depth == 0:
                start = i + 2
            depth += 1
        elif ch == ")" and depth > 0:
            depth -= 1
            if depth == 0 and start is not None:
                out.append(command[start:i])
    return out


HEREDOC = re.compile(r"<<-?[ \t]*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")


def split_heredocs(command):
    """Remove heredoc bodies; return (rest, [(kind, body)]) with kind "shell", "interp" or "data"."""
    lines, out, bodies, i = command.split("\n"), [], [], 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        for _, delim in HEREDOC.findall(line):
            body = []
            while i < len(lines) and lines[i].strip() != delim:
                body.append(lines[i])
                i += 1
            i += 1
            words = line.split()
            first = os.path.basename(words[0]) if words else ""
            if first in SHELLS or first in ("eval", "source", ".") or re.search(r"\|\s*(\S*/)?(ba|z|da|k|fi)?sh\b", line):
                kind = "shell"
            elif first in INTERPRETERS:
                kind = "interp"
            else:
                kind = "data"
            bodies.append((kind, "\n".join(body)))
    return "\n".join(out), bodies


INTERP_WRITE = re.compile(r"\bgit\b['\"\],\s]+push\b|\bgh\b['\"\],\s]+(pr|issue)['\"\],\s]+(create|comment|review|merge|close|edit)\b")


def interp_reason(prog, code):
    if INTERP_WRITE.search(code):
        return f"{prog} code that pushes or writes to GitHub"
    if re.search(r"(api|uploads)\.github\.com", code) and re.search(r"\b(POST|PUT|PATCH|DELETE)\b", code):
        return f"{prog} code that writes to the GitHub API"
    return None


def simple_commands(command):
    lexer = shlex.shlex(command.replace("\n", " ; "), posix=True, punctuation_chars=";&|()")
    lexer.whitespace_split = True
    lexer.commenters = ""
    current = []
    try:
        for tok in lexer:
            if tok in CONTROL or (tok and set(tok) <= set(";&|()")):
                if current:
                    yield current
                current = []
            else:
                current.append(tok)
    except ValueError:  # unbalanced quotes: let the raw backstop decide
        yield None
        return
    if current:
        yield current


def raw_backstop(command):
    if re.search(r"\|\s*(sudo\s+)?(env\s+\S+\s+)*(/\S*/)?(ba|z|da|k|fi)?sh\b(\s+-\S+)*\s*($|[;&|)])", command):
        return "text piped into a shell (the command cannot be checked)"
    if re.search(r"\bgraphql\b", command) and re.search(r"\bmutation\b", command):
        return "GraphQL mutation"
    if re.search(r"alias\.[\w.-]+=\s*['\"]?!?[^;&|]*\bpush\b", command) or re.search(
            r"\bgit\b[^;&|\n]*\bconfig\b[^;&|\n]*\balias\.[\w.-]+[^;&|\n]*\bpush\b", command):
        return "git alias that pushes"
    return None


def git_alias(name, cwd):
    if name in GIT_BUILTINS:
        return None
    try:
        r = subprocess.run(["git", "config", "--get", f"alias.{name}"], cwd=cwd if cwd and os.path.isdir(cwd) else None,
                           capture_output=True, text=True, timeout=3)
    except Exception:
        return None
    return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else None


def git_reason(args, cwd, depth):
    inline_aliases = {}
    i = 0
    while i < len(args):
        a = args[i]
        if a == "-c" and i + 1 < len(args):
            m = re.match(r"alias\.([^=]+)=(.*)", args[i + 1])
            if m:
                inline_aliases[m.group(1)] = m.group(2)
            i += 2
            continue
        if a in GIT_OPTS_WITH_VALUE:
            i += 2
            continue
        if a.startswith("-"):
            i += 1
            continue
        rest = args[i + 1:]
        if a.startswith("$") or a in ("(", "`"):
            return "git subcommand hidden in a variable or substitution"
        if a in GIT_WRITE:
            return f"git {a}"
        if a == "subtree" and "push" in rest:
            return "git subtree push"
        expansion = inline_aliases.get(a) or git_alias(a, cwd)
        if expansion:
            if re.search(r"\b(push|send-pack|http-push|send-email)\b", expansion):
                return f"git alias '{a}' runs '{expansion}'"
            if expansion.startswith("!"):
                return analyze(expansion[1:], cwd, depth + 1)
        return None
    return None


def gh_api_reason(args):
    method, fields, text = None, [], " ".join(args)
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("-X", "--method") and i + 1 < len(args):
            method = args[i + 1].upper()
            i += 2
            continue
        m = re.match(r"^(?:-X|--method=)(\w+)$", a)
        if m:
            method = m.group(1).upper()
        if a in ("-f", "-F", "--field", "--raw-field") and i + 1 < len(args):
            fields.append(args[i + 1])
            i += 2
            continue
        m = re.match(r"^(?:-f|-F)(.+)$|^--(?:field|raw-field)=(.+)$", a)
        if m:
            fields.append(m.group(1) or m.group(2))
        if a == "--input" or a.startswith("--input="):
            fields.append("@input")
        i += 1
    if "graphql" in args:
        queries = [f.split("=", 1)[1] for f in fields if f.startswith("query=")]
        inline = [q for q in queries if re.match(r"^\s*(query\b|\{)", q)]  # may use $variables
        if not queries or len(inline) != len(queries) or "@input" in fields:
            return "gh api graphql with a query that is not inline (cannot check it is not a mutation)"
        return "gh api graphql mutation" if any(re.search(r"\bmutation\b", q) for q in queries) or "mutation" in text else None
    if method and method != "GET":
        return f"gh api -X {method}"
    if fields and method != "GET":
        return "gh api with fields (defaults to POST)"
    return None


def gh_reason(args):
    idx = next((i for i, a in enumerate(args) if not a.startswith("-")), None)
    if idx is None:
        return None
    group, rest = args[idx], args[idx + 1:]
    if group.startswith("$"):
        return "gh command hidden in a variable"
    if group == "api":
        return gh_api_reason(rest)
    i = 0
    while i < len(rest):  # the action is the first non-flag word; -R/--repo may come before it
        a = rest[i]
        if a in ("-R", "--repo", "--hostname"):
            i += 2
            continue
        if a.startswith("-"):
            i += 1
            continue
        if a.startswith("$"):
            return f"gh {group} action hidden in a variable"
        return f"gh {group} {a}" if a in GH_WRITE.get(group, set()) else None
    return None


def http_reason(prog, args):
    text = " ".join(args)
    if not GH_HOSTS.search(text):
        return None
    if prog in ("http", "https", "xh", "httpie"):
        if any(a.upper() in ("POST", "PUT", "PATCH", "DELETE") for a in args) or any(re.match(r"^[\w.-]+(:?=|:=@|=@)", a) for a in args):
            return f"{prog} write to GitHub"
        return None
    if re.search(r"(^|\s)-[a-zA-Z]*X\s*['\"]?(POST|PUT|PATCH|DELETE)\b", text, re.I) or re.search(r"--request[=\s]+['\"]?(POST|PUT|PATCH|DELETE)\b", text, re.I):
        return f"{prog} write to GitHub"
    for a in args:
        m = re.match(r"^-([A-Za-z]+)", a)
        if m and not a.startswith("--") and set(m.group(1)) & {"d", "F", "T"}:  # -d@body.json, -sd, -Fx=y
            return f"{prog} write to GitHub"
        if re.match(r"^--(data\S*|json|form\S*|upload-file|post-data|post-file)(=|$)", a) or re.match(r"^--method=(POST|PUT|PATCH|DELETE)", a, re.I):
            return f"{prog} write to GitHub"
    return None


def script_text(path, cwd):
    """Contents of a small text file (anywhere on disk), or None. Larger files and binaries are not read."""
    p = os.path.realpath(os.path.join(cwd or "", os.path.expanduser(path)))
    if not os.path.isfile(p) or os.path.getsize(p) > 64 * 1024:
        return None
    try:
        with open(p, "rb") as fh:
            data = fh.read()
    except OSError:
        return None
    return None if b"\0" in data else data.decode("utf-8", "replace")


def indirect_reason(words):
    """A command name or subcommand that the parser cannot see."""
    if words and words[0].startswith("$") and any(w == "push" or w in GH_WRITE["pr"] | GH_WRITE["issue"] for w in words[1:]):
        return "command name hidden in a variable"
    for i, w in enumerate(words):
        base = os.path.basename(w)
        if base == "xargs":
            tail = [x for x in words[i + 1:] if not x.startswith("-")]
            if tail and os.path.basename(tail[0]) in ("git", "gh", "hub") and len(tail) <= 1:
                return f"{os.path.basename(tail[0])} subcommand supplied by xargs input"
        if base == "sbt" and any(re.match(r"^\s*git\s+push\b", x) for x in words[i + 1:]):
            return "sbt git push (sbt-git)"
        if base == "hub" and any(x in HUB_WRITE for x in words[i + 1:]):
            return "hub write"
    return None


def analyze_words(words, cwd, depth):
    r = indirect_reason(words)
    if r:
        return r
    if words and "/" in words[0]:  # ./push.sh or ~/oss/bin/x run directly
        text = script_text(words[0], cwd)
        r = analyze(text, cwd, depth + 1) if text else None
        if r:
            return f"{r} (inside {words[0]})"
    for i, w in enumerate(words):
        prog = os.path.basename(w)
        rest = words[i + 1:]
        if prog in SHELLS:
            for j, a in enumerate(rest):
                if a in ("<", "<<<") and j + 1 < len(rest) or (a.startswith("<") and len(a) > 1):
                    if a == "<<<" or a.startswith("<<<"):  # bash <<< 'git push'
                        text = rest[j + 1] if a == "<<<" else a[3:]
                    else:  # bash < push.sh
                        text = script_text(rest[j + 1] if a == "<" else a[1:], cwd)
                    r = analyze(text, cwd, depth + 1) if text else None
                    if r:
                        return r
                    continue
                if not a.startswith("-"):
                    text = script_text(a, cwd)  # bash ./push.sh
                    r = analyze(text, cwd, depth + 1) if text else None
                    if r:
                        return f"{r} (inside {a})"
                    break
                if not a.startswith("--") and "c" in a[1:] and j + 1 < len(rest):
                    r = analyze(rest[j + 1], cwd, depth + 1)
                    if r:
                        return r
                    break
        elif prog in ("source", ".") and rest:
            text = script_text(rest[0], cwd)
            r = analyze(text, cwd, depth + 1) if text else None
            if r:
                return f"{r} (inside {rest[0]})"
        elif prog == "eval":
            r = analyze(" ".join(rest), cwd, depth + 1)
            if r:
                return r
        elif prog in INTERPRETERS:
            for j, a in enumerate(rest):
                if a in ("-c", "-e", "--eval", "-p", "--print", "-E") and j + 1 < len(rest):
                    r = interp_reason(prog, rest[j + 1])
                    if r:
                        return r
                    break
                if a in ("-m", "-W", "-X"):
                    break
                if not a.startswith("-"):  # python3 x.py
                    text = script_text(a, cwd)
                    r = interp_reason(prog, text) if text else None
                    if r:
                        return f"{r} (inside {a})"
                    break
        elif prog in STRING_RUNNERS:
            for a in rest:
                if " " in a:
                    r = analyze(a, cwd, depth + 1)
                    if r:
                        return r
        elif prog == "git":
            r = git_reason(rest, cwd, depth)
            if r:
                return r
        elif prog == "gh":
            r = gh_reason(rest)
            if r:
                return r
        elif prog in HTTP_CLIENTS:
            r = http_reason(prog, rest)
            if r:
                return r
    return None


def analyze(command, cwd=None, depth=0):
    if depth > 4:
        return "command nested too deeply to check"
    command, bodies = split_heredocs(command)
    for kind, body in bodies:
        r = analyze(body, cwd, depth + 1) if kind == "shell" else interp_reason("heredoc", body) if kind == "interp" else None
        if r:
            return r
    for inner in substitutions(command):
        r = analyze(inner, cwd, depth + 1)
        if r:
            return r
    r = raw_backstop(command)
    if r:
        return r
    for words in simple_commands(command):
        if words is None:
            if re.search(r"\bgit\b.*\bpush\b|\bgh\b.*\b(pr|issue)\b.*\b(create|comment|review|merge|close|edit)\b", command):
                return "unparsable command that mentions a push or a GitHub write"
            continue
        r = analyze_words(words, cwd, depth)
        if r:
            return r
    return None


def mcp_reason(tool_name):
    parts = tool_name.split("__")
    if len(parts) < 3:
        return None
    server, tool = parts[1].lower(), "__".join(parts[2:]).lower()
    if not re.search(r"git(hub|lab)|(^|[_-])gh([_-]|$)", server):
        return None
    tokens = re.split(r"[_\-]+", tool)
    if tokens and tokens[0] in ("get", "list", "search", "read") or "read" in tokens:
        return None
    hit = next((t for t in tokens if t in MCP_WRITE_VERBS), None)
    return f"MCP tool {tool_name} ({hit})" if hit else None


def in_scope(cwd, text):
    candidates = [cwd or ""] + re.findall(r"(?:~|/)[^\s'\";|&()`]*", text or "")
    for p in candidates:
        p = os.path.realpath(os.path.expanduser(p)) if p else ""
        if p == ROOT or p.startswith(ROOT + os.sep):
            return True
    return False


def decide(data):
    tool = data.get("tool_name") or ""
    cwd = data.get("cwd")
    tool_input = data.get("tool_input") or {}
    if tool.startswith("mcp__"):
        return mcp_reason(tool) if in_scope(cwd, json.dumps(tool_input)) else None
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if isinstance(command, str):  # Bash, Monitor, PowerShell, and any future tool that runs a command
        return analyze(command, cwd) if in_scope(cwd, command) else None
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    reason = decide(data)
    if reason:
        json.dump({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Blocked ({reason}). In open-source work the agent never pushes or writes to GitHub. "
                                        f"Write the draft under ~/oss/<project>/work/<id>/ and tell the human the exact command to run.",
        }}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
