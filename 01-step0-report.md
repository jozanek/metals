# Step 0 report: how scalameta/metals works, for an outside contributor

Date: 2026-10-18. Upstream `main` @ 8c095fe5 (2026-10-09), `main-v2` @ d6eb032e (2026-10-11). Your fork's `main` (jozanek/metals @ bddd284, 2026-06-05) is 191 commits behind upstream: never judge "still valid" against it.

Method: read the repository, the scalameta org policy repo, release notes and git history (2 years). Mined public PR pages: all 21 of your PRs, 42 merged PRs by others (32 outside contributors, 10 by the main maintainer), 20 closed-unmerged PRs by others, the issue tracker (252 open issues, labels, 15 recent issues for response times) and the open PR queue. Section 7 says what this could not see.

---

## 1. The ten things that matter most

1. **One person approves almost everything.** tgodzik approved every sampled contributor PR except two on `main-v2` (#8620 and #8773, approved and merged by zielinsky), and merged every sampled `main` PR. From April to October 2026 he is the only maintainer on the docs' list who authored merged PRs: 98, across both branches. On `main` his attention is the bottleneck.
2. **There are two live branches.** `main` carries Metals 1.6.x bugfix releases (1.6.6 in March, 1.6.9 in September). `main-v2` is Metals 2, "a major overhaul" for large monorepos, at milestone `v2.0.0-M16` in July. In 2026, `main-v2` touched 3.7 times as many distinct production files as `main` (741 vs 203) and had 7.7 times as many file changes (2,719 vs 352). Maintainers port fixes between the branches themselves, in bulk.
3. **Closed PRs die of direction, never of style.** Of 20 closed-unmerged PRs, none closed over style, tests or naming. The reasons were scope, placement, wrong branch, or a maintainer or rival PR covering the same ground (4 of 8 outsider PRs).
4. **Reviewers ask "is this needed?" and "can it be simpler?" first.** Next comes placement (keep logic in the owning component, reuse helpers), then hot paths (indexing, `didChange`, caches), then behaviour-level tests. Naming, formatting and PR titles are almost never discussed.
5. **First responses are fast; the tails are long.** Outsiders' merged PRs: first human response median 1 day (range 0-22), merge median 4 days (0-49). New issues: median 0 days (same day). But 9 non-draft PRs wait for a first review, 5 of them by outsiders and quiet for 30+ days. Three of the 9 are yours (#8658, #8793, #8824).
6. **There is a written AI policy, and it is new.** The scalameta org added `CONTRIBUTING.md` and `AGENTS.md` on 2026-09-18 with a section "Contributing with agents". Metals updated its own `AGENTS.md` on 2026-09-28. Section 5 has the details.
7. **AI use itself is accepted in practice.** Merged PRs carry Claude, Codex and Cursor trailers without comment. The maintainer writes "Had a quick LLM assisted look". What the policy controls is accountability and form, not use.
8. **CodeRabbit reviews every PR automatically.** Authors fix its findings silently, and maintainers never cite it. It is a free extra reviewer, not a gate.
9. **CI is heavy and somewhat flaky.** It runs unit tests in 4 shards on Windows and Ubuntu with two JDKs, plus integration jobs for sbt, Maven, Gradle, Mill, Bazel and Scala CLI, cross tests, MiMa, scalafix and docs. More than half of the 58 sampled merged PRs (32-36, by two counts) merged with some checks not passing; the pages do not say whether those checks failed or were skipped. The maintainer treats such failures as likely unrelated ("it might be unrelated, so don't worry about it", #8852).
10. **Your record is strong, and it has a clear pattern.** 21 PRs since June: 16 merged, 2 closed, 3 open. The 9 small, local fixes (the docs fix #8862 included) merged in 1-9 days with 0 rounds. The 7 that drew design, root-cause or test-level questions took 9-97 days and 1-4 rounds. Of the rest, two were closed and three are still open.

---

## 2. How the project works

**Code.** Scala 2.13 with some Java. On `main` the production code is about 114k lines: `metals` 78k (the LSP server), `mtags` 25k (Scala 2 presentation compiler and indexers, cross-built for many Scala versions), `mtags-shared` 5k (its sources are copied into scala/scala3), `mtags-interfaces` 2k (Java API, binary-checked by MiMa), `mtags-java` 3k, and `metals-mcp`. Tests are about 124k lines: `tests/unit` 69k (LSP suites against Bloop), `tests/cross` 35k (Scala 2 PC), `tests/slow` 14k (real build tools). The Scala 3 presentation compiler lives in scala/scala3, not here, and Scala 3 PC tests do not run in this repo. `main-v2` is bigger: 2,052 Scala and 352 Java files, with new modules (`semanticdb-javac`, `gradle-extractor`, `maven-metals`, `mtags-protobuf`, `vendor`).

**Guides.** `CONTRIBUTING.md` points to `docs/contributors/getting-started.md`, which defers to the scalameta contribution rules and the Scala Code of Conduct. `architecture.md` gives the high-level map. There is no PR template, no CODEOWNERS file, and no ADR folder. The decisions live in PR discussions and release notes (`website/blog/`).

**Issues.** The bug template asks for OS, editor, Metals and Scala versions. Feature requests go to scalameta/metals-feature-requests, questions to Discussions. Issues labelled `needs more information` auto-close after 30 days. There are 252 open issues: 117 `bug`, 42 `upstream-fix-needed`, 32 `Scala 3`, 21 `metals-v2`. 81% have not been touched for 6 months, 43% for 2 years. `good first issue` is dormant (3 open, all from 2023). The live newcomer label is `spree`, from the Scala Tooling Spree events: 6 open, 38 of 44 closed. There is no `help wanted` label. Discussions are quiet: 9 new threads in the last 12 months (3 of them unanswered Q&A), and 52 unanswered Q&A threads in total.

**Process.** Conventional commit titles (`fix:`, `bugfix:`, `improvement:`, `docs:`, ...), though nobody polices them. "Over-communicate" in commit messages. Ideally one commit per PR, and maintainers squash-merge. Tests: run one suite with `sbt --client unit/testOnly tests.X -- "*name*"` (your own #8862 fixed that doc). Register new unit suites in `project/TestGroups.scala`. Format with `./bin/scalafmt`, then run `sbt scalafixAll`. sbt writes a pre-push hook into `.git/hooks` that runs scalafmt.

**CI** (`.github/workflows/ci.yml`): unit tests (4 shards × Windows/Ubuntu × JDK 25, plus JDK 17 on Ubuntu), integration (sbt in 3 shards, sbt-metals scripted, Maven, Gradle including macOS, Mill, Bazel, Scala CLI, LSP feature tests), `+cross/test`, `javapc/test`, `scalafixCheck docs/docusaurusCreateSite`, `./bin/scalafmt --test`, and MiMa on `mtags-interfaces`. A separate workflow aggregates test failures. The docs are generated from `UserConfiguration`, `ServerCommands`, `ClientCommands` and `Configs`, so changing a setting can break the docs job.

**Bots.** CodeRabbit (every PR to `main` and `main-v2`; it refuses PRs over 150-300 files). Scala Steward and Dependabot (dependency PRs; Mergify auto-merges approved patch updates).

---

## 3. What reviewers care about (ranked, with evidence)

Counts are non-LGTM human comments. On your 21 PRs: design and placement 11 (4 PRs), scope and direction 7 (4 PRs), root cause 4 (2 PRs), split or reduce 3 (3 PRs), test style 2, performance 2. On 62 others' PRs: scope 15, placement 15, process/branch/CI 13, tests 7, correctness 7, idiom 5, cross-build 5.

1. **Need and simplicity.** "Is this needed?" (#8504; you answered it with evidence, and the code stayed). "Let's simplify it" (#8489). "I wonder if we want to add this logic for a minor inconvenience." (#8468). "Even if we didn't handled everything 100%, but reduced flakiness it would be good enough." (#8745). "I would only add the user setting if users request it." (#8542).
2. **Placement and reuse.** "is it possible to just keep the compilations logic inside Compilations itself?" (#8745). "We already have the SemVer object" (#8864). "could we reuse ... ScaladocDefinitionProvider" (#8658).
3. **Do not imitate the compiler; respect hot paths.** "We are essentially trying to mimic the compiler here and that is a difficult logic." and "during indexing, which needs to be performant" (#8504). "caching too large a collection" (#8742). "The presentation compiler operates on one thread only" (#8789).
4. **Root cause, not symptom.** "do we need to deduplicate it, since we added the duplication in the first place?" (#8504). "Maybe we could avoid adding cursor when it's not needed" (#8514).
5. **Behaviour-level tests.** "these small unit tests don't test the actual behaviour" (#8556; your evidence-based pushback was accepted). "test an actual LSP behaviour that changes" (#8800). "Could we use `check`" (#8489).
6. **Reviewable size.** "this is a bit terrifying to review 😅 Do you have any fixes unrelated to the current PR we could split?" (#8658).
7. **Branch and timing.** "Most changes and improvements should be in main-v2" (#8588). "I will merge it after the current release to just be on the safe side" (#8504).

Rarely or never raised: naming, formatting (the gates catch it), PR title format, commit structure, AI use, CodeRabbit.

---

## 4. How responsive the maintainers are

| Population | First human response (median, range) | Open until merge/close | Rounds (median) |
|------------|--------------------------------------|------------------------|-----------------|
| Outsiders' merged PRs (n=32) | 1 day (0-22) | 4 days (0-49) | 1 |
| tgodzik's own PRs (n=10) | (7 of 10 had no human review) | 1 day (0-4) | 0 |
| Closed-unmerged PRs (n=20) | 1 day (0-9; 9 PRs got no reply) | 7.5 days (0-107) | 0 |
| Your PRs (n=21) | 2 days (0-57) | 6.5 days (1-97) | 0 |
| New issues by non-maintainers (n=15) | 0 days (max 7) | 8 of 15 closed, median 5 days | |

How to read it: the first response is fast when it comes. The risk is the tail: a PR that lands when the maintainer is busy (a release, a `main-v2` milestone), or that needs a design decision, waits weeks. #8529 (95 days) was mostly maintainer latency. #8504 (97 days) split about evenly: 42 days were your turnaround (25, 15, 0 and 2 days), the rest the maintainer's. Much of the latency on #8556 (34 days) and #8542 (58 days) was yours: 24 days to answer a round on each. One polite ping restarted #8542. Your queue today: #8658 open 102 days (split requested, direction comments unanswered), #8793 66 days without a human review, #8824 47 days without a human review.

---

## 5. The AI-contribution rules

**Org policy** (scalameta/.github `CONTRIBUTING.md` and `AGENTS.md`, 2026-09-18; they apply to Metals, and a repo file may override them):
- The agent must be able to read those two files. If it cannot, it may not contribute. It must read both the repo `AGENTS.md` and the org `AGENTS.md`, and their rules bind every commit an agent writes.
- "You, the human author, answer for every line. A reviewer may ask about any line, and you must be able to explain it." Review both the code and "the scope and extent of tests".
- At most one agent attribution in a commit message or PR body (for example `Co-authored-by:`), never in code.
- "A reply that an agent posts on your behalf says so": end it with `*- <Agent> (on behalf of <you>)*`, or `(paraphrasing <you>)` when the words are yours.
- Commits: one concern each; never mix functional and cosmetic changes; change only what you must; each commit compiles, passes and is formatted; no `fixup!` commits.
- A bug fix is "a proof": preparation commits, then a tests commit that asserts today's (wrong) behaviour, then a fix commit that flips the assertions. Pin the sibling inputs too ("Find the cause and the cases like it").
- Plain English (ASD-STE100 rules) in comments, commit messages, PR bodies and replies: one idea per sentence, 20 words at most, active voice. PR body: what, why, how far it reaches; never narrate the diff; one line per paragraph.
- Review rounds: rewrite the branch and force-push; answer all comments in one review before pushing.
- CI for a new contributor runs only after a maintainer approves it, so validate locally first. This no longer applies to you after 16 merges, but each red push still costs a look.

**Metals `AGENTS.md`** (updated 2026-09-28): use Metals MCP tools to compile, test and format; `sbt --client` otherwise; kebab-case test names; `./bin/scalafmt` and `sbt --client scalafixAll` before committing; Scala style (no `.iterator` or `.toList` unless needed, for-comprehensions over long map/flatMap chains, never non-local returns); "always create new commits, instead of amending existing ones".

**Conflicts to resolve** (open questions in `notes/open-questions.md`):
- Q-COMMITS: the org guide says force-push rewritten rounds; Metals `AGENTS.md` says new commits. That line dates from #8275 (2026-03-24), before the org guide, but the repo file still wins: the org guide says a repo file "can possibly override or customize" its rules. Recommendation: follow Metals until a maintainer says otherwise. Squash merges make the history moot anyway.
- Q-ATTR: whether "one attribution" means per message or per PR. Recommendation: one trailer per commit, none in the PR body.
- Q-PROOF: the org's bug-fix-as-proof shape (prep, tests, fix commits) against Metals' "Ideally, each PR would only have one commit". getting-started.md also allows several self-contained commits. Recommendation: the proof shape; ask only if a reviewer objects.
- Q-MSG: the org says write a commit body only when the reason is not obvious; Metals says "over-communicate in your commit messages". Squash merges copy the PR description into the commit, so the PR body carries the explanation. Recommendation: short commits, a complete PR body.
- PR body content: org AGENTS.md says the investigated cases do not go into the PR body ("The test commit shows the cases"). The PR template follows that.
- D-ORGSTYLE (practice, not policy): Metals review does not enforce the org's 50-character subjects or `/* */` block comments. Your #8874, opened after the org guide, merged with neither. The linter still warns on both, because the policy binds agent-written commits.
- Q-SIG: the signature rule covers replies an agent posts. You post everything yourself. Recommendation: sign any reply whose words are the agent's, and prefer writing your own.

**Observed practice:** no disclosure is required beyond attribution, and none of your PRs carried one. Several merged PRs by others carry agent trailers. Nobody has questioned AI use in the sample.

---

## 6. Your track record as the baseline

| | Small, local fixes (9) | Merged after design, root-cause or test-level questions (7) | Not merged or still open (5) |
|---|---|---|---|
| PRs | #8456, #8463, #8464, #8465, #8518, #8549, #8676, #8861, #8862 | #8489, #8504, #8514, #8529, #8542, #8556, #8874 | #8468 (closed: not wanted), #8745 (closed: too complex), #8658, #8793, #8824 (open) |
| Days to merge | 1-9 | 9-97 | n/a |
| Rounds | 0 | 1-4 | 0-2 |

Every one of your 18 issue-linked PRs fixed an issue 4.6 to 6.1 years old. So your "oldest first" default produced 15 merges. Age did not predict the outcome. What predicted it was whether the fix stayed inside one component without a design question. In the slow group, part of the delay was also your own reply time: 24 days on #8556 and on #8542. Section 1 of `03-work-shortlist.md` builds on this.

---

## 7. What this report could not see

- PR data comes from public pages read by a small model (you chose this; `gh` was not authenticated here). Inline review comments were often hidden: for example, the 6 inline comments on #8874 came back without text. Quotes were cross-checked across two fetches, but treat them as near-verbatim. Run `mine-reviews.sh` on your machine (rollout R1) for exact data.
- Pages give dates, not times. Author badges are unreliable (tgodzik shows as "Contributor").
- The samples are recent (mostly April-October 2026) and small (n=10-32 per group). Medians are directional, not precise.
- Nothing here measures what maintainers think but do not write. Slow reviews are the only signal of that.

## Check your understanding
1. A new issue arrives today with a clear repro in the debug adapter. Using sections 1 and 4, how fast is tgodzik likely to respond, and what does that mean for when you should comment on the issue?
2. Why can a merged PR count be misleading as evidence of trust, given section 6?
3. Which two rules in section 5 conflict, and which source wins under the org guide's own terms?
