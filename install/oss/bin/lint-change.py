#!/usr/bin/env python3
"""Mechanical pre-submit checks for a scalameta/metals change. Costs no model tokens.

Checks the commits in BASE..HEAD, the added lines of the diff, and optionally a
PR body draft, against rules from the scalameta org CONTRIBUTING.md/AGENTS.md,
the Metals AGENTS.md and the build (project/TestGroups.scala).

Usage:
  lint-change.py [--repo PATH] [--base upstream/main] [--head HEAD] [--pr-body FILE]

Exit code 1 if any ERROR, else 0. The report starts with the counts.
Every check prints the rule id it enforces; the ids are listed in the
"Mechanical" table of checklist.md.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

AGENT_WORDS = r"(claude|anthropic|copilot|codex|openai|chatgpt|gpt-|gemini|cursor|devin|aider|codeium|windsurf|opencode)"
ATTRIBUTION = re.compile(
    rf"^\s*(co-authored-by:.*{AGENT_WORDS}|.*generated (with|by) .*{AGENT_WORDS})",
    re.IGNORECASE,
)
CONVENTIONAL = re.compile(
    r"^(fix|bugfix|improvement|feat|feature|docs|test|tests|chore|refactor|perf|build|ci|revert|style)(\([^)]+\))?!?: \S"
)
RISKY_PATHS = (
    ".github/",
    "build.sbt",
    "project/",
    "bin/",
    "mtags-interfaces/",
    "mtags-shared/",
    "sbt-metals/",
)
NOISE = re.compile(
    r"\b(all tests pass|tests pass|ran scalafmt|formatted with|run scalafmt|cross-build ran|\d+ tests?)\b",
    re.IGNORECASE,
)


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, rule, where, msg):
        self.items.append((level, rule, where, msg))

    def emit(self):
        counts = {lvl: sum(1 for i in self.items if i[0] == lvl) for lvl in ("ERROR", "WARN", "INFO")}
        print(f"lint-change: {counts['ERROR']} error(s), {counts['WARN']} warning(s), {counts['INFO']} info")
        if not self.items:
            print("Nothing to fix.")
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        shown = {}
        for level, rule, where, msg in sorted(self.items, key=lambda i: order[i[0]]):
            shown[rule] = shown.get(rule, 0) + 1
            if level == "INFO" and shown[rule] > 3:
                continue
            print(f"{level:5} {rule:9} {where}: {msg}")
        for rule, n in shown.items():
            if n > 3 and any(i[0] == "INFO" and i[1] == rule for i in self.items):
                print(f"INFO  {rule:9} (+{n - 3} more not shown)")
        return 1 if counts["ERROR"] else 0


def check_commits(repo, base, head, rep):
    raw = git(repo, "log", "--format=%H%x1f%s%x1f%b%x1e", f"{base}..{head}")
    commits = [c.strip("\n") for c in raw.split("\x1e") if c.strip()]
    if not commits:
        rep.add("WARN", "C0", f"{base}..{head}", "no commits in range")
    # Wrong base: main and main-v2 have diverged by more than 1000 commits. In
    # 2026, regulars opened PRs with 857-1822 stray commits/files, and
    # CodeRabbit refuses PRs over 150-300 files.
    files = len(git(repo, "diff", "--name-only", f"{base}...{head}").splitlines())
    if len(commits) > 15 or files > 60:
        level = "ERROR" if files > 150 or len(commits) > 100 else "WARN"
        rep.add(level, "P-BASE", f"{base}..{head}",
                f"{len(commits)} commits, {files} files: wrong base branch (main vs main-v2) or a PR that should be split")
    for c in commits:
        sha, subject, body = (c.split("\x1f") + ["", ""])[:3]
        where = f"commit {sha[:9]}"
        if re.match(r"^(fixup|squash|amend)!", subject):
            rep.add("ERROR", "P-FIXUP", where, f"'{subject}': a pushed branch has no fixup!/squash! commits (org CONTRIBUTING.md)")
        if not CONVENTIONAL.match(subject):
            rep.add("WARN", "P-CONV", where, f"subject is not conventional-commit style: '{subject}'")
        if len(subject) > 50:
            rep.add("WARN", "P-SUBJ", where, f"subject is {len(subject)} chars; org AGENTS.md says at most 50 (it binds agent-written commits)")
        attributions = [l for l in body.splitlines() if ATTRIBUTION.match(l)]
        if len(attributions) > 1:
            rep.add("ERROR", "P-ATTR", where, f"{len(attributions)} agent attributions; at most one is allowed (org CONTRIBUTING.md)")
        for line in body.splitlines():
            if len(line) > 72 and not re.search(r"https?://|/|`", line) and not ATTRIBUTION.match(line):
                rep.add("WARN", "P-WRAP", where, f"body line over 72 chars: '{line[:60]}...'")
                break
        if NOISE.search(body):
            rep.add("INFO", "P-NOISE", where, "body mentions routine noise (test counts, formatting); org AGENTS.md says omit it")


def added_lines(repo, base, head):
    """Yield (path, line_no, text) for every added line in base...head."""
    diff = git(repo, "diff", "--unified=0", "--no-color", f"{base}...{head}")
    path, line_no = None, 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            line_no = int(m.group(1)) if m else 0
        elif line.startswith("+") and path:
            yield path, line_no, line[1:]
            line_no += 1


def check_diff(repo, base, head, rep):
    changed = git(repo, "diff", "--name-status", f"{base}...{head}").splitlines()

    def at_head(p):
        r = subprocess.run(["git", "-C", repo, "show", f"{head}:{p}"], capture_output=True, text=True, errors="replace")
        return r.stdout if r.returncode == 0 else ""

    groups_text = at_head("project/TestGroups.scala")
    for entry in changed:
        parts = entry.split("\t")
        status, path = parts[0], parts[-1]
        if path.startswith(RISKY_PATHS) and path != "project/TestGroups.scala":
            rep.add("WARN", "R-RISKY", path, "risky path (L0 area): needs a maintainer's OK before the PR")
        if status.startswith("A") and re.match(r"tests/unit/src/test/scala/.*Suite\.scala$", path):
            src = at_head(path)
            pkg = re.search(r"^package\s+([\w.]+)", src, re.MULTILINE)
            for cls in re.findall(r"^\s*(?:(?:final|abstract|sealed|private|protected|case)\s+)*class\s+(\w+Suite)\b", src, re.MULTILINE):
                fqcn = f"{pkg.group(1)}.{cls}" if pkg else cls
                if f'"{fqcn}"' not in groups_text:
                    rep.add("ERROR", "T-SHARD", path, f"new suite {fqcn} is not in project/TestGroups.scala")

    prev = {}
    for path, n, text in added_lines(repo, base, head):
        where = f"{path}:{n}"
        if path.endswith(".scala"):
            code = re.sub(r'"(\\.|[^"\\])*"', '""', text)
            if re.search(r"\breturn\b", code) and not code.lstrip().startswith(("//", "*", "/*")):
                rep.add("WARN", "S-RETURN", where, "added 'return': AGENTS.md says never use non-local returns")
            if "pprint.log" in code and "/src/main/" in path:
                rep.add("ERROR", "S-DEBUG", where, "pprint.log left in production code")
            if re.search(r"\bprintln\(", code) and "/src/main/" in path:
                rep.add("WARN", "S-PRINT", where, "println in production code; Metals logs with scribe")
            if re.search(r"\.iterator\b", code):
                rep.add("INFO", "S-ITER", where, "added .iterator: AGENTS.md says only when really necessary")
            if re.search(r"\.toList\b", code):
                rep.add("INFO", "S-TOLIST", where, "added .toList: AGENTS.md says only when necessary")
            if re.search(r"\b(TODO|FIXME|XXX)\b", text):
                rep.add("WARN", "S-TODO", where, "added TODO/FIXME: say it in the PR instead, or fix it")
            m = re.search(r'\btest\(\s*"([^"]+)"', text)
            if m and path.startswith("tests/") and " " in m.group(1):
                rep.add("WARN", "T-NAME", where, f"test name '{m.group(1)}' has spaces; AGENTS.md asks for kebab-case")
            # Once per block. Metals code itself has many multi-line // comments, but the
            # org rule binds agent-written commits (deviation noted in open-questions.md).
            is_line_comment = code.lstrip().startswith("//")
            run = prev.get(path, (-10, 0))
            if is_line_comment and run[0] == n - 1:
                run = (n, run[1] + 1)
                if run[1] == 2:
                    rep.add("WARN", "S-COMMENT", f"{path}:{n - 1}", "multi-line // comment: org AGENTS.md wants a /* ... */ block comment")
            else:
                run = (n, 1) if is_line_comment else (-10, 0)
            prev[path] = run


def check_pr_body(path, rep):
    text = Path(path).read_text()
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"^(```|~~~).*?^\1[^\n]*$", "", text, flags=re.DOTALL | re.MULTILINE)  # fenced code is not prose
    def is_prose(line):
        return (
            line.strip()
            and not re.match(r"^\s*([-*+]|\d+\.|#|\||```|>)", line)
            and not ATTRIBUTION.match(line)
            and not re.match(r"^\s*(fixes|closes|resolves|part of|refs)\b", line, re.IGNORECASE)
        )

    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    for p in paragraphs:
        prose = [l for l in p.splitlines() if is_prose(l)]
        if len(prose) > 1:
            rep.add("ERROR", "P-1LINE", path, f"hard-wrapped paragraph starting '{prose[0][:50]}...'; write one line per paragraph")
    attributions = [l for l in text.splitlines() if ATTRIBUTION.match(l)]
    if len(attributions) > 1:
        rep.add("ERROR", "P-ATTR", path, f"{len(attributions)} agent attributions in the PR body; at most one")
    elif attributions:
        rep.add("WARN", "P-ATTR", path, "agent attribution in the PR body; the commit trailer already carries one")
    for line in filter(is_prose, text.splitlines()):
        for sentence in re.split(r"(?<=[.!?])\s+", line.strip()):
            words = re.findall(r"[A-Za-z0-9'`#./:_-]+", sentence)
            if len(words) > 20:
                rep.add("WARN", "P-PLAIN", path, f"{len(words)}-word sentence: '{sentence[:60]}...'")
            if re.search(r"\b(is|are|was|were|been|being)\s+\w+ed\b", sentence):
                rep.add("INFO", "P-ACTIVE", path, f"possible passive voice: '{sentence[:60]}...'")
    for needed, label in ((r"\bNow\b", "a 'Now, ...' sentence"), (r"Tests?:", "a 'Tests:' line"), (r"Risk", "a 'Risk and undo' line")):
        if not re.search(needed, text):
            rep.add("WARN", "P-TMPL", path, f"missing {label} (templates/pr-description.md)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--base", default="upstream/main")
    ap.add_argument("--head", default="HEAD")
    ap.add_argument("--pr-body")
    a = ap.parse_args()
    rep = Report()
    check_commits(a.repo, a.base, a.head, rep)
    if any(i[0] == "ERROR" and i[1] == "P-BASE" for i in rep.items):
        rep.items = [i for i in rep.items if i[1] == "P-BASE"]
        sys.exit(rep.emit())
    check_diff(a.repo, a.base, a.head, rep)
    if a.pr_body:
        check_pr_body(a.pr_body, rep)
    sys.exit(rep.emit())


if __name__ == "__main__":
    main()
