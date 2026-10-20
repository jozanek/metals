<!--
PR description template for scalameta/metals. Fill every line. Delete these comments.
Rules (scalameta org CONTRIBUTING.md + AGENTS.md, Metals getting-started.md):
- One line per paragraph. GitHub keeps every newline, so never hard-wrap.
- Say what, why and how far it reaches. Never narrate the diff.
- Plain English: one idea per sentence, 20 words at most, active voice, name the thing.
- Title: conventional-commit form, like recent Metals titles ("fix: ...", "improvement: ...", "bugfix: ...", "docs: ...", "test: ...").
- No agent attribution here. The commit carries the single Co-authored-by trailer (see checklist P-ATTR).
-->
Previously, <what the user saw, or what the code did>. Now, <what changes>.

Fixes #<issue>   <!-- or "Part of #N" when it fixes only some cases; omit if no issue -->

Reach: <modules, features, build tools and Scala versions this affects>. It does not change <the closest thing a reviewer might suspect>.

Tests: <suite names>. Ran locally: <exact commands, or "MCP test: <suites>">. Not run locally: <for example Windows, Mill, +cross>.   <!-- not the list of investigated cases: org AGENTS.md says the tests commit shows them -->

Look first at: <path:Symbol>, because <the one decision that needs judgement, and the alternative I rejected>.

Risk and undo: <what could break and how a user would notice>. Undo: revert this commit; no migration.
