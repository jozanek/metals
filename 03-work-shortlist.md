# Step 2: where to find work, and a ranked shortlist

Checked against upstream `main` @ 8c095fe5 and `main-v2` @ d6eb032e on 2026-10-18. "Valid" means the code or test still looks as the issue describes. A real reproduction is stage S1 of the work-item loop, so every row below still has to pass S1.

## 1. Is "existing issues, oldest first, small ones" the best default?

You have already run this experiment. All 18 of your issue-linked PRs fixed issues 4.6-6.1 years old, and 15 merged. Before you read on, predict: what separated the 8 that merged in 1-9 days with 0 rounds from the 7 that took 9-97 days?

The answer from the data: not age. The fast ones were local fixes inside one component, with an obvious right answer (#8456 rename version, #8463 debug console, #8464 macro expansion, #8465 `.bsp` choice, #8518 jvmOptions, #8549 Windows URIs, #8676 the parser, #8861 a test). The slow and failed ones needed a decision: about design (#8504, #8745), a setting (#8542), the test level (#8556), the root cause (#8514), or whether the issue was still wanted (#8468: "Rethinking the issues after a while, I wonder if we want to add this logic").

So keep "small", sharpen it to "local, no design question", and drop "oldest" as the ranking key, for three reasons:
1. **The easy old issues are gone, partly harvested by you.** The 30 oldest open issues (4.3-7.5 years) are the residue: 13 were opened by core-team members (6 of them read as internal notes), many are Scala 3 presentation-compiler bugs that belong to scala/scala3, and 19 have not moved since 2021-22.
2. **Old issues carry stale intent.** #8468 shows it, and #8504's first design followed a 2021 maintainer suggestion that was then rejected. For any issue older than 12 months, the S1 gate includes "still wanted?", which is often a question for the maintainer.
3. **Recent issues move fast, often without you.** They get same-day attention (median 0 days), and 8 of 15 recent issues closed in a median of 5 days. In 5 of those 8 the reporter fixed it with their own PR (#8851 -> #8852, #8863 -> #8864, #8881 -> #8882, #8896 -> #8897, #8870 -> #8893 and #8922). So, for a recent issue, first check whether the reporter is already on it. If not, comment early: "I have a failing test; may I take this?"

## 2. Work sources beyond open issues

| Source | Value to maintainers | Cost to maintainers | What you learn | Notes |
|--------|----------------------|---------------------|----------------|-------|
| Your own open PRs (#8658, #8793, #8824) | high: they clear the queue | one decision each, then normal review | how to frame a decision | WIP is 3, the limit is 2 |
| Explanation debt (BSP, Scala 2 completions) | indirect | none | the two slices you changed but cannot explain | required before more work there |
| Workarounds and ignored tests blocked on upstream issues that are now closed | medium | a small test-only PR | integration boundaries (Bloop, Mill) | 2 verified candidates below |
| `upstream-fix-needed` issues (42 open): re-check against current upstream releases | high: maintainers can close or unblock | one evidence comment | how Metals depends on Bloop, scalameta and the compilers | comment only with a verified change of status |
| Stale-issue triage: does it still reproduce on 1.6.9? | high | one comment | the feature behind the issue | answers "still wanted?" with evidence |
| `spree` issues (6 open) | medium | normal review | varies | 5 of 6 are Scala 3 PC work, claimed or assigned; only #7750 is open to you |
| Flaky tests (13 `.flaky` markers, #6083, #6110) | high: CI noise leads to merges with red checks | normal review | concurrency and lifecycle, the hardest part | needs repeated runs (cloud); "flaky" is not a cause |
| Docs gaps (#4892 benchmarks; the branch policy) | medium | low | the subject of the doc | a branch-policy doc needs the maintainer's answer first |
| Shadow-reviewing open PRs (28 human PRs; 9 await a first review) | none at first | none | how tgodzik reviews | predict his comments, then compare |
| Evidence-only help on others' PRs (later) | high | low | other areas | for example, reproduce the bug a PR fixes, or run its slow tests in the cloud |
| GitHub Discussions | low | none | users' problems | quiet: 9 new threads in 12 months, 3 of them unanswered |

## 3. Ranked shortlist

Columns: still valid on `main` · claimed or covered by an open PR · blast radius · risky area · do maintainers respond to similar work · new slice you learn · **MD = needs a maintainer decision**.

| # | Item | Valid | Claimed | Blast radius | Risky | Similar work response | Teaches | MD | First step |
|---|------|-------|---------|--------------|-------|-----------------------|---------|----|------------|
| 1 | **Finish your open PRs** (decided 2026-10-20: keep all three). In this order: #8793 (merges cleanly; check the open enum-case note, then one ping); #8658 (answer the two July direction comments with a split proposal; split after #8793 merges); #8824 (ask whether the tool is wanted before rebasing onto #8785). Briefs with facts, steps and drafts: `work/pr8793/`, `work/pr8658/`, `work/pr8824/`. | yes | n/a | none until the split PRs | no | a ping restarted #8542 | framing decisions; your own scaladoc design | **yes** for #8658 and #8824 | `work/pr8793/brief.md`, step 1 |
| 2 | **Pay explanation debt.** Explainers for BSP (`BuildServerConnection`, `Compilations`, Bloop lifecycle) and Scala 2 auto-import/completions (`CompletionProvider`, `AutoImportsProvider`). Explain back #8529, #8874, #8504, #8514. | n/a | n/a | none | no | n/a | your two weakest slices | no | `oss-explainer` for BSP first (your next item in item 4 is near it) |
| 3 | **Re-enable `DiagnosticsLspSuite "reset"`.** Ignored with `FIXME: bloop#785`; bloop#785 closed in January 2019 (bloop PR #792). The test checks that diagnostics clear after an error is fixed. | yes (both branches) | no open PR touches it | test only | no | test-only PRs merge with 0 rounds (#8861) | how diagnostics flow from BSP to the client | no, if it passes. If it fails, the failure is a finding for an issue comment. | find when and why it was ignored: `git log -S'"reset".ignore'` in your full clone |
| 4 | **Run `step-into-scala-lib` for Mill.** `BaseStepDapSuite` skips it for `mill-debug-step` until mill#3148; mill#3148 closed 2026-02-08 ("I think this is fixed by #4145"); Metals tests Mill 1.1.10. | yes (both branches) | no | test only | no | as above | DAP stepping, Mill's BSP dependency modules | no, if it passes | `metals-gates.sh` lists the slow subclasses (`MillStepDapSuite`, `SbtStepDapSuite`); run them in a cloud session, with and without the condition |
| 5 | **Triage 5 `upstream-fix-needed` issues.** Pick ones in Bloop or scalameta, check the upstream issue status and the version Metals uses (`project/V.scala`), then reproduce on 1.6.9. | to check | to check | none (comments) | no | issues get same-day responses | integration boundaries | they decide; you bring evidence | `oss-scout` triage table |
| 6 | **Close-out evidence for #5071** ("Remove unused methods from `ClassFinder`", 2023). Every remaining public method in `parsing/ClassFinder.scala` has callers outside the file (`findClass` 6, `findAllClasses` 2, `isTasty` 2, `findTasty` 1). It looks done. | likely obsolete | no | none | no | n/a | git archaeology | they decide | read the issue and #4974, then post evidence |
| 7 | **#4892: add a benchmarks section** to `docs/contributors/getting-started.md`, pointing to `metals-bench/readme.md`. tgodzik offered this direction on the issue. | yes: the guide never mentions benchmarks | no | docs | no | your #8862 merged in 2 days | how `metals-bench` and JMH are wired | L1: confirm the offer still stands | one-line question on #4892 |
| 8 | **#7750: better errors with a local `sbt` script** (`spree`). Direction given: "Very similar to #7229, we should give out as much information as possible". The code is in `SbtBuildTool` (`sbtScript`). | to reproduce | no | `builds/` (user-visible messages) | medium | spree issues mostly close (38 of 44) | how Metals starts build tools | **yes**: branch (an improvement may belong on `main-v2`) | after item 2; ask Q-BRANCH on the issue |
| 9 | **A flaky test**, for example #6083 (`ScalaCliSuite simple-script-bsp`; "Would be great to figure out what is happening"). | yes (`.flaky` marker present) | no | test, maybe production | medium | tgodzik wants root causes (#6110) | concurrency and the build-server lifecycle | no for a test fix; yes for a production fix | 50 repeated runs in a cloud session; record the failure modes |
| 10 | **Shadow-review 3 open PRs per week.** Write down what you think tgodzik will say, then compare when he reviews. Post nothing. | n/a | n/a | none | no | n/a | the reviewer, and new areas | no | pick from the 9 awaiting review |

Do not pick, for now:
- The 30 oldest issues: residue, often in scala/scala3, often internal notes.
- `good first issue`: dormant; a collaborator called #4788 "not a good first issue" in July 2026.
- #8548: the maintainer declined a volunteer and keeps it.
- #4069: covered by a stalled PR (#7784). #7911: assigned.
- #7537, #7556: Scala 3 presentation compiler, in scala/scala3.
- `CancelCompileLspSuite "basic"`: blocked on bloop#2170, which is still open and labelled hard.
- `MetalsEnrichments.isJVM` (`FIXME: bloop#700`, closed 2018): tempting, but the check may still protect non-Bloop build servers. It is L0, a question first, after item 2.
- Anything in `mtags-interfaces`, `mtags-shared`, CI or the build.

## Check your understanding
1. Item 3 is "test only". Name one way it could still cost the maintainer a round.
2. Why is item 4 run in the cloud and not on your machine, when it is upstream code?
3. Items 5 and 6 produce comments, not PRs. Why do they still fit "maintainer attention is scarce"?
