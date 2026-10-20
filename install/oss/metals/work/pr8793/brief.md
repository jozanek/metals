# pr8793: finish "fix: resolve scaladoc links against the documented member's SemanticDB owner"
Created: 2026-10-20 · Upstream: main @ c631ca0f · Target: main · Area: Scaladoc (L1) · Do this one first: #8658 shrinks after it merges.

## Facts (verified 2026-10-20)
- Open since 2026-08-13. No human review in 68 days. Your last push: 2026-09-02.
- 3 files, +373/-54 (`DefinitionProvider`, `ScaladocDefinitionProvider`, `DefinitionLspSuite`). It merges cleanly into current `main` (58 commits behind).
- One open CodeRabbit correctness note (2026-09-01): "Restore the `Defn.EnumCase` owner mapping": a parameterized enum case such as `Mix(r: Int)` would keep the enclosing enum as its owner. No reply, no later fix. `EnumCase` does not appear in `ScaladocDefinitionProvider` on `main` or at your head (2a1ad734), so only a test can say if the claim holds.

## Predictions (write before you run the test)
1. Does a scaladoc link to a parameterized enum case resolve to the case or to the enum today?
2. If it is wrong, where does the owner get decided?

## Steps
1. You: add a `DefinitionLspSuite` case in a Scala 3 workspace (the suite already has one) with `enum Color { case Red; case Mix(r: Int) }` and a scaladoc link `[[Color.Mix]]`. Run it with Metals MCP `test`.
2. If it resolves to the enum: tests commit (assert today's result), then the fix commit (flip it). If it resolves to the case: no code change.
3. Gates: `~/oss/bin/metals-gates.sh --base upstream/main` (runs `DefinitionLspSuite` via MCP), then `oss-reviewer` (diff-only).
4. You push (new commits), then post the ping below. One ping only.

## Draft ping (rewrite in your words; if you post it unchanged, keep the signature)
Gentle ping: this PR is ready for review. It is the second part of splitting #8658, after #8676. It changes 3 files and merges cleanly into current main. I checked the open CodeRabbit note about parameterized enum cases: <result, and the test that shows it>. After this PR, #8658 gets smaller, because both change `ScaladocDefinitionProvider`.

*- Claude (on behalf of jozanek)*

## What these checks miss
Other client behaviours, and Scala 2 enum-like objects. A ping cannot make the maintainer faster: if nothing happens in 14 days, do not ping again; ask once on Discord instead.
