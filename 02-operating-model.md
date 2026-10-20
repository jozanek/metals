# Operating model: contributing to scalameta/metals from the outside

Status: v1, 2026-10-18, upstream `main` @ 8c095fe5, `main-v2` @ d6eb032e. Built from the Step 0 report (`01-step0-report.md`) and your interview answers.

Your situation in one paragraph: you have 16 merged PRs since June (plus a 2018 typo fix), 3 open and 2 closed. On `main`, nearly all of them pass through one maintainer (tgodzik). You spend 15+ hours a week, you write Scala at work but tooling internals are new, and you want understanding, reputation and a maintainer path. You have no local models any more, a Claude Max plan, an authenticated `gh`, and Metals MCP running on the Metals repo. So the constraint is not your time. It is one maintainer's attention, your Claude Max limits, and your own understanding of the BSP and completion code you have already changed.

---

## 1. Flow map

```
S0 Select ─► S1 Confirm ─► S2 Explore + explain-back ─► S3 Decision needed? ─┬─► S4 Build under gates ─► S5 Fresh review ─► S6 Submit ─► S7 Feedback ─► S8 Notes ─► S9 Watch
                                                                              └─► ask ONE closed question on the issue, wait (no code yet)
```

| Stage | Automated (no model) | Agent-assisted | Me (decide) | Maintainer |
|-------|----------------------|----------------|-------------|------------|
| S0 Select | `gh` queries, WIP count | `oss-scout` triage table: valid? claimed? area? risk? | pick one item; respect WIP limit | none |
| S1 Confirm need | test run via Metals MCP; `git log -S`, blame | reproducer as a failing test; history of the code path on `main` and `main-v2` | is it real, in this repo, worth my time? | none |
| S2 Explore | MCP `inspect`, `get-usages` | `oss-explainer` writes or reuses a commit-pinned explainer, then grades my explain-back | write predictions first; explain back in my words | none |
| S3 Decision? | ladder searches (code, history, docs, PRs) | classify against the "real decision" rubric; draft one closed question | proceed, ask, or drop | answers one closed question, only if asked |
| S4 Build | `metals-gates.sh`, `lint-change.py`, MCP compile/test; cloud for heavy jobs | implements in the proof shape: prep, tests, fix | read the diff and the evidence, not every step | none |
| S5 Review | `lint-change.py` | `oss-reviewer` (fresh context, round cap 3, diff-only after round 1) | answer every finding; explain every line or cut it | none |
| S6 Submit | `lint-change.py --pr-body` | draft title and body from the template | rewrite in my words, push from my shell, open the PR | reviews when they choose |
| S7 Feedback | fetch comments and CI with `gh` | classify each comment (fix, disagree with evidence, question); draft one batched reply | decide each reply; post it | reviews again |
| S8 Notes | ledger row | propose note diffs; re-run reviewer on the pre-correction diff (eval) | write map/glossary in my words; update autonomy | none |
| S9 Watch (30 days) | `gh search issues` for the feature | digest new reports | fix fast if it was mine | merges, releases |

**Where people stay in the loop, and why there.** The Claude Code team keeps humans on five decisions machines are bad at: should we build this, risky code, architecture, reading the evidence, and owning the outcome. From the contributor's side they split like this:

- **The maintainer** owns "should this be done", direction, pattern-setting architecture, and risky areas (`mtags-interfaces`, `mtags-shared`, the BSP lifecycle, build and CI files). You ask about these once, early, and on the issue. The article notes that even a team that "solved" its review bottleneck kept human review for changes from outside the team, "so someone asks 'should we even do this?'". That outside author is you. Answer that question before they have to ask it.
- **You** own choosing the work, deciding whether a maintainer decision is needed, reading the evidence, explaining every line, and the outcome after merge. One test applies: if you cannot say what the checks would miss, you are not ready to submit.
- **Machines** do the rest: search, reproduction, gates, first review, drafting.

### Check your understanding (answer before reading on)
1. Your #8745 was closed and #8874 replaced it. At which stage above would a closed question have saved a round, and what would the question have been?
2. Why is S2 before S3, and not after S4?

---

## 2. Per-stage spec

Each stage lists what is automated, what the agent hands you, what you decide, the exit gate, failure modes, and what the checks miss. "Opus", "Sonnet" and "none" give the cost tier (section 6).

### S0 Select (detail in `03-work-shortlist.md`)
- **Automated:** `gh issue list` / `gh pr list` queries; count of my open PRs awaiting review.
- **Agent hands me (Sonnet, `oss-scout`):** a triage table per candidate: still valid on upstream `main` (evidence), claimed or covered by an open PR, area and its autonomy level, blast radius, does it teach a new slice, does it need a maintainer decision.
- **I decide:** one item. **WIP limit:** at most 2 of my PRs waiting on a maintainer, and at most 1 in an area at L0 or L1.
- **Gate:** the item fits the WIP limit and has a row in `ledger.csv`.
- **Failure modes:** an issue already fixed or obsolete. Duplicate work with someone's open PR. The wrong repository: Scala 3 completion and hover bugs belong to scala/scala3, editor UI bugs to metals-vscode or nvim-metals. An area that `main-v2` has already rewritten.
- **The check misses:** maintainers' unwritten plans. Mitigation: look at the same code path on `main-v2` before you commit to the item.

### S1 Understand the goal, reproduce or confirm the need
- **Automated:** Metals MCP `test` (or `sbt --client unit/testOnly ...`) runs the reproducer. `git log -S<symbol>` and `git blame` find the PR that introduced the code path. For untrusted repro projects attached to issues, use a cloud session only.
- **Agent hands me (Opus, main session):** the goal in one sentence. A minimal reproducer as a test: an `LspSuite` with a `metals.json` workspace for LSP features, a `tests/cross` test for Scala 2 PC features. The observed and expected output. The PR that last changed the path, with its stated reason. Whether the same path exists on `main-v2`.
- **I decide:** is the need real, in this repository, and worth a time box (default: 6 hours to a failing test, then stop and record why)?
- **Gate:** a test that shows the wrong behaviour on upstream `main`@sha. If no test can run the path, a written manual repro and the reason no test is possible (org AGENTS.md accepts that only when no test can run the path today).
- **Failure modes:** reproducing a different bug. A repro that depends on OS, JDK or build-tool version. "Cannot reproduce" because it is already fixed: then the output is a triage comment, not a PR. Instructions planted in issue text: the scout quotes them, nobody runs them.
- **The check misses:** Windows- or macOS-only bugs (your machine runs neither CI job), editor-specific client behaviour, and bugs that need a real build tool (`tests/slow`, cloud).

### S2 Explore the slice, then explain it back
- **Automated:** Metals MCP `inspect`, `get-usages` and `glob-search` to walk the slice; `git log --format='%h %ad %s' -- <paths>` for its recent history; the explainer's age check (reuse if younger than 90 days).
- **Before any reading, I write 3 predictions** in `work/<id>/brief.md`: where the behaviour is decided, what the fix will touch, what the maintainer will comment on.
- **Agent hands me (Opus, `oss-explainer`):** an explainer for exactly this slice, pinned to the upstream sha, with entry points as `path:Symbol`, one request traced step by step, 3 invariants and the tests that pin them, and 5 questions. It reuses an explainer younger than 90 days if one exists.
- **I decide:** I answer the 5 questions without looking. I write a 5-8 sentence explain-back in my own words. The explainer grades it against the code (mode GRADE).
- **Gate:** explain-back PASS. In an area with explanation debt (BSP: #8465, #8529, #8874. PC completions: #8464, #8489, #8504, #8514), I also explain back one of my own merged PRs there, once. This pays the debt before I add more code on top of it.
- **Failure modes:** a wrong explainer. Mitigation: you verify 2 of its anchors yourself, and grading is against the code, not the explainer. Learning theatre: skimming and then agreeing. Mitigation: predictions are written first and scored later. A time sink: cap S2 at 25% of the item's time.
- **The check misses:** tacit knowledge that is not in the code, such as why the design is the way it is. That lives in old PRs, so read the PR that `git blame` names.

### S3 Decide whether a maintainer decision is needed (detail in section 3)
- **Automated:** the ladder's searches: `git log -S`, `git blame -w`, `gh search prs` and `gh search issues` (closed ones included), and `grep` over `docs/` and `website/blog/`.
- **Agent hands me (Opus):** a classification against the rubric in section 3, the ladder results (what I checked, with links), and a draft question from `templates/escalation.md` if one is needed.
- **I decide:** proceed, ask, or drop. My autonomy level for the area sets the default (section 4).
- **Maintainer:** answers one closed question, only if I asked one.
- **Gate:** either "no decision needed" with the reason in the brief, or an answer. For a reversible choice at L1 or higher, the message may say what I will do if nobody answers within 7 days.
- **Failure modes:** asking for information I could find, which costs attention and trust. Not asking about a real decision, which means a closed PR. Raising direction on a finished PR, which is a surprise. Asking several questions at once.
- **The check misses:** preferences nobody wrote down. These appear in review; `reviewers.md` keeps them.

### S4 Do the work under local gates
- **Shape (org AGENTS.md, "A bug fix as a proof"):** preparation commits with no behaviour change, then one commit with every test the fix touches, asserting today's behaviour (green, including the wrong output), then the fix commit that flips those assertions. Sibling inputs are pinned too ("Find the cause and the cases like it"). Branch from upstream at the current sha, one concern per PR.
- **Automated:** the edit loop uses Metals MCP `compile-file`, `compile-module`, `test` and `format-file` (Metals AGENTS.md). Before each commit: format the changed files and run `sbt --client scalafixAll` (Metals AGENTS.md). Before handover, run `metals-gates.sh` once. It runs the checks MCP does not offer (scalafmt on changed files, `lint-change.py`, `scalafixCheck`, and, when the paths need them, docs and MiMa). It selects the suites the change can break (edited suites, and every concrete subclass of an edited test base class, transitively). Up to 5 unit suites are listed for MCP `test`, which runs one class per call; more suites, and module-wide runs (`cross/test`, `javapc/test`), run with sbt, which Metals AGENTS.md allows for what MCP cannot do. It lists the heavy jobs (`+cross/test`, slow suites, `sbt-metals/scripted`) for a cloud session.
- **Agent hands me:** the diff, the gate table with timings, and red-to-green evidence: the new assertions fail on the pre-fix code and pass after.
- **I decide:** I read the diff and the evidence, not every intermediate step.
- **Gate:** all gates PASS. Heavy jobs are either PASS in a cloud run or named as "not run" in the PR body.
- **Failure modes:** the agent edits a test to make it pass. A fix that adds a branch for the reported input while the siblings share one path, which the org rules call the wrong place. A new test that is flaky because of timing. Scope creep and reformatted lines you did not change.
- **The check misses:** Windows and macOS runners, JDK 17 vs 25 differences, the other unit shards, and performance. For indexing or toplevel changes, consider a `metals-bench` run.

### S5 Fresh-context self-review
- **Automated:** `lint-change.py` (policy and convention rules) before the reviewer runs, so the reviewer spends nothing on what a script can catch; `git diff <last-reviewed-sha>..HEAD` scopes rounds 2-3.
- **Agent hands me (Opus, `oss-reviewer`):** findings that start with a count, are tagged Important, Nit or Pre-existing, cite `path:line`, name the class of bug, and include at most 3 nits. Round 1 reviews the full diff. Rounds 2-3 review only the new diff. There are no repeats, and round 4 is refused with "step back and reconsider the approach". Optional second opinion: the built-in `/code-review`.
- **I decide:** every finding gets an answer in the brief (fixed / dismissed with reason). Then I walk the diff hunk by hunk: I can explain it, or I learn it now, or I cut it. This is your principle 7, and the org rule "you must be able to explain it".
- **Gate:** 0 open Important findings, at most 3 rounds, I can explain every line, `lint-change.py` reports 0 errors.
- **Failure modes:** reviewer noise that an agent dutifully "fixes", which means another round. The article's finding applies: noise costs more when the author is an agent. Author and reviewer share a model's blind spots. Mitigation: the checklist rules come from human maintainers. Dismissing a real finding.
- **The check misses:** the maintainer's taste and direction, and project conventions that are not yet in the checklist.

### S6 Submit
- **Automated:** `lint-change.py --pr-body ~/oss/metals/work/<id>/pr.md` (one line per paragraph, sentence length, attribution count, template lines); `gh pr checks <n>` after you push.
- **Agent hands me:** a title in the style of recent Metals titles and a body from `templates/pr-description.md`, checked with `lint-change.py --pr-body`.
- **I decide:** I rewrite the body in my words. I push from my own terminal with my own credentials (the agent cannot). I check the base branch, the issue link, and that there is exactly one agent attribution (commit trailer only).
- **Gate:** PR-body lint shows 0 errors, the WIP limit holds, and the base branch is confirmed.
- **Failure modes:** a wrong base (`main` vs `main-v2`). A body that narrates the diff. Overclaimed testing. A missing issue link.
- **The check misses:** CI on Windows and macOS. Watch the first CI run and fix it the same day.

### S7 Handle feedback
- **Automated:** `gh pr view <n> --comments`, `gh pr checks <n>`, or `mine-reviews.sh` for one PR.
- **Agent hands me (Sonnet for sorting, Opus for evidence):** every comment, CodeRabbit's included, classified as fix, disagree-with-evidence, or question. A drafted code change per fix. Evidence for each disagreement (code, test, history; never taste). One batched set of replies.
- **I decide:** each classification and reply. Answer every comment and submit the answers as one review (org CONTRIBUTING.md). Push new commits, not amended ones (Metals AGENTS.md, until Q-COMMITS is settled). Re-request review once.
- **Then, for every maintainer correction:** add a rule to `notes/mistakes.md` and `checklist.md`, and run an eval: re-run `oss-reviewer` on the pre-correction diff. If it still misses the problem, sharpen the rule until it catches it.
- **Gate:** every thread answered, CI green.
- **Failure modes:** arguing about taste. Replies in agent voice. Fixing more than was asked. Several pushes per round, each one a notification.
- **The check misses:** silent dissatisfaction, which shows up only as slow reviews. Track days to review. Ping at most once, after 14 days.

### S8 Update notes
- **Automated:** the ledger row from `mine-reviews.sh` for the PR (rounds, comments, days); a stale-anchor check: `git grep -n <Symbol>` for each `path:Symbol` in the area's notes.
- **Agent hands me:** proposed one-line diffs for `decisions.md`, `conventions.md` and `reviewers.md`. A ledger row. Stale entries in this area.
- **I decide:** I write `map.md` and `glossary.md` entries in my own words. I score the predictions in `learning-log.md`. I apply promotion or demotion rules (section 4).
- **Gate:** ledger row complete; every correction has a rule.
- **Failure modes:** notes rot; notes filled with agent text; skipping S8 when busy (it then never happens).
- **The check misses:** what you did not notice you misunderstood. The predictions are the only probe for that.

### S9 Watch after merge (30 days)
- **Automated:** a weekly `gh search issues --repo scalameta/metals "<feature words>" --created ">=<merge date>"`, and the CI status of `main` for the suites you touched.
- **Agent hands me (Sonnet, `oss-scout`):** new reports that mention the feature, with the version they use, and whether they predate your release.
- **I decide:** is a report caused by my change? If yes, I fix it before any new work ("you land it, you own it"), and I add the class of bug to the checklist.
- **Gate:** none to pass; the item closes 30 days after the release that contains it.
- **Failure modes:** a regression reported in words that the search misses; a report on `main-v2` after the maintainers port the change.
- **The check misses:** users who hit the regression and never report it. Metals has no telemetry you can see.

---

## 3. Escalation ladder (before you spend a maintainer's attention)

Climb in order. Stop when you have the answer. Record each rung in the brief, because the question you finally ask says what you checked.

1. **Code search.** Metals MCP `glob-search`, `inspect`, `get-usages`; `git grep`. Who calls this, and what do the siblings do?
2. **Blame and history.** `git log -S'<symbol>' --format='%h %ad %s'`, `git blame -w`. The `(#NNNN)` in the subject names the PR, and its discussion often holds the reason.
3. **Docs.** `architecture.md`, `docs/contributors/`, the release notes in `website/blog/` (they list every merged PR), `metals-lsp.org` for Metals 2.
4. **Past PRs and issues.** `gh search prs --repo scalameta/metals "<term>"`, `gh search issues ...`, including closed ones. Closed-unmerged PRs show what was rejected and why.
5. **Similar changes.** How did someone solve the analogous problem for another build tool, another Scala version, or the other branch?
6. **A fresh-context agent.** Give an Opus subagent the two options and ask it to argue for each from the code. If one side has no evidence, you have your answer.
7. **Only then ask the maintainer: once, early, on the issue, before code.** Use a closed question, options with your recommendation, what you checked, and (only for reversible choices at L1+) what you will do if nobody answers.

**A real decision** is one whose answer depends on maintainer intent that is written nowhere:
- scope: should Metals do this at all, or is it a feature request (those go to metals-feature-requests);
- user-visible behaviour: a new default, a new setting or its name, a changed message;
- architecture or placement when two places both fit the existing code;
- branch strategy for a bug present on both `main` and `main-v2` (Q-BRANCH);
- compatibility: dropping support, binary API (`mtags-interfaces`), anything copied to scala/scala3 (`mtags-shared`);
- any change in an L0 area or a risky path (`.github/`, `build.sbt`, `project/` except `TestGroups.scala`, `bin/`, `sbt-metals/`).

**Information you can find yourself:** how the code works, which tests cover it, conventions, test commands, why something was done (history), whether a bug is fixed, which branch has the code, and what a maintainer said last time about the same kind of change (`reviewers.md`).

**Anti-patterns:** asking in a finished PR, asking several questions at once, follow-up pings within 14 days, asking an open question ("what do you think?").

---

## 4. Autonomy levels per area

Levels describe how far you go before a maintainer sees the work. The initial map with evidence is in `install/oss/metals/autonomy.md`.

| Level | You do | Maintainer sees |
|-------|--------|-----------------|
| L0 ask first | Investigate, reproduce, then stop. Post one closed question. | The question, before any code. |
| L1 propose | Post the question with your recommendation and a default, or open a small PR that says "proposal" in its first line. | A recommendation they can accept with one word. |
| L2 decide, explain | Decide, then state the decision and the rejected alternative in "Look first at". | A PR whose decision is visible and reviewable. |
| L3 decide, defend | Decide, and defend the choice in review with evidence. | A PR and, if challenged, evidence. |

**Promotion (one level, per area):** in the last 90 days, at least 3 merged PRs in the area, each with at most 1 maintainer change round. No repeated correction (the same checklist rule broken twice). An explain-back PASS for each. No regression within 30 days. Predictions for the area at 2/3 or better on the last 3 items. Merge count alone never promotes. You have merged presentation-compiler and BSP PRs that you cannot yet explain, which is exactly why.

**Demotion (one level, at once):** a regression traced to your change. A "should not have been done" or "wrong place" comment. A repeated correction. A failed explain-back. A major redesign of the area (for example `main-v2` replacing it) resets it to L1.

**Always L0, whatever the evidence:** `mtags-interfaces`, `mtags-shared`, `.github/`, `build.sbt`, `project/` (except registering a suite in `TestGroups.scala`), `bin/`, `sbt-metals/`, release files, and anything on `main-v2` until you have one merged PR there.

**Agent autonomy toward you (a separate axis):** the agent may read, search, run local tests, and edit inside a git worktree without asking. It must ask you before deleting anything, before touching risky paths, and before spending an Opus review round. It never pushes, posts, comments or opens PRs (section 7).

---

## 5. Knowledge system

Folder: `~/oss/metals/` (outside the repo; the clone lives inside it as `repo/`). Rules are in `install/oss/metals/notes/README.md`. In short:
- **Read at the start** of every item: autonomy, mistakes, reviewers, the map rows for the area, the latest explainer, open questions.
- **Update at the end:** map and glossary in your words; one-line dated entries in decisions, conventions and reviewers; every correction as a rule; predictions scored; one ledger row.
- **Link to code** as `path:Symbol`, with `(verified YYYY-MM-DD @ sha)`. Use permalinks for PRs and commits.
- **Prune:** 90 days without re-verification makes an entry stale. An anchor that no longer resolves makes it stale at once. Rules unused for 6 months move to an archive section.
- **Learning check:** predict first (S2), explain back (S2), graded against code, and scored in `learning-log.md`. Your prediction hit rate per area is part of the promotion evidence. It is the one metric that measures your understanding rather than your output.

Why this differs from the article: the Claude Code team has "no formal process" for learning and asks for explainers on demand. That works for people who already own the code. Your goal is the reverse: to become someone the maintainers trust with judgement. An explainer you only read leaves the understanding with the agent. A prediction you get wrong, then correct, moves it to you.

---

## 6. Model and budget plan (Claude Max, no local models)

| Tier | What runs there | Examples |
|------|-----------------|----------|
| none | Deterministic tools | `metals-gates.sh`, `lint-change.py`, `mine-reviews.sh`, `git`, `gh` GET, Metals MCP calls |
| Sonnet | Bulk reading and sorting (`oss-scout`) | issue triage, review-data digests, log digests, CI failure summaries, comment classification |
| Opus | Depth: work where a mistake costs a maintainer round | root cause in an unfamiliar area, the explainer for a new slice, `oss-reviewer`, evidence for a disagreement, the one escalation question |

Budget rules:
- One work item, one fresh main session. `CLAUDE.md` and the notes give it context cheaply, and old context is not dragged along.
- Keep bulk reading in subagents, so the main context holds conclusions, not file dumps.
- Prefer Metals MCP (`inspect`, `get-usages`, `glob-search`) over reading whole files.
- Reuse explainers younger than 90 days. Per PR: one full Opus review and at most 2 diff-only re-reviews.
- Record the budget per item: the number of sessions, and your Max usage before and after (from the usage view), in the ledger `notes` column. After 5 items you will know what an item costs and can plan the week.
- If a local model server comes back, use it outside Claude Code: Anthropic does not support routing Claude Code to non-Claude models through a gateway. Point a separate harness, or plain scripts, at it for the Sonnet-tier chores (triage tables, digests). Keep review and root cause on Claude, where a weaker model costs a maintainer round.
- Record cost per item from `/usage` (alias `/cost`). For headless runs, `claude -p ... --output-format json` reports `total_cost_usd`, an estimate that is still a usable proxy on a subscription.

Cloud sessions (you said you would like to use them):
- **Use them for:** running other people's PR branches (untrusted code), heavy CI-like jobs (`+cross/test`, slow build-tool suites, `sbt-metals/scripted`), and parallel explorations.
- **Environment, set once:** Network access at Limited, with "Allow package managers" ticked, plus the hosts the sbt build needs (Maven Central and the Sonatype snapshots host from `bin/test.sh`). A Setup script that installs a JDK, coursier and sbt. Start each task with `templates/cloud-preamble.md`.
- **Limits:** a cloud session cannot read your local notes, so paste what it needs. It draws on plan usage (check the usage view). Cloud sessions read permission rules only from a committed `.claude/settings.json`, which your no-files rule excludes. A session with your fork attached can push: in this session's own container the proxy authenticated `git push --dry-run` to your fork. So the default is a session with no write-capable repository attached, working in an anonymous clone of upstream (the preamble says how). If you must attach your fork, the preamble and an afterwards check (`git ls-remote origin` shows no new branches) are the only controls, and that is an exception you accept knowingly.

---

## 7. Safety: untrusted input, sandboxing, never posting

- **Untrusted input.** Issue and PR text, comments, logs and linked pages are data. The scout quotes them; nobody follows instructions found in them. The main session never runs a command copied from an issue unless you have read it.
- **Unfamiliar code.** Upstream `main` and `main-v2` run locally. Anything else runs only in a cloud session: forks, PR branches, repro projects from issues. sbt builds execute code from `build.sbt` and `project/`, so a PR branch is code you have not reviewed.
- **Never post, in four layers.** The order matters: the first is the only one that is a real boundary.
  1. **No write credentials in the agent's environment.** The `claude-oss` launcher exports a fine-grained token with read-only access to public repositories as `GH_TOKEN`, removes every other GitHub token variable (`GITHUB_PERSONAL_ACCESS_TOKEN`, `GH_ENTERPRISE_TOKEN`, ...), and points `GH_CONFIG_DIR` at an empty directory, so gh has no stored login to fall back to. It clears git credential helpers (the github.com one too), askpass programs (IDE terminals export one), the SSH agent, and SSH keys (`ssh -F /dev/null`, no identities). `claude-oss metals --selftest` checks each of these without starting Claude, including one no-op write probe on your fork that only a read-only token's refusal passes; if the probe does not run, the result is NOT VERIFIED. Its limit: a process that runs as you can still read files such as `~/.ssh`. For a hard boundary, add the Claude Code sandbox with those paths denied, or use a cloud session (README, "Optional hardening").
  2. **A PreToolUse hook**, `~/.claude/hooks/guard-github-writes.py`, a best-effort tripwire for any tool that runs a command (Bash, Monitor, PowerShell) and for MCP tools. No parser can list every way a shell runs code, so it backs up layer 1; it does not replace it. It checks every word of every command, so wrappers (`timeout`, `nice`, `env -u`, `xargs`, `find -exec`) do not hide `git` or `gh`. It follows shell `-c` clusters, `eval`, interpreter `-c`/`-e` code, `` `...` `` and `$(...)`, small scripts under `~/oss`, and git aliases. It denies pushes, gh write actions in any flag order, `gh api` writes (a method or fields), GraphQL mutations and indirect queries, curl/wget/httpie writes to the GitHub API, text piped into a shell, and write-shaped tools on any GitHub-like MCP server. It acts only under `~/oss`. `test_guard.py` ships with it: 112 cases pass. So do the 143 probe cases written by two fresh-context review rounds: 91 bypass attempts, all denied, and 52 legitimate commands, all allowed.
  3. **Deny rules** in `repo/.claude/settings.local.json`: `git push`, the `gh` write commands, and the GitHub MCP server's tools (`mcp__github`). `gh api` is set to "ask". The Claude Code docs warn that these rules match text and "are not a security boundary": `git -C . push` passes them, but not layers 1 and 2. A GitHub MCP server or connector under another name is caught only by layer 2; README check V6 confirms that none is active for this project.
  4. **The standing instruction** in `CLAUDE.md`, hard rule 1, which also forbids `/code-review --comment` (it posts to GitHub) and `--fix`.
- **Headless runs.** `claude -p` runs a checkout's hooks and `.mcp.json` servers without a trust prompt. Never run it in an untrusted checkout. Where you must, add `--setting-sources user`.
- **`/security-review` caveat.** It compares your branch with origin's default branch. Your fork's `main` is 191 commits behind upstream, so it would review the wrong diff. Sync the fork first (from your terminal: `git push origin upstream/main:main`), or skip it.
- **No files in the repo.** The clone lives inside the workspace, so `~/oss/metals/CLAUDE.md` loads as a parent-directory memory file. Check it with `/memory` during install; if it is missing, the fallback is a one-line `repo/CLAUDE.local.md` that imports `@~/oss/metals/CLAUDE.md`. Metals' `.gitignore` ignores `CLAUDE.md`, `.vscode/` and `.cursor/`, but not `CLAUDE.local.md`, `.claude/` or `.mcp.json`. Metals writes `.mcp.json` into the workspace when it configures Claude Code. So `.git/info/exclude` lists all four. `git status` must stay clean apart from your change.

---

## 8. Adapted from the article, not transplanted

| The article's practice | Your version | Why it differs |
|------------------------|--------------|----------------|
| Minimise human review time; trusted authors get lighter paths | Minimise maintainer time per merged PR. You are on the "everyone else" path, so you spend your own time instead. | You are an outsider; maintainer time is not yours to spend. |
| AI review on every PR, in the team's infrastructure | Local fresh-context review before push. CodeRabbit already reviews every Metals PR, so pre-empt what it would flag. | The project's CI and bots are outside your control. |
| Several agents vote on each finding | One Opus reviewer, plus deterministic checks; findings must cite `path:line`; you adjudicate | Token budget. Voting multiplies cost; evidence requirements cut noise more cheaply. |
| Incidents become an eval set | Maintainer corrections become evals: re-run the reviewer on the pre-correction diff | Your "incidents" are review comments that cost a maintainer a round. |
| Measure noise by what people do with comments | Log every finding's fate (fixed, wrong, intentional, did not matter), CodeRabbit's on your PRs included | The same loop, at the size of one contributor. |
| The change sets the risk tier, not the author | The risky-path list and your per-area level decide whether you ask first | You cannot change their approval rules, but you can match your caution to the risk. |
| Merge queue, flags, staged release, rollback | Small single-concern PRs, "Risk and undo" in every body, a 30-day watch after merge | A revert is the maintainer's cost, so make it a one-click one. |
| Round cap 3, diff-only re-review, class of bug, no repeats | The same, built into `oss-reviewer` | It converges for the same reasons. |
| Raise a different direction early, in the thread | Stronger: before any code for anything non-trivial | A closed PR from an outsider costs the maintainer a decision and a conversation. |
| No formal learning process | Predict, explain back, graded; explanation debt per area | Your second goal is understanding, and agents must not do it for you. |

---

## 9. Rollout and metrics

### Rollout

**R0 Setup (one evening).** Follow `README.md`, "Install". It ends with a verification list: each check has an expected result, and you proceed only when all pass.

**R1 Exact data (week 1, no maintainer contact).**
1. Run `~/oss/bin/mine-reviews.sh`. It fetches your PRs plus 50 merged and 20 closed-unmerged PRs by others, with every inline comment.
2. Give `data/comments.jsonl` to `oss-scout` (Sonnet), with `checklist.md`. Ask it for changed or new rules, each with PR links. You accept or reject each one. This turns checklist v0 into v1.
3. Measure the reviewer before you trust it. Run `oss-reviewer` on the pre-correction diffs of #8745, #8504 and #8542 (`notes/mistakes.md` says how). Record which known problems it catches. This is your eval set. It grows with every new correction, like the article's incident set.

**R2 The first three items: strict gates, measure only (weeks 1-3).**
- Item A: shortlist #1, finishing your three open PRs (you chose to keep them). It starts with S3 and the escalation template: one message per PR. The code work follows the answers. Briefs: `work/pr8793/`, `work/pr8658/`, `work/pr8824/`.
- Item B: shortlist #3, re-enabling `DiagnosticsLspSuite "reset"`. Test-only, run through the full loop S0-S8, with an explainer for the diagnostics flow.
- Item C: shortlist #4, running `step-into-scala-lib` for Mill. Test-only, in an L2 area, using one cloud session for the slow suite.
- In parallel: the explanation-debt sessions (shortlist #2). They cost the maintainer nothing.
- Strict mode means every stage and every gate, an Opus review even for test-only changes, a mandatory explain-back, WIP at most 2, and a ledger row with time per stage and Max usage per item.

**R3 Loosen on evidence (review after item 3, then after item 10).** One change at a time:
- Test- or docs-only items with 0 Important findings and 0 maintainer rounds, three times: allow a Sonnet review for that kind of item.
- First-try explain-back PASS three times in one area: reuse the explainer for small fixes there.
- Median maintainer rounds at most 1 over the last 5 PRs, with 0 repeated corrections: raise WIP to 3.
- Never loosen: L0 areas, P-ASK, the four never-post layers, or explaining every line.
- Tighten at once: a repeated correction, a red CI caused by you, a direction correction, or a failed explain-back.

**R4 Toward the maintainer path (month 2 on).** Shadow reviews first (shortlist #10). Then evidence-only help on others' PRs: reproduce the bug a PR claims to fix, or run its slow tests in the cloud. Also triage of `upstream-fix-needed` and stale issues. Once Q-BRANCH is answered, offer a short docs PR that writes the answer down. Then the next contributor does not cost the maintainer the same question: your principle 4, applied to the project.

### Metrics

| # | Metric | How | Baseline (your 21 PRs) | Target |
|---|--------|-----|------------------------|--------|
| 1 | Maintainer rounds per PR | ledger `maintainer_rounds` | median 0, p90 2, max 4; 11 of 21 had 0 | p90 at most 1 |
| 2 | Maintainer non-LGTM comments per PR | ledger | median 1, p90 6, max 14 | p90 at most 2 |
| 3 | Repeated corrections (a rule broken again) | `mistakes.md` | placement in 4 PRs, scope in 4, size in 3 (before any rules) | 0 once a rule exists |
| 4 | PRs closed for direction or need | ledger `state` + reason | 2 of 21 (#8468, #8745) | 0: ask first |
| 5 | Time to a decision (merged or closed) | ledger | median 6.5 days; 5 of 16 merges took more than 30 days; 3 open at 47-102 days | none open over 30 days without a decision |
| 6 | Your reply time to a review | ledger `notes` | 24 days on #8556 and #8542; 42 of the 97 days on #8504 (25, 15, 0 and 2) | at most 3 days |
| 7 | Red CI caused by you after a push | ledger | unknown (R1 data) | 0 |
| 8 | Local reviewer precision and recall | brief: finding fates; R1 eval set | to measure in R1 | precision 60%+, recall 70%+ on the eval set |
| 9 | Understanding | `learning-log.md`: first-try explain-back PASS, prediction hits per area | you said you can explain 2 of the 4 area groups you changed (debug and run; scaladoc, files, rename), not completions or BSP | BSP and completions explained back by the end of month 2 |
| 10 | Budget per item | Opus sessions, Max usage before and after, cloud runs | unknown | measure in R2, then set a weekly budget |
| 11 | Guardrail: regressions within 30 days traced to you | S9 searches | none known | 0. If it rises, tighten (R3) |

Review the metrics every 5 items, in 15 minutes: the ledger, then `mistakes.md`, then `autonomy.md`. The article's guardrail logic applies. If 1-6 improve while 7 or 11 get worse, you have not saved maintainer time, you have moved it.

---

## 10. Assumptions and open questions

### Assumptions (tell me if one is wrong)
- A1. GitHub user `jozanek` is you, and the 21 PRs analysed are yours (a trivial 2018 PR, #252, was left out).
- A2. `main` stays your default target, and `main-v2` stays L0 until you have one merged PR there.
- A3. Your machine runs Linux or macOS. Claude Code's built-in sandbox supports both; native Windows is not sandboxed.
- A4. Your local Metals clone has full history, for `git log -S` and blame. This session's clones were shallow.
- A5. Claude Max limits are the binding budget, and cloud sessions draw on the same plan. Check this in your usage view.
- A6. The v0 review data is near-verbatim but misses many inline comments. R1 replaces it.
- A7. Metals MCP runs whenever you work, because your editor is open on the repo.
- A8. The scalameta org policy binds Metals: Metals' guide defers to Scalameta's rules, which defer to the org guide.

### Open questions for you
- U1. Answered 2026-10-20: not now; later you want a remote ("origin") for it. The workspace is git-ready: `~/oss/metals/.gitignore` excludes `repo/` and `data/raw/`. Only you push it.
- U2. Answered 2026-10-20: yes, you can start cloud sessions without attaching your fork. The default stands: an anonymous clone of upstream.
- U3. Answered 2026-10-20: keep all three and finish them. See shortlist #1 and the three briefs in `work/`.
- U4. Do you want to use the Claude Code sandbox for local sbt runs? It isolates Bash only, and sbt needs network access to Maven Central and Sonatype. My recommendation: try it in R0; if sbt or MCP breaks, keep it off and rely on the cloud for anything untrusted.
- U5. Do you want to move toward `main-v2` later? That is where most of the work happens, and it would change the learning plan (MBT, Turbine, Bazel).
- U6. Answered 2026-10-20: the split is agreed (6 hours new work, 4 hours learning, 3 hours triage and shadow reviews, 2 hours feedback and notes).

### Open questions for maintainers (ask once, early, only when an item needs the answer)
- Q-BRANCH: for a bug on both branches, one PR to `main` (maintainers port it), or one PR per branch? Ask on the first item that has the choice.
- Q-COMMITS: new commits or a rewritten branch per review round? Ask only if a reviewer raises it; Metals `AGENTS.md` answers it for now.
- Per-item decisions, from the S3 rubric.
