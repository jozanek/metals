# pr8824: finish "feat(mcp): add test-repeated tool for detecting flaky tests"
Created: 2026-10-20 · Upstream: main @ c631ca0f · Target: main · Area: MCP tools (L0: a new tool needs a maintainer's OK first).

## Facts (verified 2026-10-20)
- Open since 2026-09-01 (49 days). No human activity, no reviewer requested, no linked issue.
- 4 files, +428/-15. It now conflicts with `main` in `McpTestRunner.scala`, which matejcerny changed in #8785 ("resolve test suites across modules") and #8791 ("suggest `import-build` when no build target is found").
- The tool runs a suite 1-100 times, in sequence. Your PR description lists "No cancellation or timeout" as a known limit. CodeRabbit raised the same resource risk, and a docs nit (MD040: a language tag on a fenced block).

## Predictions (write before you read the steps)
1. Will tgodzik want this as its own tool, or as an option on the existing `test` tool?
2. Which limit will he raise first: the 100-run cap, or the missing cancellation?

## Steps
1. Now: post the closed question below. Do not rebase yet: the answer may change the shape.
2. If yes: merge `main` (adopt #8785's cross-module resolution), fix the MD040 nit, then add what the answer asks for (a lower cap, cancellation, or both). Gates, `oss-reviewer`, push.
3. If no: close it with one line of thanks. Keep the idea in `notes/decisions.md`.

## Draft question (rewrite in your words; if you post it unchanged, keep the signature)
Before I update this for #8785, one question: do you want a test-repeated MCP tool in Metals?

1. Yes, as its own tool: I lower the cap from 100 runs and stop the runs when the request is cancelled.
2. Yes, but as an option on the existing `test` tool: I rework it that way.
3. No: I close it.

I recommend 1. It lets an agent confirm a flaky test before anyone files an issue. The repo marks 13 tests `.flaky` today.

*- Claude (on behalf of jozanek)*

## What these checks miss
Whether matejcerny, who now works most on the MCP tools, would rather shape it. If tgodzik points to him, ask him the same question once.
