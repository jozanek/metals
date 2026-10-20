# Handoff: contributor operating model for scalameta/metals (jozanek)

Updated 2026-10-20. This branch (`oss-operating-model` in jozanek/metals) is an orphan branch: it shares no history with Metals. Never base PR work on it, and never merge it into a Metals branch.

## What exists
| Path | What it is |
|------|------------|
| `README.md` | entry point: reading order, install (R0), verification V1-V7, optional hardening |
| `01-step0-report.md` | how the project works, what reviewers care about, responsiveness, the AI policy |
| `02-operating-model.md` | flow map, stage specs S0-S9, escalation ladder, autonomy rules, notes system, budget, safety layers, rollout, metrics, assumptions and open questions |
| `03-work-shortlist.md` | work sources and the ranked shortlist |
| `install/oss/` | becomes `~/oss`: `bin/` scripts, `metals/` workspace (`CLAUDE.md`, checklist, autonomy map, ledger, notes, templates, `work/` briefs) |
| `install/claude/` | becomes parts of `~/.claude`: three subagents, the guard hook and its tests, settings snippets |
| `data/` | the public review and issue data behind the report (mined 2026-10-18) |

## Decisions made (by jozanek)
- 2026-10-18: Claude Max, no local models; 15+ hours a week; goals: understanding, reputation, maintainer path. Can explain the debug/run and scaladoc/files/rename work, not the completions or BSP work (explanation debt).
- 2026-10-20: keep all three open PRs and finish them (#8793, #8658, #8824). Cloud sessions start without the fork attached. The notes folder becomes a git repo with an origin later (the workspace is git-ready). Weekly split agreed: 6 h new work, 4 h learning, 3 h triage and shadow reviews, 2 h feedback and notes.
- 2026-10-20: jozanek asked the agent to push this branch. That is a one-off exception to "never push", limited to this branch. The rule still holds for everything else, including Metals branches and PRs.
- Still open: whether to use the Claude Code sandbox for local sbt runs (U4), and whether to move toward `main-v2` later (U5).

## State as of 2026-10-20
- Upstream `main` @ c631ca0f, `main-v2` @ 541ae6ec, `scalameta/.github` @ 632e5cc. All seven hashes in `install/oss/metals/notes/policy-hashes.txt` still match these heads.
- #8793: open, merges cleanly into `main`, no human review in 68 days. One CodeRabbit correctness note is unanswered (parameterized enum case owner). Next: the test in `work/pr8793/brief.md`, then one ping.
- #8658: open 104 days, 27 files (+6,649/-174), conflicts with `main` in `project/TestGroups.scala`. tgodzik's two direction comments from 2026-07-08 are unanswered. Next: one reply with a split proposal (`work/pr8658/brief.md`); split after #8793 merges.
- #8824: open 49 days, no human activity, conflicts with `main` in `McpTestRunner.scala` (#8785, #8791). Next: the closed question in `work/pr8824/brief.md`, before any rebase.
- Nothing is installed on jozanek's machine yet.

## Next steps, in order
1. jozanek: install and verify (README, R0). Sessions start only after `claude-oss metals --selftest` says "layer 1 OK" (with the write probe run) and `test_guard.py` shows 112/112.
2. R1: run `~/oss/bin/mine-reviews.sh`, then accept or reject each proposed checklist v1 rule. Then run `oss-reviewer` on the pre-correction diffs of #8745, #8504 and #8542. `notes/mistakes.md` says how.
3. R2, item A: the three PR briefs, in order: pr8793, pr8658, pr8824. Items B and C follow (`02-operating-model.md`, section 9).
4. R3: after the third R2 item, review the metrics in the same section. Loosen or tighten one rule at a time.

A reminder for step 1 fires in the original cloud session on 2026-10-22 at 21:08 UTC. It is a scheduled task (`trig_01557rN6hKBBSGopvv4xcBRM`); delete it if you no longer need it.

## What a future session must know
- The hard rules in `install/oss/metals/CLAUDE.md` still hold. The agent never pushes, posts, comments or opens PRs; this branch is the one exception. It adds no files to the Metals working tree.
- The review data is v0. Public pages hid many inline comments (for example the six on #8874). R1 replaces it with exact `gh` data.
- The guard hook is a best-effort tripwire. Layer 1 (no write credentials in the agent's environment) is the boundary. Verified: 112 hook tests, 143 probe cases from two fresh-context review rounds, the launcher on stubs. Not yet run on jozanek's machine.
- Never run the selftest's write probe in a cloud session: the session's proxy holds credentials for the fork. On 2026-10-18 this session sent two no-op PATCH requests to jozanek/metals while testing; GitHub refused both, and nothing changed.
- Cloud sessions have no Metals MCP and no sbt by default. To run tests there, add a setup script that installs a JDK, coursier and sbt. Allow Maven Central and Sonatype in the network settings.
- The fork is public, so this branch is public. `install/oss/metals/notes/reviewers.md` describes a maintainer's review habits from public comments. To unpublish: `git push origin --delete oss-operating-model` (copies may stay cached).

## How to resume
- On your machine: `git clone --single-branch -b oss-operating-model https://github.com/jozanek/metals ~/Downloads/oss-operating-model`, then follow `README.md`. `--single-branch` skips the Metals history.
- In a new cloud session: the same clone, into `~/oss-operating-model`. The fork is public, so the session usually does not need it attached. Then read this file and `README.md`, and give the session `install/oss/metals/templates/cloud-preamble.md` as its first rules.

## Check your understanding
1. Why is this branch an orphan, and why must no PR or merge ever start from it?
2. Which safety layer is the real boundary? What does the write probe prove that the other selftest checks cannot?
3. For #8824, which answer do you need before you rebase, and why ask before you write code?
