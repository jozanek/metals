# My mistakes, as rules (each one cost a maintainer a comment once)

Status: active (in checklist.md) or archived. Eval: re-run `oss-reviewer` on the pre-correction diff; `catches` means the current checklist flags it.
Fetch a pre-correction diff: `git -C repo fetch upstream pull/<N>/head:pr-<N>`, then pick the last commit before the review date from `data/raw/<N>/commits.json`.

| Date | PR | What happened | Rule | Eval |
|------|----|---------------|------|------|
| 2026-06-11 | #8468 | Fixed a 2021 issue; the maintainer then decided the behaviour should stay and closed the issue. | P-ASK | pending |
| 2026-06 to 09 | #8504 | First design re-implemented compiler logic at indexing time ("mimic the compiler", "needs to be performant"); 4 rounds, 97 days. | F-COMPILER, F-HOTPATH, F-DEDUP | pending |
| 2026-06 | #8489 | Repeated code comments; tests without an expected result; asked to simplify. | F-COMMENT, F-TESTLEVEL, F-SIMPLE | pending |
| 2026-06 | #8514 | Handled the error type instead of asking why CURSOR caused it. | F-SYMPTOM | pending |
| 2026-07 | #8556 | Added small unit tests of internals ("don't test the actual behaviour"). My pushback with evidence was accepted, so check before you "fix". | F-TESTLEVEL | pending |
| 2026-07 to 08 | #8542 | Added a user setting; the maintainer asked to drop it ("only add the user setting if users request it"). I took 24 days to answer one round. | F-NEED | pending |
| 2026-07 to 10 | #8658 | One PR with a feature plus fixes, 27 files ("terrifying to review"); direction comments left unanswered for months. | F-SIZE, P-ANSWER | pending |
| 2026-07 to 09 | #8745 | 16 files, 7 commits, a new dispatch gate and registry; replaced by a smaller fix inside `Compilations`. | F-PLACE, F-SIMPLE, F-SIZE | pending |
| 2026-09 | #8874 | Callbacks passed where objects fit (6 inline nits; text not scraped, verify in R1). | F-PLACE | pending |
| 2026-09 | #8824 | New MCP tool without an issue or a prior question; no human activity in 47 days. | P-ASK | pending |
| 2026-06 | (pattern) | 13 PRs in 12 days for one reviewer. | P-WIP | n/a |
