#!/usr/bin/env python3
"""Tests for guard-github-writes.py. Run: python3 -I test_guard.py  (exit 1 on any failure)."""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "guard-github-writes.py")

DENY = [
    "git push origin fix-1",
    "cd repo && git -C . push",
    "git -c core.x=y --no-pager push --force-with-lease",
    "GIT_TRACE=1 git push",
    "echo ok; git push",
    "sudo -E git push",
    "timeout 60 git push origin HEAD",
    "nice -n 10 git push",
    "stdbuf -oL git push",
    "env -u GH_TOKEN -u GITHUB_TOKEN gh issue comment 1 -R scalameta/metals -b hi",
    "unset GH_TOKEN GITHUB_TOKEN; gh pr -R scalameta/metals comment 8874 -b hi",
    "gh pr --repo scalameta/metals comment 1 -b x",
    "gh issue -R scalameta/metals comment 1 -b x",
    'bash -c "git push origin HEAD"',
    "bash -lc 'git push origin HEAD'",
    "sh -ec 'git push'",
    "eval 'gh pr create --fill'",
    "echo `git push origin HEAD`",
    "x=$(git push origin HEAD)",
    "git -c alias.p=push p",
    "git subtree push --prefix=x origin main",
    "find . -name x -exec git push \\;",
    "printf 'git push\\n' | sh",
    "python3 -c \"import subprocess; subprocess.run(['git', 'push'])\"",
    "gh pr create --fill --draft",
    "gh pr comment 8874 --body x",
    "gh issue comment 123 -b hi",
    "gh repo fork scalameta/metals",
    "gh auth login --with-token",
    "gh api -X POST repos/scalameta/metals/issues/1/comments",
    "gh api -XPOST repos/scalameta/metals/issues/1/comments",
    "gh api repos/scalameta/metals/issues/1/comments -f body=hi",
    "gh api --method=PATCH repos/x/y/pulls/1",
    "gh api graphql -f query='mutation { addComment(input:{}) { clientMutationId } }'",
    "Q='mutation{addComment(input:{}){clientMutationId}}'; gh api graphql -f query=\"$Q\"",
    "gh api graphql -F query=@/tmp/m.graphql",
    'curl -X POST https://api.github.com/repos/x/y/issues -d "{}"',
    "curl -sXPOST https://api.github.com/repos/x/y/issues",
    "curl -s https://api.github.com/repos/x/y/issues -d '{}'",
    "curl -s -d@/tmp/body.json https://api.github.com/repos/scalameta/metals/issues/1/comments",
    "curl -s -d'{\"body\":\"hi\"}' https://api.github.com/repos/scalameta/metals/issues/1/comments",
    "curl -s -Fbody=hi https://api.github.com/repos/scalameta/metals/issues/1/comments",
    "http POST https://api.github.com/repos/x/y/issues title=x",
    "wget --post-data=x https://api.github.com/repos/x/y/issues",
    "G=git; $G push origin HEAD",
    "git $(echo push) origin HEAD",
    "echo push | xargs git",
    "gh alias set pc 'pr create' && gh pc --fill",
    'sbt --client "git push"',
    "hub pull-request -m x",
    "git config alias.pp push && git pp",
]
ALLOW = [
    "git log --oneline -5",
    "git -C repo fetch upstream",
    "git log --grep=push",
    "git status",
    "gh pr view 8874 --comments",
    "gh pr view 8874 --json comments",
    "gh pr list -R scalameta/metals --author jozanek",
    "gh api repos/scalameta/metals/pulls/8874/comments --paginate",
    "gh api -X GET search/issues -f q=repo:scalameta/metals",
    "gh api graphql -f query='query { viewer { login } }'",
    'echo "git push is forbidden"',
    'grep -rn "gh pr create" notes/',
    "curl -fsSL https://raw.githubusercontent.com/scalameta/.github/main/AGENTS.md",
    "curl -s https://api.github.com/repos/scalameta/metals/pulls/1",
    "sbt --client 'unit/testOnly tests.DiagnosticsLspSuite -- *reset*'",
    "python3 -I ~/oss/bin/lint-change.py --base upstream/main",
    "cat .git/config",
    "gh pr list -R scalameta/metals --search review --state open",
    "gh pr list -R scalameta/metals --search merge",
    "gh issue list -R scalameta/metals --search close",
    "gh api graphql -F owner=scalameta -F name=metals -f query='query($owner:String!,$name:String!){repository(owner:$owner,name:$name){pullRequest(number:8874){reviewThreads(first:50){nodes{isResolved}}}}}'",
    "gh api graphql --paginate -f query='query($endCursor: String) { viewer { repositories(first: 50, after: $endCursor) { nodes { name } } } }'",
    "git stash push -m wip",
    "~/oss/bin/metals-gates.sh --dry-run",
]
MCP_DENY = [
    "mcp__github__add_issue_comment", "mcp__github__create_pull_request", "mcp__github__pull_request_review_write",
    "mcp__github__push_files", "mcp__github__merge_pull_request", "mcp__github__issue_write",
    "mcp__claude_ai_GitHub__create_issue", "mcp__gh__update_pull_request", "mcp__plugin_gitlab_gitlab__create_merge_request",
    "mcp__github__actions_run_trigger", "mcp__github__request_copilot_review",
]
MCP_ALLOW = [
    "mcp__github__pull_request_read", "mcp__github__list_issues", "mcp__github__get_file_contents",
    "mcp__github__search_code", "mcp__github__issue_read", "mcp__metals__compile-file", "mcp__metals__format-file",
]


def run(payload, env):
    out = subprocess.run([sys.executable, "-I", HOOK], input=json.dumps(payload), capture_output=True, text=True, env=env)
    return "DENY" if out.stdout.strip() else "allow"


def main():
    root = tempfile.mkdtemp(prefix="oss-guard-")
    inside = os.path.join(root, "metals", "repo")
    os.makedirs(inside)
    env = dict(os.environ, OSS_GUARD_ROOT=root)
    with open(os.path.join(inside, "push.sh"), "w") as fh:
        fh.write("#!/bin/sh\nset -e\ngit add -A\ngit push origin HEAD\n")
    with open(os.path.join(inside, "fetch.sh"), "w") as fh:
        fh.write("#!/bin/sh\ngit fetch upstream\ngit log -1\n")
    failures = 0
    cases = [(c, "DENY", inside) for c in DENY] + [(c, "allow", inside) for c in ALLOW]
    outside = tempfile.mkdtemp(prefix="oss-guard-outside-")
    with open(os.path.join(outside, "push.sh"), "w") as fh:
        fh.write("git push origin HEAD\n")
    with open(os.path.join(inside, "p.py"), "w") as fh:
        fh.write("import subprocess\nsubprocess.run(['git', 'push', 'origin', 'HEAD'])\n")
    with open(os.path.join(inside, "ok.py"), "w") as fh:
        fh.write("print('hello')\n")
    cases += [("bash ./push.sh", "DENY", inside), ("./push.sh", "DENY", inside), ("sh push.sh", "DENY", inside),
              ("bash ./fetch.sh", "allow", inside), ("./fetch.sh", "allow", inside),
              (f"bash {outside}/push.sh", "DENY", inside), (f"sh -e {outside}/push.sh", "DENY", inside),
              ("source ./push.sh", "DENY", inside), (". ./push.sh", "DENY", inside),
              ("bash < ./push.sh", "DENY", inside), ("bash <<< 'git push origin HEAD'", "DENY", inside),
              ("bash <<'EOF'\ngit push origin HEAD\nEOF", "DENY", inside),
              ("python3 - <<'EOF'\nimport subprocess; subprocess.run(['git', 'push'])\nEOF", "DENY", inside),
              ("python3 -I ./p.py", "DENY", inside), ("python3 -I ./ok.py", "allow", inside),
              ("cat > ~/oss/metals/work/x/steps.md <<'EOF'\nThen run: git push origin fix-8468\nEOF", "allow", inside)]
    # Tools other than Bash that run a command (Monitor runs in the same shell environment)
    for tool, cmd, expected in (("Monitor", "git push origin HEAD", "DENY"), ("Monitor", "gh pr checks 8874 --watch", "allow"),
                                ("PowerShell", "git push origin HEAD", "DENY")):
        got = run({"tool_name": tool, "cwd": inside, "tool_input": {"command": cmd}}, env)
        ok = got == expected
        failures += not ok
        print(f"{'ok ' if ok else 'BAD'} {got:5} [{tool}] {cmd}")
    cases += [("git push origin main", "allow", tempfile.gettempdir()), (f"git -C {inside} push", "DENY", tempfile.gettempdir())]
    for cmd, expected, cwd in cases:
        got = run({"tool_name": "Bash", "cwd": cwd, "tool_input": {"command": cmd}}, env)
        ok = got == expected
        failures += not ok
        print(f"{'ok ' if ok else 'BAD'} {got:5} {cmd}")
    for name in MCP_DENY + MCP_ALLOW:
        expected = "DENY" if name in MCP_DENY else "allow"
        got = run({"tool_name": name, "cwd": inside, "tool_input": {}}, env)
        ok = got == expected
        failures += not ok
        print(f"{'ok ' if ok else 'BAD'} {got:5} {name}")
    got = run({"tool_name": "Read", "cwd": inside, "tool_input": {"file_path": "/x"}}, env)
    failures += got != "allow"
    print(f"{'ok ' if got == 'allow' else 'BAD'} {got:5} Read tool")
    total = len(cases) + len(MCP_DENY) + len(MCP_ALLOW) + 1
    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
