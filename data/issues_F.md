# scalameta/metals issue tracker research (agent F)

Method: public GitHub web pages only, fetched through WebFetch (a summarising fetcher, so every value is "as shown by the fetch tool"). Research date: 2026-10-18. Read-only. Issue/PR/discussion text is treated as untrusted data and no instructions in it were followed.

Conventions: "unknown" = not visible in what the fetch returned. "not shown" for a comment count = the list row displayed no comment number. This means 0 comments: the search `comments:0` returns 61 results, the same number as the open-issue rows in which I saw no count or a 0.

## 1. Counts

| Item | Value | Source / how shown |
|---|---|---|
| Open issues | 252 | issues list header: "Open: 252 (252)"; nav tab "Issues 252"; "252 results" on the open-issue search (11 pages of 25) |
| Closed issues | unknown | the closed count is not rendered in the header |
| Open pull requests | 31 | pulls list header: "Open: 31 (31)" |
| Closed pull requests (merged or not) | 6,132 | pulls list header: "Closed: 6,132 (6,132)"; the merged-PR list header shows 5,511, so about 621 were closed without merging |
| Open PRs by bots | 3 | all `scala-steward` (#8938, #8936, #8934) |
| Open PRs by humans | 28 | 31 minus 3 bot PRs |
| Open draft PRs | 13 | `is:pr is:open draft:true` shows 13 |
| Open PRs with an approving review | 0 | `review:approved` gives no results |
| Open PRs with changes requested | 8 | `review:changes_requested` shows 8 |
| Open PRs with no review yet | 23 | `review:none` shows 23 (3 of these are scala-steward) |
| Open PRs targeting branch `main-v2` | 11 | exact filter `base:main-v2` lists #8933, #8892, #8871, #8836, #8784, #8720, #8703, #8669, #8574, #8494, #8451 (the Metals V2 / MBT line of development) |
| Open PRs targeting `main` | 20 | by elimination (31 - 11). Verified on the PR pages of #8939, #8793, #8093, #8407 (base `main`). Caution: the `base:main` search filter appears to match by prefix (it lists all 31 PRs) and `-base:main` wrongly returns nothing, so those two filters are unreliable |
| Labels in the repo | 98 | labels page header "98 labels" (4 pages: 30+30+30+8) |
| "help wanted" label | does not exist | not in the 98-label list; `label:"help wanted"` search gives "Open 0 (0)" / "No results matched your search" |
| Discussions total | about 158 (page shows no total) | 7 list pages (25 per page, 8 on the last); 53 answered + 52 unanswered Q&A; see section 7 |

## 2. Labels (98 labels; open-issue counts)

Per-label counts are NOT rendered on the public labels pages, so counts below come from tallying the labels on all 252 open-issue rows (11 list pages, fetched oldest-first) and were cross-checked against direct `label:` searches. Every cross-check matched exactly: bug 117, improvement 48, upstream-fix-needed 42, Scala 3 32, presentation-compiler 25, metals-v2 21, BSP 17, investigation needed 15, java support 11, tech debt 9, documentation 4, spree 6, good first issue 3, needs more information 2. Counts are open ISSUES only (open PRs are not included). 24 of the 252 open issues carry no label at all. GitHub also has an issue "Type" (e.g. "Bug") that is separate from labels; it is not counted here.

### Labels with at least one open issue (tally of 252 open issues)

| Label | Open issues | Label description (as shown) |
|---|---|---|
| bug | 117 | "Something that is making a piece of functionality unusable" |
| improvement | 48 | "Not a bug or a feature, but something general we can improve" |
| upstream-fix-needed | 42 | "Waiting on a fix upstream" |
| Scala 3 | 32 | "Generic ticket relating to Scala 3" |
| presentation-compiler | 25 | "Something relating to the presentation compiler" |
| metals-v2 | 21 | none shown |
| BSP | 17 | "Generic BSP related tickets" |
| investigation needed | 15 | none shown |
| java support | 11 | "Java support related tickets" |
| navigation | 9 | "Related to goto definition, find references, open symbol" |
| tech debt | 9 | "We should have addressed this yesterday" |
| bloop | 8 | "Bloop related tickets" |
| debug | 8 | "DAP debug related tickets" |
| sbt | 8 | "Generic relation to sbt" |
| scala-cli | 8 | "Relates to the scala-cli tool" |
| test-explorer | 8 | none shown |
| completions | 6 | "Tickets related to completion functionality" |
| mill | 6 | "Mill related tickets" |
| Scala 2 | 6 | none shown |
| semanticdb | 6 | "Related to semanticdb usage in Metals" |
| spree | 6 | none shown |
| model-context-protocol | 5 | none shown |
| worksheets | 5 | "Use for tickets related to worksheets" |
| bazel | 4 | none shown |
| documentation | 4 | "Tickets related to website and other documentation" |
| fixed-upstream | 4 | "Tag a ticket with this when a fix upstream has been completed and we can now address the ticket" |
| gradle | 4 | "Gradle related tikets" |
| code action | 3 | "Related to LSP code actions" |
| good first issue | 3 | none shown |
| hover | 3 | none shown |
| scalafix | 3 | "Relating to the built-in scalafix support" |
| affects clients | 2 | "Use this if you are adding a new setting or making a change that will affect clients." |
| document-highlight | 2 | none shown |
| feature-request | 2 | "Used for feature requests" |
| needs more information | 2 | "Use if we need more information for a specific ticket" |
| notebooks | 2 | none shown |
| priority:low | 2 | none shown |
| sbt server | 2 | "Relates to sbt BSP server support" |
| semantic-highlight | 2 | none shown |
| stability | 2 | none shown |
| bleep, decorations, diagnostics, doctor, emacs, flaky-test, inlay-hints, installation, performance, rename, reporting, scalafmt, signature-help, TVP, up for debate | 1 each | (various) |

### Labels highlighted in the brief

| Label | Open issues | Note |
|---|---|---|
| good first issue | 3 | #4788, #5680, #5708 (opened Jan 2023, Sep 2023, Oct 2023); see section 4 |
| help wanted | 0 (label does not exist) | not in the 98-label list; searches for the phrases "help wanted", "PRs welcome", "contributions welcome" in open issues return 0 results |
| bug | 117 | 46% of all open issues |
| needs more information | 2 | #5589 (Aug 2023), #8198 (Feb 2026) |
| Scala 3 | 32 | |
| presentation-compiler | 25 | |
| spree | 6 | appears to be the label for "Scala Tooling Spree" contribution events (inferred from a comment on #7556; the label has no description) - the closest thing to "help wanted"; 44 issues carry or carried it, 38 closed; see section 4 |
| metals-v2 | 21 | the new "Metals 2" / MBT work, mostly opened Jan-Oct 2026 |
| upstream-fix-needed | 42 | waiting on Scala compiler / Bloop / sbt / scala-cli etc. |
| investigation needed | 15 | triage label: not yet understood |

### Labels with 0 open issues seen on the 252 open-issue rows

ammonite support, artifact-migrations, backport-scala3-pc, call hierarchy, commit-count:1, commit-count:n:3, configuration, confirmed-reproduction, dependencies, duplicate, early-semver-major/minor/patch/pre-release, experiment, folding, github_actions, go-to-implementations, indexing, inline, javascript, library-update, maven, merge after release, missing-reproduction, new-feature, old-version-remains, priority:high, sbt-plugin-update, selection-range, semver-spec-major/minor/patch/pre-release, tokenizer, type hierarchy, version-scheme:always, version-scheme:early-semver, version-scheme:semver-spec, vscode, windows, wont-fix, zed. (Many of these are bot/release-tooling labels used on PRs.)

Observations: `confirmed-reproduction` and `missing-reproduction` are unused on open issues; `priority:high` has no open issue; `vscode`, `windows`, `maven` and `zed` also have none. All 98 label names: affects clients, ammonite support, artifact-migrations, backport-scala3-pc, bazel, bleep, bloop, BSP, bug, call hierarchy, code action, commit-count:1, commit-count:n:3, completions, configuration, confirmed-reproduction, debug, decorations, dependencies, diagnostics, doctor, document-highlight, documentation, duplicate, early-semver-major, early-semver-minor, early-semver-patch, early-semver-pre-release, emacs, experiment, feature-request, fixed-upstream, flaky-test, folding, github_actions, go-to-implementations, good first issue, gradle, hover, improvement, indexing, inlay-hints, inline, installation, investigation needed, java support, javascript, library-update, maven, merge after release, metals-v2, mill, missing-reproduction, model-context-protocol, navigation, needs more information, new-feature, notebooks, old-version-remains, performance, presentation-compiler, priority:high, priority:low, rename, reporting, sbt, sbt server, sbt-plugin-update, Scala 2, Scala 3, scala-cli, scalafix, scalafmt, selection-range, semantic-highlight, semanticdb, semver-spec-major, semver-spec-minor, semver-spec-patch, semver-spec-pre-release, signature-help, spree, stability, tech debt, test-explorer, tokenizer, TVP, type hierarchy, up for debate, upstream-fix-needed, version-scheme:always, version-scheme:early-semver, version-scheme:semver-spec, vscode, windows, wont-fix, worksheets, zed.

## 3. The 30 oldest open issues (sorted by creation date ascending)

Source: `is:issue is:open sort:created-asc`, page 1 (25 rows) plus the first 5 rows of page 2. Dates are as displayed. "Last updated" comes from a second listing sorted by least-recently-updated (`sort:updated-asc`), whose rows show an absolute "Updated on" date; only the 25 least recently updated open issues were read, so for the other 11 rows the only thing known is that they were updated on or after Oct 27, 2022 (written ">= Oct 27, 2022"). Comment count "0*" = the list row showed no comment number. That reading is confirmed: the search `is:issue is:open comments:0` returns 61 results, exactly the 61 open-issue rows in which I saw no count or a 0.

| # | Issue | Title | Opened | Opener | Labels | Comments | Last updated |
|---|---|---|---|---|---|---|---|
| 1 | #707 | Feature requests | May 1, 2019 | olafurpg | none | 1 | >= Oct 27, 2022 (pinned/locked meta-issue; last comment May 1, 2019; last timeline event Jul 4, 2023) |
| 2 | #1189 | Fetch main and test classes as soon as possible | Dec 16, 2019 | mzarnowski | debug, upstream-fix-needed | 1 | Dec 29, 2021 |
| 3 | #2563 | BSP connection being attempted isn't halted when `bsp-switch` happens. | Feb 27, 2021 | ckipp01 | BSP, bug | 0* | Aug 18, 2021 |
| 4 | #3383 | Invalid scaladoc links in hover response | Dec 17, 2021 | ayoub-benali | bug | 8 | >= Oct 27, 2022 |
| 5 | #3473 | Missing `provided`/ `optional` dependencies | Jan 5, 2022 | dos65 | improvement | 0* | Jan 18, 2022 |
| 6 | #3479 | Jdk sources selected incorrectly | Jan 7, 2022 | dos65 | improvement | 0* | Jan 18, 2022 |
| 7 | #3503 | Inconsistent test detection with project matrices | Jan 13, 2022 | keynmol | improvement, test-explorer | 4 | >= Oct 27, 2022 |
| 8 | #3527 | improvement: Don't partition test into shards manually | Jan 16, 2022 | kpodsiad | improvement, tech debt | 1 | >= Oct 27, 2022 (label change Nov 2, 2022) |
| 9 | #3622 | Code Autosuggest/Autocomplete Issues | Feb 9, 2022 | LingarajVB | improvement, presentation-compiler | 7 | Feb 11, 2022 |
| 10 | #6782 | Add a way to filter in/out modules to prevent metals from triggering their compilation | Mar 1, 2022 (see notes) | Baccata | improvement | 21 | >= Dec 11, 2024 (label added); last comment Feb 17, 2023 |
| 11 | #3690 | Second parameter starts with `$` become `\|` in autofill arg completion, hover, signature help (Scala2) | Mar 9, 2022 | tanishiking | bug, completions, Scala 3, upstream-fix-needed | 1 | >= Oct 27, 2022 |
| 12 | #3722 | Doctor - compilation status improvements | Mar 16, 2022 | kpodsiad | doctor, improvement | 0* | Mar 16, 2022 |
| 13 | #3727 | Virtual Documents based dependency source reader lost the in-editor breadcrum | Mar 16, 2022 | spangaer | improvement | 3 | Mar 22, 2022 |
| 14 | #3741 | Cannot decompile the companion object of an opaque type in Scala 3 | Mar 21, 2022 | Atry | bug | 1 | Mar 21, 2022 |
| 15 | #3757 | Stale diagnostics after build re-import | Mar 25, 2022 | pvid | bug | 5 | Mar 29, 2022 |
| 16 | #3761 | asTerm called on not-a-Term val <none> error in Scala 3 | Mar 26, 2022 | ckipp01 | presentation-compiler, Scala 3 | 12 | >= Oct 27, 2022 |
| 17 | #3771 | Test Explorer - munit support status | Mar 30, 2022 | kpodsiad | test-explorer | 0* | Jul 22, 2022 |
| 18 | #3809 | Ambiguous symbols are not always disambiguated in hovers | Apr 8, 2022 | desophos | bug, Scala 3 | 2 | >= Oct 27, 2022 |
| 19 | #3915 | Wrong details for `sliding` method | May 13, 2022 | tgodzik | bug, presentation-compiler, Scala 3 | 2 | >= Oct 27, 2022 |
| 20 | #3939 | Metals doesn't recognise method overrides with vararg params | May 23, 2022 | Arthurm1 | bug, Scala 2, semanticdb | 4 | May 24, 2022 |
| 21 | #3975 | Metals cannot follow definitions of some items | Jun 1, 2022 | frioux | gradle | 16 | >= Oct 27, 2022 |
| 22 | #4036 | Unable to import gradle build. | Jun 6, 2022 | ckipp01 | bloop, gradle, upstream-fix-needed | 20 | Jun 16, 2022 |
| 23 | #4040 | Opened sources from dependencies aren't updated after build import | Jun 17, 2022 | dos65 | bug | 0* | Jun 20, 2022 |
| 24 | #4054 | Integral goes before Int in completion | Jun 22, 2022 | kurnevsky | bug, presentation-compiler | 4 | Jul 1, 2022 |
| 25 | #4057 | Protobuf generated (Java) package not detected | Jun 22, 2022 | vishalovercome | none | 7 | Jun 28, 2022 |
| 26 | #4065 | cant' code navigation | Jun 25, 2022 | fuyou001 | bug, gradle | 4 | Aug 12, 2022 |
| 27 | #4069 | overlapping param names in generating for comprehension | Jun 27, 2022 | ghost (deleted account) | bug, code action, spree | 0 | >= Oct 27, 2022; last activity Sep 11, 2025 (commits by Perl99, PR #7784) |
| 28 | #4070 | Should I get an error when running `run_scalafix` without having any rules defined? | Jun 27, 2022 | ckipp01 | improvement, scalafix | 8 | Jun 28, 2022 |
| 29 | #4143 | Formatting with Scala 3 can break your build when triggered in a `project/*.scala` file | Jul 12, 2022 | ckipp01 | none | 7 | Jul 13, 2022 |
| 30 | #4156 | Stack overflow on VSCode with Metals but not on IntelliJ IDEA, for ZIO effect with recursion | Jul 15, 2022 | robknapen | bug, debug | 2 | Jul 19, 2022 |

Statistics for these 30 rows (computed by script from the table data):
- Age: 4.3 to 7.5 years (all opened May 2019 - Jul 2022).
- 13 carry `bug`; 9 carry `improvement` (4 of them only `improvement`: #3473, #3479, #6782, #3727); 3 carry `upstream-fix-needed` (#1189, #3690, #4036); 3 have no label (#707, #4057, #4143).
- 6 involve Scala 3 / presentation-compiler / completions (#3622, #3690, #3761, #3809, #3915, #4054); 4 involve build tools or BSP (#2563, #3975, #4036, #4065).
- 13 were opened by core-team members (ckipp01 x5, dos65 x3, kpodsiad x3, olafurpg, tgodzik); 6 of those 13 have 0 comments and read as internal notes or tracking issues (#2563, #3473, #3479, #3722, #3771, #4040). Across all 30 rows, 7 have 0 comments (those 6 plus #4069).
- 19 of the 30 are among the 25 least recently updated open issues (last updates between Aug 2021 and Aug 2022).

Notes on individual rows:
- #707 "Feature requests" (opened by olafurpg, May 1, 2019): the body tells users to file feature requests in a separate repository and says "The main issue tracker is reserved for bug reports and issues with an assigned milestone." A bot comment lists top-voted requests; the issue was pinned and the conversation locked to collaborators on May 1, 2019. It is a meta/pinned issue, not a work item.
- #6782: the page's timeline shows tgodzik transferred it from `scalameta/metals-feature-requests` on Sep 17, 2024, which explains the Mar 1, 2022 date next to a 6xxx number. Assigned to tgodzik; 21 comments; last comment Feb 17, 2023 (a long discussion about not compiling every cross-built module).
- #4069 is labelled `spree`; PR #7784 (Perl99, open, changes requested, last updated Sep 17, 2025) is the attempt to fix it.

### How stale is the whole open backlog (252 open issues)?

| Measure | Value | Source |
|---|---|---|
| Open issues not updated since before 2026-04-18 (6+ months) | 203 of 252 (81%) | search `updated:<2026-04-18` |
| ... before 2025-10-18 (1+ year) | 178 of 252 (71%) | search `updated:<2025-10-18` |
| ... before 2024-10-18 (2+ years) | 109 of 252 (43%) | search `updated:<2024-10-18` |
| Open issues with zero comments | 61 of 252 (24%) | search `comments:0` (matches my row tally) |
| Opened more than 1 / 2 / 3 / 4 years ago | 193 / 136 / 97 / 44 | computed from the 252 rows' opened dates |
| Opened per year (open ones only) | 2019: 2, 2021: 2, 2022: 46, 2023: 57, 2024: 48, 2025: 41, 2026: 56 | computed |
| Open issues opened in 2026 that carry `metals-v2` | 21 of 56 | computed |
| Open issues labelled `bug` | 117 of 252 (46%) | label search |
| Least recently updated open issue | #2563, last updated Aug 18, 2021 | `sort:updated-asc` |

## 4. Open "good first issue" / "help wanted" issues (and closest equivalents)

What exists:
- `help wanted`: the label does not exist (not among the 98 labels; label URL returns an empty list). Searches of open issues for the phrases "help wanted", "PRs welcome" and "contributions welcome" return 0 results, and "good first issue" as text matches only #4788.
- `good first issue`: 3 open issues. 23 issues carry or carried the label in total (3 open, 20 closed). Seen on the label's search page (created-descending), the newest-created issue with the label is #6252 (closed Mar 28, 2024); the newest-created *open* one is #5708 (Oct 3, 2023).
- `spree` (no description): 6 open issues; 44 carry or carried it in total (38 closed), so most tagged issues did get resolved. It is the closest equivalent to "help wanted": it has been in use for years (closed examples include #4215, closed May 19, 2023, and #4178, closed Feb 20, 2025) and maintainers applied it to the currently open ones between Jun 4, 2025 and Oct 21, 2025 (kasiaMarek on #7537 Jun 4, 2025 and #4069 Jun 26, 2025; tgodzik on #7556 Jun 9, #7750 Aug 27 and #7911 Oct 21, 2025). A comment on #7556 (Jun 26, 2025) refers to the "Scala Tooling Spree" (paraphrase from the fetch tool), which is why I read the label as newcomer-event tagging; the label itself has no description, so that reading is an inference.
- Secondary "approachable" sets that are not newcomer-labelled but are small, self-contained or documentation work: `tech debt` (9 open) and `documentation` (4 open). 10 of those (not already counted) were opened too.
- Fetch budget: 19 distinct issue pages opened for this section (3 + 6 + 10), plus one re-fetch of #4788 to verify exact quotes: 20 fetches in total (limit 25).

### 4a. Explicitly newcomer-labelled (good first issue, spree)

| Issue | Title | Opened | Labels | Comments | Claimed? | Maintainer said how to fix? | Linked / mentioned PR | Last comment |
|---|---|---|---|---|---|---|---|---|
| #4788 | Clean constructor parameters for `Indexer` and `ScalaCli` | Jan 1, 2023 (kpodsiad) | good first issue, improvement, tech debt | 6 | Informally, in 2023: Abhijeetmishr said on Feb 19, 2023 they would like to raise a PR, and on Mar 2, 2023 mentioned PR #5021. Never assigned; no PR shown in the Development panel | Only a generic offer: tgodzik, Feb 20, 2023: "Let us know if you need any hints!". In Jul 2026 odisseus (Collaborator) discussed the pitfalls (volatile parameters, snapshots) and wrote on Jul 31, 2026: "By the way, I'd argue that this is not a good first issue." (the comment adds that it "may be a good entry point for a dedicated person who wants to become familiar" with the code) | #5021 and #4776 mentioned (state not shown); none linked | Jul 31, 2026 (odisseus) |
| #5680 | When a name like `res2` is used in a worksheet, it causes a double definition | Sep 26, 2023 (spamegg1) | bug, good first issue, worksheets | 4 | Informally: zxdsc, Oct 15, 2023: "I would like to take care of it" (jkciesluk welcomed it Oct 16, 2023). Not assigned; no PR from zxdsc visible | Yes: jkciesluk (Member), Sep 26, 2023: "I think we should add `$` to names generated by `mdoc`" - points at mdoc's Scala 3 `Instrumenter.scala` | The fix is in another repo: scalameta/mdoc#1158 (SatvikMishra08, state not shown) and an mdoc commit 7acb37a by tgodzik on Sep 29, 2026 ("fix: skip user-defined names when gensymming resN binders") reference this issue. Issue still open | Sep 19, 2026 (SatvikMishra08) |
| #5708 | Missing documentation for "commands" in Emacs docs | Oct 3, 2023 (cpitclaudel) | documentation, emacs, good first issue | 9 | Offers only, no assignee: ag91 offered to open a PR (Nov 3, 2023); dohrisalim offered to improve the docs (Nov 9, 2025). No PR visible | Partly: tgodzik, Oct 3, 2023, said it needs docs changes only and asked Emacs users to add info; contributors (KaranAhlawat, ag91) explained how lsp-metals wraps commands as interactive functions | none | Nov 9, 2025 (dohrisalim) |
| #4069 | overlapping param names in generating for comprehension | Jun 27, 2022 (deleted account "ghost") | bug, code action, spree | 0 | No comment or assignee, but a contributor (Perl99) has an open PR | No comment on the issue; guidance sits on the PR (see below) | PR #7784 (Perl99, opened Sep 11, 2025): tgodzik requested changes on Sep 16, 2025 (asked whether the author still has time, suggested splitting out a simpler code action first; move logic into `resolveCodeAction`; use `compilers.references`). Last activity on the PR Sep 17, 2025; stalled for about 13 months | no comments (last activity on the issue: commits by Perl99, Sep 11, 2025) |
| #7433 | Support eta-expansion in 'convert to named lambda parameters' code action | May 1, 2025 (KacperFKorban) | code action, improvement, spree | 0 | No | Opener's body, not a maintainer, points to an ignored test in `ConvertToNamedLambdaParametersSuite.scala` in the scala/scala3 repository (the code action lives in the Scala 3 compiler repo); mentions scala/scala3 PR #22799 (state not shown) | none in Metals | no comments |
| #7537 | Parameter hints for method of a structural type show hints for applyDynamic | Jun 3, 2025 (TomasMikula) | bug, Scala 3, spree, upstream-fix-needed | 1 | No | No | none | Jan 22, 2026 (pranjal270: reproduces on Scala 3.7.4) |
| #7556 | Parameter hints of extension methods do not instantiate outer (extension[A]) type parameters | Jun 8, 2025 (TomasMikula) | bug, Scala 3, spree | 6 | No | Yes: tgodzik (Jun 9, 2025) noted completion handles it but the signature provider does not; rochala (Collaborator, Jun 27, 2025) suggested rebuilding the signature from the function type, likely in `toParamss` in `Signatures.scala` | none | Jul 1, 2025 (rochala) |
| #7750 | Metals should accurately report errors when using local `sbt` executable | Aug 26, 2025 (hearnadam) | improvement, sbt, spree | 1 | No | Indirectly: tgodzik (Aug 27, 2025) says it is "Very similar to #7229 we should give out as much information as possible"; #7229 is a closed `spree` issue ("Import partially failed - message improvement idea", closed Sep 5, 2025) | none | Aug 27, 2025 (tgodzik) |
| #7911 | Wrong rendering parametric extension method type argument | Oct 21, 2025 (ypytomets) | inlay-hints, presentation-compiler, Scala 3, spree | 3 | Yes, by assignment: zielinsky self-assigned on Mar 12, 2026. A commit by dorodb-web22 in a fork of scala/scala3 (Feb 7, 2026, 3abc98d) also references the issue | No (tgodzik only asked for the snippet and thanked the reporter) | none (no PR; one fork commit) | Oct 21, 2025 (tgodzik) |

Summary of the nine: 1 formally assigned (#7911); 1 has an open but stalled PR (#4069 via #7784); 1 is being fixed in a different repository (#5680, mdoc); 2 carry only old informal offers with no assignee or PR (#4788 from 2023, #5708 from 2023 and Nov 2025); 4 show no claim at all (#7433, #7537, #7556, #7750). Maintainers gave concrete code-level hints on 2 of them (#5680, #7556). At least three of the nine point to work outside the Metals repository: #5680 (fix in scalameta/mdoc), #7433 (the existing test is in scala/scala3) and #7911 (the only visible fix attempt is a commit in a scala/scala3 fork); #7537 is labelled upstream-fix-needed.

### 4b. Secondary candidates (tech debt / documentation; not newcomer-labelled)

| Issue | Title | Opened | Labels | Comments | Claimed? | Maintainer said how to fix? | Linked / mentioned PR | Last comment |
|---|---|---|---|---|---|---|---|---|
| #3527 | improvement: Don't partition test into shards manually | Jan 16, 2022 (kpodsiad) | improvement, tech debt | 1 | No | Partly: tgodzik (Jan 17, 2022) suggests adding new suites to the first shard for now and asks if munit's Category would be better; body names `project/TestGroups.scala` | none | Jan 17, 2022 |
| #4160 | Properly mention all the client commands | Jul 18, 2022 (tgodzik) | affects clients, documentation, tech debt | 0 | No | Body proposes two options (document all client commands, or refactor into a shared set) | none (links discussion #4146) | no comments |
| #4211 | Add sbt-vspp for publishing sbt-metals plugin | Aug 1, 2022 (kpodsiad) | improvement, tech debt | 0 | kpodsiad self-assigned Aug 1, 2022 and removed himself Jan 8, 2023; unassigned now | Body: "The same as in scalacenter/bloop#1766" | scalacenter/bloop#1766 mentioned | no comments |
| #4445 | Debug shouldn't be allowed for build server which don't implement debug. | Sep 26, 2022 (kpodsiad) | improvement, tech debt | 0 | No | Body suggests checking the build target's debug capability; needs scalacenter/bloop#1820 | scalacenter/bloop#1820 mentioned | no comments |
| #4785 | Refactor usages of old `MetalsLanguageServer` in tests | Dec 30, 2022 (kpodsiad) | improvement, tech debt | 0 | No | Body describes the goal (reduce `TestingServer` coupling to internals) | #4776 mentioned | no comments |
| #4892 | Add section about benchmark in documentation | Jan 23, 2023 (kpodsiad) | documentation | 3 | No | Partly: tgodzik says benchmarks are documented in the metals-bench folder and offers to add info to the contributing guide; kpodsiad says that README is outdated | none | Jan 24, 2023 |
| #5071 | Remove unused methods from `ClassFinder` | Mar 21, 2023 (kpodsiad) | tech debt | 0 | No | Body: arose in review of PR #4974; check which tests are still valuable | #4974 mentioned | no comments |
| #6083 | tests.scalacli.ScalaCliSuite.simple-script-bsp is flaky | Feb 2, 2024 (tgodzik) | flaky-test, tech debt | 0 | No | No (body: "Would be great to figure out what is happening") | none | no comments |
| #6110 | windows-latest jdk-17 unit tests always failed | Feb 10, 2024 (doofin) | tech debt | 3 | No | Partly: kasiaMarek (Member) says the failing suite `DebugProtocolSuite` is flaky; tgodzik wants the root cause found rather than ignoring the suite | none | Feb 15, 2024 |
| #8548 | Tidy up and document configuration options in v2 | Jun 16, 2026 (tgodzik) | documentation, metals-v2 | 2 | Asked, then declined: krrish175-byte asked "Can I take upon this issue?" (Jun 22, 2026); tgodzik answered the same day that he wants to handle it himself | Yes, a 4-step plan in the body (remove unused options, merge same-meaning options, check handling in `UserConfiguration`, write a user guide) | #8352 mentioned | Jun 22, 2026 |

Reading of 4b: none of the ten is assigned or has a linked PR; six have no comments at all (#4160, #4211, #4445, #4785, #5071, #6083); none shows a maintainer asking for outside help, and on #8548 a volunteer was turned down by the maintainer who opened it.

### 4c. Are the labels maintained and claimed? (evidence only)
- `good first issue`: dormant. The three open items are from Jan-Oct 2023; the label was applied by kpodsiad (Jan 1, 2023), jkciesluk (Sep 27, 2023) and tgodzik (Oct 3, 2023). The newest-created issue that carries it is #6252 (closed Mar 28, 2024). Not curated: on Jul 31, 2026 a Collaborator wrote on #4788: "By the way, I'd argue that this is not a good first issue." Claims: informal comments only ("would like to raise a PR" / "I would like to take care of it"), none turned into a visible PR on these three.
- `spree`: maintained in 2025 (labels added Jun-Oct 2025 by kasiaMarek and tgodzik); 38 of 44 labelled issues are closed (examples closed Jan 5-7, 2026: #7944, #7532), so tagged issues do get fixed. The six still open are the harder ones or need upstream work.
- No `help wanted` label and no explicit "PRs welcome" text on open issues.


## 5. Responsiveness: 15 most recent issues (open or closed) at least 14 days old, not opened by a maintainer

Selection: search `is:issue created:<2026-10-05 sort:created-desc` (open AND closed issues, newest first). Today is 2026-10-18, so "at least 14 days old" means opened on or before Oct 4, 2026. Each issue page was opened. Skipped as maintainer-opened: #8909 (opened by zielinsky, who shows a Member badge on his PRs and also labelled, self-assigned and closed it), #8840 and #8815 (tgodzik).

Who counts as a maintainer: GitHub's badge is unreliable here. tgodzik shows only a "Contributor" badge wherever a badge is displayed on issue and PR pages, yet he is the person who labels, closes, assigns milestones, announces releases and reviews PRs ("I was planning 1.6.9 next week"). ckipp01, jkciesluk, kpodsiad, kasiaMarek show "Member"; rochala and odisseus show "Collaborator". Times of day are not shown on the pages, so response times are whole calendar days (0 = same day). "n/s" = badge not shown on the page.

| Issue | Title (shortened) | Opener (badge) | Opened | First response by a human who is not the opener | Days | Maintainer labelled / triaged? | Current state (Oct 18, 2026) |
|---|---|---|---|---|---|---|---|
| #8914 | Notebooks: imports | Quafadas (Contributor) | Oct 1, 2026 | tgodzik (Contributor), comment, Oct 1, 2026 | 0 | No. No labels, no assignee | Open, 3 comments |
| #8913 | Notebooks: resource handling? | Quafadas (n/s) | Oct 1, 2026 | tgodzik (Contributor), comment, Oct 1, 2026 | 0 | Yes. tgodzik set type Bug and labels `bug`, `notebooks` on Oct 1 | Open, 1 comment |
| #8912 | Notebooks: Almond API not included in compile target | Quafadas (Contributor) | Oct 1, 2026 | tgodzik (Contributor), comment, Oct 1, 2026 | 0 | Yes. `bug`, `notebooks`, type Bug on Oct 1; asked halotukozak to look, who replied Oct 2 | Open, 3 comments |
| #8902 | SBT 2.0.x: sbt bsp hangs on `build/initialize` after bspConfig | Matboegli (Author) | Sep 30, 2026 | tgodzik (Contributor), comment, Sep 30, 2026 | 0 | Yes. `bug`, `sbt`, `sbt server`, `BSP`, type Bug on Sep 30 | Open, 10 comments; tgodzik linked PR #8937 on Oct 16 as the fix (that PR is open) |
| #8896 | get-docs/get-source fail to resolve Scala library dependency symbols | tkolleh (Contributor) | Sep 28, 2026 | tgodzik, closed it (no comment), Sep 30, 2026 | 2 | No labels | Closed as completed Sep 30 (fix PR #8897 referenced) |
| #8887 | Semantic tokens: $ident at column 0 in a multi-line interpolated string... | realstraw (n/s) | Sep 25, 2026 | tgodzik, closed it (no comment), Sep 28, 2026 | 3 | No labels | Closed as completed Sep 28 via PR #8895 |
| #8881 | Typing blocks for seconds in files with many diagnostics | Dolfik1 (n/s) | Sep 24, 2026 | tgodzik, closed it (no comment), Sep 25, 2026 | 1 | No labels | Closed as completed Sep 25 via PR #8882 |
| #8880 | MCP `inspect` returns no members when the build target comes from `module`... | calinburloiu (n/s) | Sep 23, 2026 | tgodzik (Contributor), comment "Thanks for reporting!", Sep 23, 2026 | 0 | Yes. `bug`, `model-context-protocol` on Sep 23 | Open, 1 comment |
| #8870 | metals-v2 gradle-exporter omits several properties from mbt.json | ErikAtSumo (n/s) | Sep 19, 2026 | tgodzik, triage only (labels `bug`, `gradle`, `metals-v2`, type Bug, self-assigned), Sep 22, 2026; no comment | 3 | Yes (Sep 22) | Closed as completed Oct 10 by the opener after fixes in PRs #8873, #8893, #8922 |
| #8863 | MCP `find-dep` reports a pre-release as the latest version | matejcerny (Contributor) | Sep 15, 2026 | tgodzik (Contributor), comment, Sep 15, 2026 | 0 | Yes. `bug`, `model-context-protocol` on Sep 18 | Closed as completed Sep 22 via PR #8864 |
| #8854 | Completion not shown with error "...ScalametaTokenizer$AsTokenize$ not a subtype" | wele0612 (n/s) | Sep 10, 2026 | tgodzik (Contributor), comment, Sep 10, 2026 | 0 | No labels | Closed as completed Sep 15 after a new release |
| #8853 | Metals 1.6.8 breaks autocomplete and type hinting for projects with scala 2.12 | kerzok (n/s) | Sep 10, 2026 | tgodzik (Contributor), comment, Sep 10, 2026 | 0 | Yes. `needs more information` on Sep 10 | Closed as completed Sep 15 ("new version is out! closing this one for now"); label left on |
| #8851 | MCP server rejects initialization requests with unknown JSON properties | povder (n/s) | Sep 10, 2026 | tgodzik, labels only (`bug`, `model-context-protocol`), Sep 11, 2026; no comment | 1 | Yes (Sep 11) | Closed as completed Sep 16 via PR #8852 |
| #8839 | Worksheet warnings about dollar signs | spamegg1 (Contributor) | Sep 8, 2026 | tgodzik (Contributor), comment, Sep 8, 2026 | 0 | Yes. `upstream-fix-needed` on Sep 10 | Open, 13 comments; a scala/scala3 commit (#27050) referencing it appeared Sep 11 |
| #8812 | `metals-mcp` hangs forever and dies on the 2-minute `Await` ... `LinkageError` | destitutus (n/s) | Aug 25, 2026 | tgodzik (Contributor), comment, Sep 1, 2026 | 7 | No labels | Open, 2 comments |

Supplementary, outside the 15 (the next two non-maintainer issues): #8806 (midgramr, opened Aug 17; ckipp01 [Member] replied Aug 21 = 4 days; label `needs more information` added by tgodzik Sep 11; closed as "not planned" by the github-actions bot on Oct 12 after 30 days without new information) and #8797 (Jasper-M, opened Aug 17; tgodzik replied and closed it Aug 21 = 4 days; milestone Metals v1.6.9).

Computed statistics for the 15 (script):
- Time to first response by a non-opener human, in days: 0 x9, 1 x2, 2 x1, 3 x2, 7 x1. Median = 0 days (same calendar day); mean = 1.1 days; maximum = 7 days. Responded within 1 day: 11 of 15; within 3 days: 14 of 15; within 7 days: 15 of 15.
- If only written comments count as a "response": 10 of 15 got one (9 on the same day, 1 after 7 days; median 0 days). 5 of 15 got no written reply at all, only a triage action or a close (#8896, #8887, #8881, #8870, #8851).
- Every one of the 15 first responses came from the same person, tgodzik. Over the sample, labelling by a maintainer: 9 of 15 labelled (6 not: #8914, #8896, #8887, #8881, #8854, #8812).
- Current state: 7 open, 8 closed. All 8 closed issues were closed as completed (7 by tgodzik, 1 by the opener), after a median of 5 days (range 1 to 21 days: 2, 3, 1, 21, 7, 5, 5, 6); 6 of 8 cite a fix PR and 2 closed after a release.
- Corroboration from pages opened for other sections (not part of the sample): the first maintainer reaction came the same day or next day on #5680 (Sep 26, 2023, jkciesluk), #5708 (Oct 3, 2023), #7556 (Jun 9, 2025), #7750 (Aug 27, 2025) and #7911 (Oct 21, 2025).

Caveats on the responsiveness picture:
- The sample is the newest issues, many are MCP/Gradle/sbt bugs that the lead maintainer can fix quickly, and three (#8912-#8914) come from one reporter on one day.
- Not every issue gets a reply: 61 of 252 open issues (24%) have zero comments. 39 of those 61 were opened by nine core accounts (internal notes: tgodzik, kpodsiad, ckipp01, dos65, kasiaMarek, jkciesluk, rochala, olafurpg, zielinsky). The other 22 were opened by other accounts, 10 of them in the last 12 months: #8061, #8235, #8239, #8253, #8426, #8435, #8455, #8495, #8663, #8686. Of the 50 open issues opened in the last 12 months by those other accounts, 40 have at least one comment (80%).

## 6. Open pull requests

31 open PRs in total: 28 by humans (all listed below, so fewer than the 30 requested exist) and 3 by the bot `scala-steward`. Order is "most recently updated first", as the list page returns it. Draft status comes from the filter `draft:true` (13 PRs); formal review state from `review:approved` (0), `review:changes_requested` (8) and `review:none` (23, including the 3 bots); base branch from `base:main-v2` (11 PRs; other PRs are on `main` by elimination, and four of them were confirmed on their PR pages). The list rows themselves do not show draft, review or base. "Days since update" is as of 2026-10-18. "List count" is the trailing number on the list row (probably comments, bot comments included). "(page checked)" = I opened the PR page.

| Rank | PR | Title | Author (badge in list) | Opened | Last updated | Days since update | Draft | Formal review | Base | List count | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | #8939 | bugfix: Doctor flags best effort only when a dependency has errors | leigh-perry (none) | Oct 17, 2026 | Oct 17, 2026 | 1 | no | none yet | main | 1 | New; only the CodeRabbit bot has responded so far (page checked) |
| 2 | #8937 | bugfix: Don't set additional data when different server is used | tgodzik (Contributor) | Oct 16, 2026 | Oct 16, 2026 | 2 | no | none yet | main | 3 | Maintainer PR; proposed fix for issue #8902 |
| 3 | #8933 | MBT: Speed up test class discovery in large workspaces | ErikAtSumo (none) | Oct 10, 2026 | Oct 13, 2026 | 5 | no | changes requested | main-v2 | 5 | tgodzik requested changes on Oct 11 (day after opening); author pushed a new commit and re-requested review from tgodzik on Oct 13. Waiting on reviewer (page checked) |
| 4 | #8916 | Notebook cell execution | halotukozak (Contributor) | Oct 5, 2026 | Oct 12, 2026 | 6 | no | changes requested | main | 18 | Notebooks area (see issues #8912-#8914); page not opened |
| 5 | #8857 | test: Test Scala 3.3.9 | tgodzik (Contributor) | Sep 11, 2026 | Oct 8, 2026 | 10 | yes | none yet | main | 1 | Maintainer CI/test draft |
| 6 | #8892 | Ignore implicit dependencies when collecting Bazel targets for MBT import | odisseus (Collaborator) | Sep 25, 2026 | Sep 28, 2026 | 20 | yes | none yet | main-v2 | 11 | Bazel/MBT series |
| 7 | #8784 | Proper source lookup when importing Bazel targets | odisseus (Collaborator) | Aug 11, 2026 | Sep 25, 2026 | 23 | no | none yet | main-v2 | 24 | Bazel/MBT series; not draft, no formal review, 24 comments |
| 8 | #8871 | Ensure that source files from Bazel external repos are indexed | odisseus (Collaborator) | Sep 21, 2026 | Sep 21, 2026 | 27 | yes | none yet | main-v2 | 1 | Bazel/MBT series |
| 9 | #8836 | Do not import source files from targets which don't belong to the project scope | odisseus (Collaborator) | Sep 7, 2026 | Sep 8, 2026 | 40 | yes | changes requested | main-v2 | 2 | Bazel/MBT series; draft with changes requested |
| 10 | #8720 | Do not use the unpinned repositories to resolve Maven dependencies in Bazel projects | odisseus (Collaborator) | Jul 23, 2026 | Sep 2, 2026 | 46 | yes | none yet | main-v2 | 1 | Bazel/MBT series |
| 11 | #8793 | fix: resolve scaladoc links against the documented member's SemanticDB owner | jozanek (Contributor) | Aug 13, 2026 | Sep 1, 2026 | 47 | no | none yet | main | 7 | Only CodeRabbit bot reviews (Aug 13, Sep 1); no human review or comment visible in 66 days (page checked) |
| 12 | #8824 | feat(mcp): add test-repeated tool for detecting flaky tests | jozanek (Contributor) | Sep 1, 2026 | Sep 1, 2026 | 47 | no | none yet | main | 3 | MCP tool; page not opened |
| 13 | #8669 | Add watchedFiles support to MBT script importers | zielinsky (Member) | Jul 10, 2026 | Aug 19, 2026 | 60 | yes | none yet | main-v2 | 8 | Member-authored draft |
| 14 | #8703 | mbt(bazel): add a streamed_proto decoder for bazel query output | maksymilianrozanski (Contributor) | Jul 21, 2026 | Aug 17, 2026 | 62 | no | changes requested | main-v2 | 19 | Changes requested; page not opened |
| 15 | #8658 | feat: make scaladoc/javadoc wiki links navigable in hover and go-to-definition | jozanek (Contributor) | Jul 8, 2026 | Aug 12, 2026 | 67 | no | none yet | main | 7 | List row also shows 1 linked reference; page not opened |
| 16 | #8761 | chore: Update sbt to 2.0.4 | tgodzik (Contributor) | Aug 3, 2026 | Aug 3, 2026 | 76 | yes | none yet | main | 1 | Maintainer draft |
| 17 | #8746 | Small improvements | odisseus (Collaborator) | Jul 28, 2026 | Jul 31, 2026 | 79 | yes | none yet | main | 1 | Bazel/MBT series |
| 18 | #8667 | feat(mcp): Add show-implicits MCP tool for inspecting implicits | matejcerny (Contributor) | Jul 10, 2026 | Jul 31, 2026 | 79 | yes | none yet | main | 14 | MCP tool; draft |
| 19 | #8494 | Resolve scala versions from streamed_proto for Bazel builds imported as MBT | maksymilianrozanski (Contributor) | Jun 10, 2026 | Jul 23, 2026 | 87 | yes | changes requested | main-v2 | 40 | Draft with changes requested; longest thread (40) |
| 20 | #8332 | Bazel native BSP integration | odisseus (Collaborator) | Apr 24, 2026 | Jul 1, 2026 | 109 | yes | none yet | main | 1 | Long-running draft |
| 21 | #8574 | Add BSP generated source manual suite | mahib-stripe (none) | Jun 22, 2026 | Jun 24, 2026 | 116 | no | none yet | main-v2 | 1 | No human review; the fetch tool reports a tgodzik commit message of Jul 8, 2026 saying such ManualSuite PRs are kept as unmerged branches for debugging (page checked) |
| 22 | #8451 | improvement: Don't run compile if no debugging is needed | tgodzik (Contributor) | Jun 4, 2026 | Jun 4, 2026 | 136 | yes | none yet | main-v2 | 3 | Maintainer draft |
| 23 | #8407 | Add OTEL tracing | sake92 (Contributor) | May 25, 2026 | Jun 2, 2026 | 138 | yes | none yet | main | 4 | tgodzik reviewed May 26 and Jun 2 (said he lacked time, gave direction); no activity since; waiting on author (page checked) |
| 24 | #7525 | Experimental Gradle import | Arthurm1 (Contributor) | May 31, 2025 | May 6, 2026 | 165 | no | changes requested | main | 8 | Changes requested; page not opened |
| 25 | #8093 | feat: Find All References includes overridden methods | warcholjakub (Contributor) | Jan 8, 2026 | Jan 9, 2026 | 282 | no | none yet | main | 1 | tgodzik left one inline question on Jan 9, 2026 (no reply from the author since); closes metals-feature-requests#94 (page checked) |
| 26 | #7891 | improvement: Show crashes more visibly for the user | tgodzik (Contributor) | Oct 10, 2025 | Oct 10, 2025 | 373 | no | none yet | main | unknown | Maintainer PR, untouched since opening; list row shows a linked-issue indicator |
| 27 | #7784 | Code action for-comprehension: support overlapping param names | Perl99 (not shown) | Sep 11, 2025 | Sep 17, 2025 | 396 | no | changes requested | main | 13 | Fixes spree issue #4069; tgodzik requested changes Sep 16, 2025, last reply Sep 17, 2025 (page checked) |
| 28 | #5884 | Initial support for remote reporters | WojciechMazur (not shown) | Nov 28, 2023 | Apr 9, 2024 | 922 | no | changes requested | main | 35 | Oldest open PR; list row shows '3 of 5 tasks' |

Bot PRs (not counted above), all by `scala-steward`, no reviews: #8938 "build(deps): Update mcp from 2.0.1 to 2.1.0" (opened Oct 16, 2026), #8936 "build(deps): Update scala-library from 2.13.18 to 3.10.0" (Oct 14, updated Oct 15) and #8934 "build(deps): Update mill-contrib-testng from 1.1.10 to 1.3.0" (Oct 10).

### Queue statistics (computed by script from the 28 human PRs)

| Measure | Value |
|---|---|
| Drafts | 13 of 28 |
| Formal review state | 0 approved, 8 changes requested (#8933, #8916, #8836, #8703, #8494, #7784, #7525, #5884), 20 no formal review (11 drafts + 9 non-drafts) |
| In the author's court by status (draft and/or changes requested) | 19 of 28 (13 drafts + 6 non-draft PRs with changes requested). Exception: #8933 already answered the review on Oct 13 and awaits re-review |
| Non-draft PRs with no formal review (waiting for a first review) | 9: #8939 (1 day since update), #8937 (2, maintainer's own), #8784 (23), #8793 (47), #8824 (47), #8658 (67), #8574 (116), #8093 (282), #7891 (373, maintainer's own). 7 of the 9 are by authors other than tgodzik; 5 of those 7 have had no update for over 30 days (#8793, #8824, #8658, #8574, #8093) |
| Not updated for more than 30 / 60 / 90 / 180 / 365 days | 20 / 15 / 9 / 4 / 3 of 28 |
| "Stale" (no update for more than 90 days) | 9 PRs: #8332 (109 days), #8574 (116), #8451 (136), #8407 (138), #7525 (165), #8093 (282), #7891 (373), #7784 (396), #5884 (922). By status: 3 drafts, 3 changes requested, 3 waiting for review |
| Median days since last update / median age | 64.5 days / 88 days |
| Authors | odisseus 7 (Bazel/MBT series; 5 target `main-v2`), tgodzik 5, jozanek 3, maksymilianrozanski 2, one each: leigh-perry, ErikAtSumo, halotukozak, zielinsky, matejcerny, mahib-stripe, sake92, Arthurm1, warcholjakub, Perl99, WojciechMazur |
| Base branch | 11 of the 28 human PRs target `main-v2` (Metals V2 / MBT line), 17 target `main` |
| Areas (from titles) | Bazel in the title: 7 PRs (#8892, #8784, #8871, #8720, #8703, #8494, #8332); MBT in the title: 5 (#8933, #8892, #8703, #8669, #8494); MCP tools: #8824, #8667; Notebooks: #8916; Gradle: #7525; scaladoc links: #8793, #8658; plus single fixes |

### Spot checks of PR pages (7 externally authored PRs)

| PR | Author | First human response | What I saw |
|---|---|---|---|
| #8939 | leigh-perry | none yet (1 day old) | CodeRabbit bot walkthrough only, no human review |
| #8933 | ErikAtSumo | tgodzik, Oct 11, 2026 (1 day after Oct 10) | Review with changes requested plus inline suggestions; author pushed a new commit and re-requested review on Oct 13 |
| #8793 | jozanek | none in 66 days | Only CodeRabbit bot reviews (Aug 13 and Sep 1); author pushed a follow-up commit on Sep 2; no human review |
| #8093 | warcholjakub | tgodzik, Jan 9, 2026 (1 day) | One inline question ("Do we ever set it to false?"); author has not replied for about 9 months; reactions from three other people; the PR page says at least one approving review is required |
| #8574 | mahib-stripe | none in 118 days | Only a CodeRabbit "review skipped" notice (base is not the default branch); per the fetch tool, a Jul 8, 2026 tgodzik commit message says such manual-suite PRs are kept as unmerged branches for debugging |
| #8407 | sake92 | tgodzik, May 26, 2026 (1 day) | Review comment and a follow-up on Jun 2 with direction ("Ideally, we could get traces on entire metals project with more exact timings."); no activity since |
| #7784 | Perl99 | tgodzik, Sep 11, 2025 (same day) | Inline comments, then changes requested on Sep 16, 2025; last reply Sep 17, 2025; stalled since |

Context for the merge flow (merged-PR list, first page): header "Closed: 5,511" for merged PRs (6,132 closed in total, so about 621 were closed without merging). The 25 most recently updated merged PRs were all merged between Oct 1 and Oct 11, 2026 (nothing newer on the list): 11 by tgodzik, 6 by dependabot, and 8 by other people (jchyb 4, ErikAtSumo 2: #8893 and #8922, zielinsky 1, jozanek 1: #8874). So outside contributors do get PRs merged, quickly when they respond to review, and 19 non-bot PRs were merged in that 11-day window; the open queue is slow mainly where PRs wait on their authors or sit without any human review.

## 7. GitHub Discussions

| Item | Value | How obtained |
|---|---|---|
| Categories | General, Polls, Q&A (no per-category counts shown) | discussions page |
| Total discussions the page shows | no total is displayed; the main list has 7 pages: pages 1 and 6 had 25 rows each, page 7 had 8 rows, pages 2-5 assumed 25 each, so about 158 discussions. The two pinned ones ("Welcome to Metals discussions", Dec 2020, gabro; "New Era: Tooling for Scala 3", Mar 2021, tgodzik) are also in the list | pages 1, 6, 7 counted directly |
| Q&A answered | 53 | `is:answered` filter: 3 pages of 25 + 25 + 3 rows |
| Q&A unanswered | 52 | `is:unanswered` filter: 3 pages of 25 + 25 + 2 rows. GitHub counts a discussion as unanswered until a reply is marked as the answer, even if people replied; the list includes closed discussions (at least "can't create connection to server", Nov 9, 2024, and "how to setup the environment for debugging the metals", Mar 7, 2024) |
| General / Polls (no answered state) | about 53 | derived: 158 - 53 - 52 |
| Newest discussion | May 14, 2026 ("Unable to use VScode on a Mill project", Q&A, answered, 2 comments) | list sorted by date created |
| Discussions created in the last 12 months (since Oct 18, 2025) | 9: May 14, 2026 (Q&A, answered), Apr 19, 2026 (Q&A, unanswered), Apr 3, 2026 (Q&A, unanswered), Mar 20, 2026 (Q&A, answered), Mar 4, 2026 (Q&A, unanswered), Dec 31, 2025 (General), Dec 9, 2025 (General), Nov 8, 2025 (General, closed), Oct 23, 2025 (Q&A, closed, answered). Nothing newer than May 14, 2026 | date-created view, first 12 rows |
| Recent unanswered | Of the 6 Q&A discussions created in the last 12 months, 3 are unanswered (Apr 19, Apr 3 and Mar 4, 2026). Only 3 of the 52 unanswered discussions are from the last 12 months; the newest unanswered is 6 months old | computed from the two views above |
| Unanswered by year created (all 52) | 2020: 1, 2021: 16, 2022: 11, 2023: 8, 2024: 7, 2025: 6, 2026: 3 | counted from the three unanswered pages |
| Unanswered with zero comments | 3 of 52 ("can't create connection to server", "Debugging "Unknown Source" and "Unsupported evaluation in unmanaged classpath entry"", "import scala project failed with theia and metals plugin by maven"); the other 49 have at least 1 comment (a reply exists, but none was marked as the answer) | counts shown on the rows |

### The 10 most recent unanswered discussions (all Q&A; list sorted by date created, newest first)

| # | Title | Category | Author | Created | Comments |
|---|---|---|---|---|---|
| 1 | How to use a custom version of Metals in VS Code | Q&A | ldokduy20 | Apr 19, 2026 | 2 |
| 2 | How to investigate when importing a symbol doesn't work. | Q&A | tanin47 | Apr 3, 2026 | 1 |
| 3 | metals-mcp --client windsurf? | Q&A | pellekrogholt | Mar 4, 2026 | 1 |
| 4 | Metals MCP Resources vs Tools | Q&A | ckipp01 | Jul 25, 2025 | 3 |
| 5 | Way to setup proper workspace for apache spark project? | Q&A | ktk1012 | Jun 10, 2025 | 1 |
| 6 | Does Metals support including a dependency directly from a git repo? | Q&A | tanin47 | May 24, 2025 | 1 |
| 7 | `inspect` MCP tool for external dependencies | Q&A | jpetuchovas | May 23, 2025 | 5 |
| 8 | Is it possible to force metals to use bazel? | Q&A | abrassel | Mar 15, 2025 | 1 |
| 9 | Can I get the `initialize_params.json` of the deployed version? | Q&A | jinulee-v | Mar 1, 2025 | 1 |
| 10 | metals-emacs apparently caches information about projects I would like to forget. | Q&A | frgomes | Nov 21, 2024 | 1 |

(The row numbers are positions in the filtered list, not discussion numbers. Row 11 of the same list is "can't create connection to server", Nov 9, 2024, closed, 0 comments.) Row 4 was opened by ckipp01 and reads as a design question about MCP resources versus tools rather than a support request.

## 8. Method notes and limits

- Only WebFetch on github.com/scalameta/metals pages was used (issue/PR/discussion/label list pages and issue/PR pages). No GitHub MCP, gh, curl or API calls; nothing was posted, reacted to or changed. No instructions were found embedded in the fetched pages (nothing to ignore).
- WebFetch returns a model-written reading of each page, not the raw HTML. I therefore cross-checked what could be cross-checked: the label tally built from all 252 open-issue rows matched 14 direct `label:` searches exactly (bug, improvement, upstream-fix-needed, Scala 3, presentation-compiler, metals-v2, BSP, investigation needed, java support, tech debt, documentation, spree, good first issue, needs more information); the "no comment count shown" reading matched `comments:0` (61 = 61); draft/review filters add up (13 drafts; 0 + 8 + 23 = 31 PRs).
- Known tool oddities: the issue list rows show no closed count; label pages show no per-label counts; the `base:main` PR filter returned all 31 PRs (prefix-like matching) and `-base:main` returned nothing, even though two PR pages show base `main-v2`; `review:required` returned 16 PRs and left out 7 PRs that `review:none` includes (reason not visible), so I did not use it. Timestamps (times of day) are not shown, so all response times are in calendar days.
- "Maintainer" is my judgement from visible behaviour plus badges (see section 5). GitHub shows tgodzik as "Contributor".
- Comment counts in list rows may include bot comments (CodeRabbit appears on PRs, github-actions on issues).
- Dates are in the 2026 timeline of the pages (today = 2026-10-18).
- Working files, not kept: the 252 transcribed open-issue rows (`open_issues_F.psv`), `pr_table.md`, and the tally and statistics scripts. They lived in the build session's scratch folder.
