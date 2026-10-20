# Decisions and their rationale (project-level)

| Date seen | Decision | Rationale (as stated) | Source |
|-----------|----------|-----------------------|--------|
| 2026-10-18 | The Scala 3 presentation compiler lives in scala/scala3, not in Metals. Scala 3 completion/hover bugs usually belong there. | Compiler-version coupling | `docs/contributors/getting-started.md` |
| 2026-10-18 | `mtags-shared` sources are copied into the Scala 3 compiler repo. A change there reaches scala/scala3. | Scala 3 compiler cannot depend on Scala projects | getting-started.md |
| 2026-10-18 | Metals 2 is developed on `main-v2` (milestones, `v2.0.0-M16` in July 2026). `main` carries 1.6.x releases; maintainers forward-port fixes (for example #8930). | Monorepo scale, better behaviour on non-compiling code | `website/blog/2026-01-21-osmium.md`, `2026-07-23-osmium.md`, git log |
| 2026-10-18 | Feature requests go to scalameta/metals-feature-requests; questions go to GitHub Discussions. | Issue tracker is for bugs | `.github/ISSUE_TEMPLATE/config.yml` |
| 2026-10-18 | Issues labelled "needs more information" close after 30 days without new information. | Stale-issue hygiene | `.github/workflows/close-inactive-needs-more-info-issues.yml` |
| 2026-09-18 | scalameta org rules for every change, with a section for agents. | Review quality | scalameta/.github `CONTRIBUTING.md`, `AGENTS.md` |
