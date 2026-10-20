# How things are usually done in Metals

Process facts only. Each line has a source. Re-verify when the source file changes.

## Commits and PRs
- Conventional commits: `<type>[scope]: <description>`; recent titles use `fix:`, `bugfix:`, `improvement:`, `docs:`, `test:`, `chore:`, `refactor:`. Source: `docs/contributors/getting-started.md` (Commit messages); `git log`. (verified 2026-10-18 @ 8c095fe5)
- Ideally one commit per PR, with title and body equal to the PR's. Several commits are fine if each is self-contained and revertable. Source: getting-started.md. (verified 2026-10-18 @ 8c095fe5)
- Agents create new commits instead of amending. Source: `AGENTS.md` (Git), in the file since #8275 (2026-03-24). The org guide (2026-09-18) says the opposite (force-push rewritten branches), and also says a repo file may override it: see open question Q-COMMITS. (verified 2026-10-18 @ 8c095fe5)
- No PR template, no CODEOWNERS file. CodeRabbit reviews every PR to `main` and `main-v2` automatically. Source: `.github/`, `.coderabbit.yaml`. (verified 2026-10-18 @ 8c095fe5)

## Before committing
- Format changed Scala files: Metals MCP `format-file`, else `./bin/scalafmt`. CI runs `./bin/scalafmt --test`. Source: `AGENTS.md`, `.github/workflows/ci.yml`. (verified 2026-10-18 @ 8c095fe5)
- Run `sbt --client scalafixAll`. CI runs `sbt scalafixCheck docs/docusaurusCreateSite`. Source: same. (verified 2026-10-18 @ 8c095fe5)
- sbt's `onLoad` writes `.git/hooks/pre-push`, which runs `bin/scalafmt --diff --diff-branch main`. Source: `build.sbt` (Global / onLoad). (verified 2026-10-18 @ 8c095fe5)

## Tests
- Run one test: `sbt --client <project>/testOnly <Suite> -- "*<test-name>*"`. The filter is an MUnit glob; a bare name matches nothing (my own fix, #8862). Source: getting-started.md, `AGENTS.md`. (verified 2026-10-18 @ 8c095fe5)
- Test names are kebab-case without spaces. Source: `AGENTS.md`. (verified 2026-10-18 @ 8c095fe5)
- A new suite in `tests/unit` must be added to `project/TestGroups.scala`; otherwise the build only warns and runs it in shard 1. Source: `build.sbt` (isInTestShard). (verified 2026-10-18 @ 8c095fe5)
- Prefer `tests/unit` for LSP features, `tests/cross` for Scala 2 PC features, `tests/slow` only for build-tool integration. Scala 3 PC tests live in scala/scala3. Source: getting-started.md (Tests). (verified 2026-10-18 @ 8c095fe5)

## Scala style (from AGENTS.md, binding on agent-written commits)
- No `.iterator` unless necessary; use collection methods directly.
- Prefer for-comprehensions over `map`/`flatMap` chains longer than one line.
- No `.toList` unless necessary. Never use non-local returns.
(verified 2026-10-18 @ 8c095fe5)
