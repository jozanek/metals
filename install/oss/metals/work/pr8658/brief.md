# pr8658: finish "feat: make scaladoc/javadoc wiki links navigable in hover and go-to-definition"
Created: 2026-10-20 · Upstream: main @ c631ca0f · Target: main · Area: Scaladoc (L1: direction not settled) · Depends on: pr8793.

## Facts (verified 2026-10-20)
- Open since 2026-07-08 (104 days). 27 files, +6,649/-174: about 4,000 test lines (`HoverLspSuite` +2,814) and about 2,600 production lines (`ScaladocDefinitionProvider` +1,095/-115; new `ScaladocImportScope`, `MetalsSymbolLink`, `DocScope`).
- It conflicts with current `main` only in `project/TestGroups.scala` (a list merge).
- It adds a user-visible server command, `goto-scaladoc-link`: hover renders each wiki link as a link that runs it, and it resolves the link on click "so that building the hover stays cheap (#3383)". The docs are generated from `ServerCommands`, so the docs gate will run.
- tgodzik's two comments from 2026-07-08 are still unanswered:
  1. "I was thinking about this feature previously and I hoped we could just make the links become `go to definition` links for VS Code"
  2. "I wonder if we could reuse ... ScaladocDefinitionProvider.scala here (this might need some fixes)"
  (His third comment, the split request, you answered with #8676 and #8793.)

## Predictions (write before you read the steps)
1. Which of his two comments does the PR already satisfy, and how would you show it in one sentence?
2. What does a client without command links (Neovim, Emacs) show for a hover link?
3. Which part of the 2,600 production lines is he most likely to ask you to drop or defer?

## Steps
1. Now: post ONE reply that answers both comments and proposes the rest of the split (draft below). This is a direction question, so ask it before more code (S3).
2. After pr8793 merges: merge `main` into the branch (resolve `TestGroups.scala`), then open the split PRs in the agreed order. Each stays under about 10 files. Cut the hover tests to one case per link shape.
3. Each split PR runs the full loop (S4-S6). Close #8658 itself only when the last part is open, with a link to each part.

## Draft reply (rewrite in your words: you can explain this area, so the placeholders are yours to fill)
Sorry for the long silence on your two questions from July.

1. Go-to-definition links: the hover now renders each wiki link as a link that runs a new `goto-scaladoc-link` command. The command resolves the link on click, so building the hover stays cheap (#3383). In clients without command links, <what they show>.

2. `ScaladocDefinitionProvider`: the PR builds on it, and most of the new resolution code lives there. #8793 moves the owner-resolution fix into it first.

Proposal: after #8793 merges, I split the rest into three PRs, in this order:
1. <the scope and indexing model>
2. <go to definition on wiki links in comments>
3. <the hover links and the new command>

Does that order work for you?

*- Claude (on behalf of jozanek)*   <!-- delete this line if you rewrite the text in your own words -->

## What these checks miss
Whether he still wants the feature at all after 104 days. If the answer is "not now", the split PRs wait, and your notes keep the design.
