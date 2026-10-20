# Review checklist for my changes to scalameta/metals (v0, 2026-10-18)

Mined from 58 merged, 22 closed-unmerged and 3 open PRs (21 of them mine) on public PR pages. Inline comments were often hidden from that scrape (example: #8874), so this is v0. Re-mine with `~/oss/bin/mine-reviews.sh` and update it: rollout step R1.
Used by `oss-reviewer` and by me before every PR. Keep it short. A rule that has caught nothing for 6 months moves to the archive at the end.

## What failure looks like in Metals
Most review comments on my PRs were about design and placement, scope, or size, not style. Of 20 closed-unmerged PRs, none was closed over style, tests or naming.

| ID | Failure | Evidence (maintainer words) |
|----|---------|-----------------------------|
| F-PLACE | Logic outside the component that owns the behaviour | "is it possible to just keep the compilations logic inside Compilations itself?" (#8745) |
| F-SIMPLE | A complete but complex fix where a simpler, good-enough one exists | "Even if we didn't handled everything 100%, but reduced flakiness it would be good enough." (#8745); "Let's simplify it" (#8489) |
| F-COMPILER | Re-implementing compiler logic in Metals instead of asking the presentation compiler | "We are essentially trying to mimic the compiler here and that is a difficult logic." (#8504) |
| F-HOTPATH | Extra work on indexing, didChange or per-keystroke paths; large caches | "during indexing, which needs to be performant" and "Is this neccessary to do onChange?" (#8504); "caching too large a collection" (#8742) |
| F-DEDUP | Creating duplicates and then deduplicating them later | "do we need to deduplicate it, since we added the duplication in the first place?" (#8504) |
| F-SYMPTOM | Handling the wrong output instead of its cause | "Maybe we could avoid adding cursor when it's not needed" (#8514) |
| F-REUSE | A new helper where one exists | "We already have the SemVer object" (#8864); "could we reuse ... ScaladocDefinitionProvider" (#8658) |
| F-NEED | Code, a setting or a feature nobody needs | "avoid the setting altogether, since it might be hard to discover" and "I would only add the user setting if users request it" (#8542); "Do we need this function still?" (#8882). Counter-example: on #8504 "Is this needed?" was answered with evidence and the code stayed, so check before you cut. |
| F-SIZE | Too much for one review | "a bit terrifying to review" (#8658); 16 files and 7 commits, closed (#8745) |
| F-TESTLEVEL | Tests of internals instead of observable LSP behaviour; no expected result | "these small unit tests don't test the actual behaviour" (#8556); "test an actual LSP behaviour that changes" (#8800); "Could we use `check`" (#8489) |
| F-COMMENT | Comments that repeat or explain nothing | "better to have no comments at all than to have comments that explain nothing" (#8620); "comments are repeated in a lot of places" (#8489) |
| F-THREAD | Ignoring a threading or fallback invariant | "The presentation compiler operates on one thread only" and "InteractiveSemanticdb is more of a fallback" (#8789) |
| F-SCALA3 | Scala 3 presentation-compiler work in this repo | "we don't run Scala 3 tests in metals repo" (#8468). The Scala 3 PC lives in scala/scala3. |

## Before the PR exists (process)
- P-ASK: An issue older than 12 months, a feature, a new setting or an MCP tool: ask on the issue first. Evidence: #8468 (2021 issue, then "I should go over older issues and figure out if all of them make sense"); #8824 and outsider PRs #8388, #8369 with no issue drew months of silence.
- P-BRANCH: A 1.x bug goes to `main`. Ask before targeting `main-v2` or opening a second PR for it ("Most changes and improvements should be in main-v2", #8588; bulk backports, #8738).
- P-WIP: At most 2 of my PRs wait on a maintainer. In June I opened 13 in 12 days for one reviewer.
- P-CI: A red check that also fails on `main` is not mine; say so with the link ("Doesn't seem to fail on main", #8529; "it might be unrelated", #8852).
- P-ANSWER: Answer every review comment, in one batched review, within 3 days. #8658 left direction comments unanswered for months; on #8556 and #8542 I took 24 days to answer a round.

## Mechanical (lint-change.py enforces these; metals-gates.sh adds scalafmt, scalafixCheck, docs, MiMa and the test gates)
| ID | Level | Rule | Source |
|----|-------|------|--------|
| P-BASE | ERROR over 150 files or 100 commits, else WARN | wrong base branch, or a PR to split | 2026 PRs with 857-1822 stray commits; CodeRabbit file limit |
| P-FIXUP | ERROR | no `fixup!`/`squash!` commits | org CONTRIBUTING.md |
| P-ATTR | ERROR over 1 | at most one agent attribution per commit or PR body | org CONTRIBUTING.md |
| P-1LINE | ERROR | one line per PR paragraph (code blocks excluded) | org CONTRIBUTING.md |
| T-SHARD | ERROR | a new `tests/unit` suite is listed in `project/TestGroups.scala` | build.sbt (isInTestShard) |
| S-DEBUG | ERROR | no `pprint.log` in production code | getting-started.md (debugging) |
| P-SUBJ | WARN | commit subject of at most 50 characters | org AGENTS.md (see D-ORGSTYLE) |
| S-COMMENT | WARN | a comment over one line is a `/* */` block | org AGENTS.md (see D-ORGSTYLE) |
| P-CONV | WARN | conventional-commit subject | getting-started.md |
| P-WRAP | WARN | commit body wrapped at 72 | org AGENTS.md |
| P-PLAIN | WARN | sentences of 20 words at most in the PR body | org AGENTS.md (Plain English) |
| P-TMPL | WARN | PR body has "Now", "Tests:", "Risk" lines | templates/pr-description.md |
| R-RISKY | WARN | risky path (L0) touched | autonomy.md |
| T-NAME | WARN | kebab-case test names | Metals AGENTS.md |
| S-RETURN | WARN | no non-local `return` | Metals AGENTS.md |
| S-PRINT | WARN | no `println` in production code | Metals logs with scribe |
| S-TODO | WARN | no new TODO/FIXME | say it in the PR instead |
| P-NOISE | INFO | no test counts or "formatted" in commit bodies | org AGENTS.md |
| P-ACTIVE | INFO | possible passive voice in the PR body | org AGENTS.md (Plain English) |
| S-ITER, S-TOLIST | INFO | `.iterator` / `.toList` only when needed | Metals AGENTS.md |
| C0 | WARN | the range has no commits | sanity check |

## Reviewer output (oss-reviewer)
- First line: the count of findings, or "0 findings. Nothing to fix."
- Tags: Important, Nit, Pre-existing. At most 3 nits. Each finding cites `path:line` and quotes the line. No finding that the mechanical checks already report.
- Name the class of bug and every instance. Never repeat a finding from an earlier round.
- Skip: `website/` (bot-updated npm dependencies), `tests/unit/src/test/resources/` (fixtures), `NOTICE.md`.

## Archive (rules with no hits for 6 months)
(empty)
