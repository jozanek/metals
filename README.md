# Operating model for contributing to scalameta/metals (jozanek)

Built 2026-10-18 in a Claude Code cloud session. Sources: the repository, the scalameta org policy, and public review data (your 21 PRs, plus 62 PRs and 252 issues by others). Nothing was posted, and nothing was added to a Metals branch. On 2026-10-20, at your request, this folder was pushed to `oss-operating-model`, an orphan branch of your fork. Keep your copy outside any Metals clone (Install, step 1).

## Read in this order
0. `HANDOFF.md`: the current state, the decisions made, and the next steps.
1. `01-step0-report.md`, section 1: the ten facts that shape everything else (5 minutes).
2. `02-operating-model.md`, sections 1 and 4: the flow map and the autonomy levels. The rest is reference.
3. `03-work-shortlist.md`: what to do next, with the checks done so far.
4. `install/oss/metals/CLAUDE.md`: what your agents will follow. If you disagree with a line, change it before you install.

Each document ends with "Check your understanding" questions. Answer them before you install. The point is that you hold the model, not the files.

## What is in the folder
```
HANDOFF.md                  current state, decisions, next steps, how to resume
01-step0-report.md          how the project works, what reviewers care about, responsiveness, AI rules
02-operating-model.md       flow map, stage specs, escalation, autonomy, notes, budget, safety, rollout, metrics, open questions
03-work-shortlist.md        work sources and a ranked shortlist (still-valid, claimed, blast radius, needs-decision checks)
install/oss/                becomes ~/oss
  bin/claude-oss            starts Claude Code with a read-only token and no git or SSH credentials; --selftest checks that
  bin/metals-gates.sh       path-aware local gates that mirror the CI jobs; lists test gates for Metals MCP (tested in dry-run)
  bin/lint-change.py        policy and convention checks, no model tokens (tested on your #8874 and #8529)
  bin/mine-reviews.sh       exact review data with your gh (GET only); feeds the checklist
  bin/test-selection.py     which suites a change can break (edited suites and transitive subclasses)
  metals/CLAUDE.md          standing instructions (loads because the clone lives in metals/repo)
  metals/checklist.md       project checklist mined from reviews (v0)
  metals/autonomy.md        your starting level per area, with evidence
  metals/ledger.csv         metrics, seeded with your 21 PRs as the baseline
  metals/notes/             reviewers, mistakes-as-rules, conventions, decisions, map, glossary, questions, learning log
  metals/templates/         PR description, escalation message, cloud-session preamble, work-item brief
  metals/work/              briefs for your three open PRs (pr8793 first, then pr8658, pr8824), with drafts to post
  metals/.gitignore         for when you make ~/oss/metals a git repo with an origin (excludes repo/ and data/raw/)
install/claude/             becomes parts of ~/.claude
  agents/oss-reviewer.md    fresh-context reviewer (Opus, read-only, round cap 3)
  agents/oss-explainer.md   commit-pinned explainers and explain-back grading (Opus)
  agents/oss-scout.md       bulk triage and digests (Sonnet, read-only)
  hooks/guard-github-writes.py   blocks pushes and GitHub writes under ~/oss, for Bash and MCP tools
  hooks/test_guard.py       its tests (112 cases, including bypass attempts and must-allow commands)
  user-settings.hook-snippet.json  merge into ~/.claude/settings.json
  repo-settings.local.json  copy to ~/oss/metals/repo/.claude/settings.local.json
data/                       the mined review and issue data behind the report (public sources)
```

## Install (rollout step R0, one evening)
```bash
# 1. Workspace, outside any repository (--single-branch skips the Metals history)
git clone --single-branch -b oss-operating-model https://github.com/jozanek/metals ~/Downloads/oss-operating-model
#    or, from the archive: tar -xzf oss-operating-model.tar.gz -C ~/Downloads
mkdir -p ~/oss && cp -R ~/Downloads/oss-operating-model/install/oss/. ~/oss/ && chmod +x ~/oss/bin/*
echo 'export PATH="$HOME/oss/bin:$PATH"' >> ~/.bashrc        # or ~/.zshrc; then open a new shell

# 2. The Metals clone lives INSIDE the workspace (move your clone there, or clone again)
git clone https://github.com/jozanek/metals ~/oss/metals/repo   # or: mv <your clone> ~/oss/metals/repo
cd ~/oss/metals/repo
git remote add upstream https://github.com/scalameta/metals && git fetch upstream
printf 'CLAUDE.md\nCLAUDE.local.md\n.claude/\n.mcp.json\n' >> .git/info/exclude

# 3. A read-only token for agents. On GitHub: Settings > Developer settings >
#    Fine-grained tokens > Repository access: "Public repositories (read-only)", no other permissions.
mkdir -p ~/.config/oss && chmod 700 ~/.config/oss
cat > ~/.config/oss/gh-readonly.token     # paste the token, then Ctrl-D
chmod 600 ~/.config/oss/gh-readonly.token

# 4. User-level agents and the guard hook (outside any repository)
mkdir -p ~/.claude/agents ~/.claude/hooks
cp ~/Downloads/oss-operating-model/install/claude/agents/*.md ~/.claude/agents/
cp ~/Downloads/oss-operating-model/install/claude/hooks/*.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.py
#    Merge install/claude/user-settings.hook-snippet.json into ~/.claude/settings.json by hand (keep your keys).

# 5. Project-local settings: deny rules and one-trailer attribution. Git never sees .claude/.
mkdir -p ~/oss/metals/repo/.claude
cp ~/Downloads/oss-operating-model/install/claude/repo-settings.local.json ~/oss/metals/repo/.claude/settings.local.json

# 6. Metals MCP for Claude Code, at local scope (stored in ~/.claude.json, not in the repo).
#    Use the port Metals prints: "Metals MCP server started on port: N".
cd ~/oss/metals/repo && claude mcp add --transport http metals http://localhost:N/mcp
```

### Verify (each check has an expected result; continue only when all pass)
| # | Do | Expect |
|---|----|--------|
| V1 | `git -C ~/oss/metals/repo status --short` | empty |
| V2 | `claude-oss metals --selftest`, from the terminal you will start sessions in (IDE terminals export askpass variables; the selftest checks they are cleared). Answer `y` to the one no-op write probe. | every line PASS (SKIP only for ssh if it is not installed), then "layer 1 OK". If the write probe did not run, it says NOT VERIFIED: do not continue. It checks: gh uses only the read-only token; no stored gh login to fall back to; the token cannot write to your fork; git cannot authenticate a push; no credential helper or askpass answers; ssh has no usable identity. |
| V3 | `python3 -I ~/.claude/hooks/test_guard.py` | "112/112 passed" |
| V4 | `claude-oss metals`, then `/memory` | `~/oss/metals/CLAUDE.md` is listed. If not: `echo '@~/oss/metals/CLAUDE.md' > ~/oss/metals/repo/CLAUDE.local.md` and approve the import prompt. |
| V5 | In that session: "run `git push --dry-run origin HEAD`" | denied by the hook, with the reason "Blocked (git push)" |
| V6 | In the session: `/mcp` | `metals` connected, with `compile-file`, `test`, `inspect`; no GitHub or GitLab server active for this project (or only read tools, which the hook allows) |
| V7 | In the session: "run `~/oss/bin/metals-gates.sh --dry-run`" | "No changes against upstream/main." and the plan of gates |

## Optional hardening (a hard boundary instead of layers)
Layer 1 removes credentials from the agent's environment, but a process that runs as you can still read `~/.ssh` and other files. Two ways to close that:
- The Claude Code sandbox (`/sandbox`; built in on macOS and Linux). Use its filesystem restrictions (see the Claude Code sandboxing docs) to deny reads of `~/.ssh` and your gh config, then check that a sandboxed `cat` of your SSH key fails. Keep `sandbox.allowUnsandboxedCommands` false, and allow only the network hosts sbt needs (Maven Central, Sonatype). It isolates Bash only, so layers 2-4 still matter. Try it during R0; if sbt or Metals MCP breaks, keep it off.
- A cloud session with no write-capable repository attached, for anything untrusted (templates/cloud-preamble.md).

## Daily use
```
claude-oss metals
> Session start per CLAUDE.md, then start work item <id>: <shortlist number and title>.
```
At the end of each item: one ledger row, notes updated, and you posted whatever needed posting from your own terminal.

## Where this disagrees with the article, and why
See `02-operating-model.md`, section 8. In short: you are on the "everyone else" path, so you spend your own time to save one maintainer's. Learning is a formal loop, not an on-demand explainer, because the understanding has to end up with you. Review runs locally with one strong reviewer and deterministic checks, not a voting panel, because of the budget.
