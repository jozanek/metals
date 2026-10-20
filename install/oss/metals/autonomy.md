# Autonomy map (per area). Rules: 02-operating-model.md, section 4.

Levels: L0 ask first · L1 propose with a recommendation · L2 decide, explain in the PR · L3 decide and defend.
"Explains" is your own answer from the interview (2026-10-18). Merge count alone never promotes.

| Area | Level now | Evidence | Next promotion needs | Demote if |
|------|-----------|----------|----------------------|-----------|
| Debug and run (DAP, jvmOptions) | L2 for bug fixes; L1 for new behaviour | #8463, #8518, #8549 merged with 0 rounds; #8556 1 round (test level); #8861 merged; you can explain it | 3 merged with at most 1 round, predictions 2/3 or better | a regression, or a direction correction |
| Scaladoc and docstrings | L1 | #8676 merged with 0 rounds; #8658 open 102 days (direction not settled); #8793 open 66 days with no review; you can explain it | settle #8658/#8793 first | another stalled PR |
| New-file templates, rename | L2 for fixes; L1 for anything with a setting | #8456 0 rounds; #8542 2 rounds (drop the setting); you can explain it | 2 more clean merges | a new setting without prior OK |
| Docs (contributor docs) | L2 for corrections; L1 for new sections | #8862 merged in 2 days with 0 rounds | n/a | a "lies" finding (wrong docs) |
| Tests only (regression tests, re-enabling ignored tests) | L2 | #8861 merged with 0 rounds | 2 more | a flaky test traced to you |
| Scala 2 presentation compiler (completions, auto-import) | L1, explanation debt | #8464 0 rounds; #8489 2 rounds; #8504 4 rounds, 97 days; #8514 1 round; you cannot yet explain them | explain back #8504 and #8514 first, then 3 clean merges | a "mimic the compiler" or hot-path correction |
| Build server / BSP / compile lifecycle | L0 for lifecycle or concurrency changes; L1 for small fixes; explanation debt | #8465 0 rounds; #8529 1 round, 95 days; #8745 closed (complexity, placement); #8874 1 round; you cannot yet explain them | explain back #8529 and #8874 first | any placement correction |
| MCP tools | L0 for new tools; L1 for fixes | #8824 open 47 days, no issue, no review | an answered question on #8824 | n/a |
| Indexing (mtags), toplevels | L0 | no PRs yet; performance goal in project-goals.md | an explainer, then 1 merged fix | n/a |
| Anything on `main-v2` | L0 | no PRs there yet; active redesign | 1 merged PR there | n/a |
| Risky paths: `mtags-interfaces`, `mtags-shared`, `.github/`, `build.sbt`, `project/` (except TestGroups), `bin/`, `sbt-metals/`, release | L0 always | binary API (MiMa), copied into scala/scala3, CI and release | never promoted | n/a |
