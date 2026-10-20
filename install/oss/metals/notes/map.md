# Architecture map (my words)

Fill one row per area AFTER the explain-back for that area passes. Until then, the row says "not explained yet".
Sources to start from: `architecture.md` and `docs/contributors/getting-started.md` in the repo, then the explainer in `explainers/`.

| Area | Entry points (path:Symbol) | How a request flows (my words, 2-4 sentences) | Tests that cover it | Risk | Verified |
|------|----------------------------|-----------------------------------------------|---------------------|------|----------|
| LSP entry and dispatch | `MetalsLanguageServer`, `WorkspaceLspService`, `ProjectMetalsLspService`, `FallbackMetalsLspService` | not explained yet | | high | |
| Build server / BSP | `BspConnector`, `BuildServerConnection`, `ConnectionProvider`, `Compilations` | not explained yet (explanation debt: #8465, #8529, #8874) | `BillLspSuite`, `BuildServerConnectionRecoverySuite` | high | |
| Scala 2 presentation compiler | `Compilers`, `mtags/src/main/scala-2/.../pc/MetalsGlobal`, `CompletionProvider` | not explained yet (explanation debt: #8464, #8489, #8504, #8514) | `tests/cross` | medium | |
| Debug and run (DAP) | `metals/debug/DebugProvider`, `DebugProxy` | | `DebugProtocolSuite`, `tests/unit/.../debug` | medium | |
| Scaladoc and docstrings | `mtags/.../docstrings`, `ScaladocDefinitionProvider` | | `JavadocSuite`, `WikiLinkSuite` | low-medium | |
| New files, rename | `newScalaFile/NewFileProvider`, `rename/RenameProvider` | | `NewFileLspSuite`, `RenameLspSuite` | low-medium | |
| Indexing (mtags) | `mtags/Mtags`, `ScalaToplevelMtags`, `JavacMtags` | not explained yet | `MtagsSuite`, `ScalaToplevelSuite` | medium-high (performance goal) | |
| MCP server | `metals/mcp/MetalsMcpServer`, `MetalsMcpTools` | not explained yet | `tests/unit/.../mcp` | medium | |
| PC interfaces | `mtags-interfaces` (binary API, checked by MiMa) | | `interfaces/mimaReportBinaryIssues` | high | |
| Shared PC utils | `mtags-shared` (sources copied into scala/scala3) | | | high (cross-repo) | |
