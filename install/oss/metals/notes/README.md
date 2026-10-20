# Metals notes: how this folder works

These notes live outside the Metals repository. They cache what I learned, so no session has to re-read the codebase from zero, and they record what I got wrong so a maintainer never corrects it twice.

## Read at the start of every work item (in this order)
1. `../autonomy.md`: my level in the area I am about to touch.
2. `mistakes.md`: every active rule. Each one cost a maintainer a comment once.
3. `reviewers.md`: what the likely reviewer of this area cares about.
4. `map.md`: the rows for the area. Open the latest file in `explainers/` for that slice, if it is less than 90 days old.
5. `open-questions.md`: anything still open in this area.

## Update at the end of every work item
- `map.md`, `glossary.md`: in my own words, after the explain-back. Never paste agent text here.
- `conventions.md`, `decisions.md`, `reviewers.md`: one dated line each, with a link as evidence.
- `mistakes.md`: every maintainer correction becomes a rule (also add it to `../checklist.md`).
- `learning-log.md`: my predictions against what happened.
- `../ledger.csv`: one row for the item.

## Format rules
- Every entry ends with `(verified YYYY-MM-DD @ <short-sha>)`. The sha is the upstream commit I checked against.
- Point at code as `path:Symbol` (for example `metals/src/main/scala/scala/meta/internal/metals/Compilers.scala:Compilers`), not at line numbers. Lines move; symbols rarely do. For a permanent link, use a GitHub permalink at the sha.
- Agent-written text lives only in `explainers/`, and every explainer says so in its first line.

## Pruning (monthly, or when a note misleads me)
- An entry that is not re-verified for 90 days is stale. Re-verify it or delete it.
- An entry whose `path:Symbol` no longer resolves on upstream is stale at once.
- A rule in `mistakes.md` with no violation and no use for 6 months moves to an "archive" section, not to the bin.
