# Test Coverage Analysis & Improvement Proposals

_Analysis date: 2026-08-28. Scope: `metals`, `mtags`, `mtags-shared`, `mtags-java`,
`metals-mcp` and the `tests/` tree._

## Summary

Metals has a large and mature test suite — **1,123 test `.scala` files** and
**~433 test suite classes** covering roughly **110k lines** of main source. Most
user-facing LSP features (completion, hover, definition, references, rename,
folding, inlay hints, code actions, DAP, worksheets) are well exercised.

The coverage is, however, **heavily weighted toward slow end-to-end integration
suites**: ~165 suites spin up a full LSP/DAP server (`BaseLspSuite`,
`BaseDapSuite`, …) while only ~82 are lightweight `FunSuite`/`BaseSuite` unit
tests. As a result, a layer of **pure-logic helpers and provider internals is
only ever tested transitively**, if at all. When one of these regresses, the
failure surfaces as a flaky/hard-to-localize integration failure rather than a
fast, precise unit failure — and several of them have **no coverage of any
kind**.

There is also **no automated line-coverage measurement** (no scoverage/jacoco in
`build.sbt`, `project/`, or CI), so gaps are invisible until something breaks in
the field. Coverage is currently assessed only by proxy (suite counts / naming).

The proposals below prioritize (a) untested pure-logic units that are cheap,
deterministic wins, and (b) high-churn / high-risk feature internals.

---

## Well-covered areas (don't over-invest here)

- **DAP / debugging** — `BreakpointDapSuite`, `StepDapSuite`, `StackFrameDapSuite`,
  `EvaluationDapSuite`, `DebugDiscoverySuite`, `MessageIdAdapterSuite`, plus
  sbt/mill/scala-cli cross variants.
- **MCP server** — `McpServerLspSuite`, `McpQueryLspSuite`, `McpRunTestSuite`,
  `McpCompileToolsLspSuite`, `McpFormatLspSuite`, `McpConfigSuite`,
  `McpPortConfigSuite`, plus stdio suites.
- **Code actions** — nearly every action has a dedicated LSP suite (extract
  method/value, inline, organize-imports, implement-abstract, convert-to-named-args,
  rewrite braces/parens, …).
- **Scala toplevel / mtags indexing** — `ScalaToplevelSuite`, `ToplevelSuite`,
  `MtagsSuite`, `JavaToplevelSuite`, `SemanticdbSuite`.
- **Doctor** — `ProblemResolverSuite`, `ReportsSuite`.
- **sbt & Mill build integration** — ~12 suites each.

---

## Priority gaps

### P1 — Pure-logic units with zero direct tests (cheap, high-value)

These are small, deterministic, and currently only tested transitively (or not at
all). Fast unit suites here would pin down behavior and localize regressions.

| Source | LOC | What breaks if it regresses |
|---|---|---|
| `parsing/TokenOps.scala`, `parsing/MatchingToken.scala`, `parsing/BinarySearch.scala` | 77 / 11 / 43 | Token classification & position lookup underpin edit application, folding, and every text-edit-producing feature. No direct tests. |
| `mtags/OverloadDisambiguator.scala` | — | Disambiguates overloaded method symbols during indexing; errors silently corrupt goto-definition/references for overloads. |
| `mtags-shared/…/metals/StringBloomFilter.scala`, `ConcatSequence.scala`, `PrefixCharSequence.scala`, `ZeroCopySubSequence.scala` | — | Low-level string/bloom primitives backing classpath symbol pre-filtering; regressions cause missing or slow symbol search. |
| `mtags-shared/…/pc/CompletionFuzzy.scala`, `MemberOrdering.scala` | — | Completion matching/ranking; only tested through full PC completion suites. |
| `metals/PatchMatcher.scala`, `StringCase.scala`, `ManifestJar.scala`, `Fingerprints.scala`, `JvmSignatures.scala` | 23 / 29 / 61 / 71 / 47 | Assorted core utilities with no direct coverage. |

### P2 — Feature internals covered by only one broad integration suite

A single end-to-end suite can pass while internal branches rot. These deserve
focused suites at the unit or targeted-LSP level.

- **Test discovery finders** — `testProvider/frameworks/`: `MunitTestFinder`,
  `WeaverCatsEffectTestFinder`, `AnnotationTestFinder`, `JunitTestFinder`,
  `TestNGTestFinder` have **no dedicated finder suites** (only `ScalatestFinderSuite`
  and `ZioTestFinderSuite` exist). `ScalatestTestFinder`/`ZioTestFinder` are also
  among the highest-churn files in the last year. Broken discovery silently drops
  tests from the Test Explorer and run/debug lenses.
- **Tree View (`tvp/`)** — `ClasspathTreeView.scala` and `IndexedSymbols.scala`
  have zero direct references; the whole package rests on a single
  `TreeViewLspSuite`.
- **On-type formatting** — `formatting/InterpolateStringContext.scala` has zero
  references, while every sibling formatter (`MultilineString`, `IndentOnPaste`,
  `OnTypeFormatting`, `RangeFormatting`) is well covered.
- **scala-cli internals** — `scalacli/DependencyConverter.scala` and
  `ScalaCliServers.scala` have no direct tests; only exercised via end-to-end
  `ScalaCliSuite` / a code-action suite.
- **BSP config / reload** — `builds/BspConfigGenerator.scala`,
  `BSPErrorHandler.scala`, `VersionRecommendation.scala`, `WorkspaceReload.scala`
  have no direct tests.
- **Multi-root workspace** — `metals/WorkspaceFolders.scala` (153 LOC managing
  multi-root folders) has no direct coverage.
- **Docstring rendering** — only `MarkdownGenerator` is tested (`JavadocSuite`);
  `docstrings/printers/PlaintextGenerator.scala`, `ScalaDocPrinter.scala`, and
  `docstrings/HtmlConverter.scala` (plaintext/HTML hover) are untested.
- **Java class-file indexing** — source-based `JavaToplevelMtags` is covered by
  `JavaToplevelSuite`, but the `.class` path in `mtags/JavacMtags.scala` is not.

### P3 — Build tools with thin integration coverage

`sbt` and `mill` have ~12 suites each; **Gradle (2), Maven (3), Bazel (3),
Bloop (2)** are comparatively thin. These are the integrations most likely to
break on external-tool version bumps and the hardest for users to work around.

### P4 — Process / tooling

- **No line-coverage measurement.** Consider a periodic (not per-PR, to avoid the
  presentation-compiler-plugin friction scoverage causes) coverage job, or at
  least a one-off scoverage run to produce a real gap map for `metals` and
  `mtags`.
- **Rebalance toward fast unit tests.** Many helpers above only need plain
  `FunSuite` tests; adding them shortens the feedback loop and reduces reliance on
  the slow shard that dominates CI time.

---

## Recommended concrete test additions

Ordered by value/effort:

1. `TokenOpsSuite` / `BinarySearchSuite` — unit-test token classification and
   position search over hand-written inputs (`parsing/`).
2. `TestFinderSuite`s for `MunitTestFinder`, `WeaverCatsEffectTestFinder`,
   `AnnotationTestFinder` — assert discovered test nodes for representative sources
   (mirror `ScalatestFinderSuite`).
3. `OverloadDisambiguatorSuite` — feed overloaded method sets, assert stable
   disambiguated symbols.
4. `DependencyConverterSuite` — round-trip dependency syntax across
   Mill/sbt/scala-cli directives (`scalacli/DependencyConverter.scala`).
5. `StringBloomFilterSuite` — membership true-positives and a false-negative-free
   guarantee over a large symbol set.
6. `InterpolateStringContext` on-type formatting suite — typing `${` inside a plain
   string auto-adds the `s` prefix.
7. Plaintext/`ScalaDocPrinter` docstring suite mirroring `JavadocSuite`.
8. `BspConfigGeneratorSuite` — config generation + `BSPErrorHandler` propagation.
9. TreeView suite exercising `tvp/ClasspathTreeView.scala` + `IndexedSymbols.scala`.
10. Thicken Gradle/Maven/Bazel LSP suites (compile, diagnostics, goto-definition on
    a representative project).

---

_Methodology: cross-referenced main source files/packages against test suite
names and their contents (grep by class/feature name), git churn over the last 12
months, and the CI/build configuration. "Zero references" means no test file
mentions the class by name; some such classes are still exercised transitively
through integration suites — those are called out as P2 rather than "untested"._
