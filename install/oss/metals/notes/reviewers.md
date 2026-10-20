# Reviewers: what they care about (evidence-linked)

Source: 58 merged, 22 closed-unmerged and 3 open PRs on public pages, 2026-10-18. Inline comments were often hidden from that scrape. Refresh from `data/comments.jsonl` after `mine-reviews.sh` (rollout R1).

## tgodzik (Tomasz Godzik): the approver on `main`, and on most of `main-v2`
- Approved every sampled contributor PR except two on `main-v2` (#8620 and #8773, approved and merged by zielinsky), and merged every sampled `main` PR. (verified 2026-10-18)
- Fast first response: median 1 day on outsiders' PRs, same day on new issues. Long tails exist: "Totally forgot to finish the review before, sorry about that!" (#8737), "Finally got back to the PR, sorry about taking so long!" (#8504). One polite ping after a long silence worked (#8542).
- Asks "is this needed?" and "can it be simpler?" more than anything else (#8504, #8489, #8468, #8514, #8542, #8745).
- Wants logic in the component that owns it and reuse of existing helpers (#8745, #8658, #8864). Prefers passing objects to passing callbacks (#8874, inferred from the fix commit).
- Avoids new user settings: "I would only add the user setting if users request it" (#8542).
- Guards hot paths: indexing, `didChange`, caches (#8504, #8742).
- Wants tests of observable LSP behaviour, with expected output (`check`) (#8556, #8489, #8800). Accepted evidence-based pushback on #8556.
- Splits big PRs: "a bit terrifying to review" (#8658). Changes direction when a simpler route exists (#8745 -> #8874).
- Reconsiders old issues: "I should go over older issues and figure out if all of them make sense" (#8468).
- Merges with a few unrelated red checks; says so ("it might be unrelated, so don't worry about it", #8852).
- Ports between `main` and `main-v2` himself, in bulk (#8738); cherry-picks merged PRs (seen on #8504 and others).
- Open to LLM use: "Had a quick LLM assisted look:" (#8800); "You could try the refactor with LLMs" (#8788). PRs with Claude, Codex and Cursor trailers merged without comment on AI use.
- Approves with a bare approval or "LGTM!". Never cites CodeRabbit.
(verified 2026-10-18)

## Others
- zielinsky (Zieliński Patryk), org Member: works on `main-v2` (MBT test UI); self-merges his own PRs after review. (verified 2026-10-18)
- odisseus, Collaborator: first reviewer on several 2026 `main` PRs; approves without text. (verified 2026-10-18)
- `main-v2` regulars (jchyb, erik-snider, damiankus-vl, Myroslav, snjeza, mahib-stripe, olafurpg, iuliand): authors, not seen as approvers in the sample. (verified 2026-10-18)

## CodeRabbit (bot, every PR to `main` and `main-v2`)
- About 1-3 findings per PR. Authors almost never reply. Fixes go in silent commits; maintainers ignore it. It refuses PRs over its file limit (150-300 files), a sign of a wrong base.
- Use it as a free second reviewer: fix real findings in the next commit, decline the rest with one line only if a human might read the thread. Do not let it start an agent loop.
(verified 2026-10-18)
