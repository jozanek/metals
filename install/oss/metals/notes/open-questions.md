# Open questions

Status: searching -> ready-to-ask -> asked (link) -> answered (link). Ask only after the escalation ladder (CLAUDE.md, "Escalation").

| ID | Question | Why it matters | What I checked | Status |
|----|----------|----------------|----------------|--------|
| Q-COMMITS | Review rounds: new commits (Metals AGENTS.md) or a rewritten, force-pushed branch (org CONTRIBUTING.md)? | Wrong choice annoys the reviewer every round | The Metals line dates from #8275 (2026-03-24), before the org guide (2026-09-18). It still wins: the org guide says a repo file "can possibly override or customize" its rules. Maintainers squash-merge, so history is moot. | decided for now: new commits |
| Q-PROOF | Org AGENTS.md wants a bug fix as prep, tests and fix commits; Metals getting-started.md says "Ideally, each PR would only have one commit". | Commit shape every PR | getting-started.md also allows several self-contained commits, which the proof shape is. | decided for now: proof shape; ask only if a reviewer objects |
| Q-MSG | Org: write a commit body only when the reason is not obvious; Metals: "over-communicate in your commit messages. Be thorough." | Message style | Squash merges copy the PR description into the commit, so the PR body carries the explanation. | decided for now: short commits, a complete PR body |
| D-ORGSTYLE | Deviation in practice, not in policy: the org rules on 50-character subjects and `/* */` block comments are not enforced in Metals review. #8874 (opened 2026-09-22, after the org guide) merged with a 67-character subject and multi-line `//` comments. | Lint noise vs policy | lint-change.py warns on both, because the org policy binds agent-written commits and you asked to follow the written policy. | relax only if a maintainer says Metals overrides it |
| Q-ATTR | "One agent attribution": one per commit message and one per PR body, or one in total? | Policy compliance | Org CONTRIBUTING.md, "Contributing with agents" | searching |
| Q-SIG | Do I sign replies that an agent drafted and I posted unchanged? | Disclosure rule covers replies "an agent posts on your behalf" | Org CONTRIBUTING.md | decided for now: sign them; write my own words where I can |
| Q-BRANCH | For a bug present on both branches: PR to `main` and let maintainers forward-port, or a PR per branch? | Wasted work or wasted review | git log shows forward ports by tgodzik (#8930) | searching |
| Q-MBT | What does "MBT" stand for in main-v2, and which code is it? | Glossary | main-v2 commit titles | searching |
