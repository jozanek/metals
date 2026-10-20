#!/usr/bin/env bash
# Exact review-data miner for scalameta/metals. Uses gh with GET requests only.
# Run it on your machine (gh authenticated, ideally with the read-only token).
#
# Usage:
#   mine-reviews.sh [--repo scalameta/metals] [--me jozanek] [--out ~/oss/metals/data]
#                   [--others 50] [--closed 20] [--since 2026-01-01] [--summarize-only]
#
# Writes:
#   <out>/raw/<pr>/{pr,reviews,review_comments,issue_comments,commits,timeline}.json
#   <out>/summary.jsonl   one line per PR: timings, rounds (feedback between pushes), who commented, force-pushes
#   <out>/comments.jsonl  one line per human (non-author, non-bot) comment: the raw material
#                         for checklist rules. Feed it to the oss-scout agent, not to Opus.
# Re-running skips PRs already fetched (delete <out>/raw/<pr>/done to refetch one).
set -euo pipefail

REPO="scalameta/metals"; ME="jozanek"; OUT="$HOME/oss/metals/data"
OTHERS=50; CLOSED=20; SINCE="2026-01-01"; SUMMARIZE_ONLY=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    --me) ME="$2"; shift 2 ;;
    --out) OUT="$2"; shift 2 ;;
    --others) OTHERS="$2"; shift 2 ;;
    --closed) CLOSED="$2"; shift 2 ;;
    --since) SINCE="$2"; shift 2 ;;
    --summarize-only) SUMMARIZE_ONLY=1; shift ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done
mkdir -p "$OUT/raw"
BOTS='-author:app/dependabot -author:scala-steward -author:scalameta-bot -author:app/github-actions'

fetch() { # fetch <pr-number>
  local n="$1" d="$OUT/raw/$1"
  [[ -f "$d/done" ]] && return 0
  mkdir -p "$d"
  gh api "repos/$REPO/pulls/$n" > "$d/pr.json"
  gh api --paginate "repos/$REPO/pulls/$n/reviews" | jq -s 'add // []' > "$d/reviews.json"
  gh api --paginate "repos/$REPO/pulls/$n/comments" | jq -s 'add // []' > "$d/review_comments.json"
  gh api --paginate "repos/$REPO/issues/$n/comments" | jq -s 'add // []' > "$d/issue_comments.json"
  gh api --paginate "repos/$REPO/pulls/$n/commits" | jq -s 'add // []' > "$d/commits.json"
  gh api --paginate "repos/$REPO/issues/$n/timeline" | jq -s 'add // []' > "$d/timeline.json"
  touch "$d/done"
}

if [[ $SUMMARIZE_ONLY -eq 0 ]]; then
  gh pr list -R "$REPO" --author "$ME" --state all --limit 300 --search "created:>=$SINCE" --json number > "$OUT/list_mine.json"
  gh pr list -R "$REPO" --state merged --limit "$OTHERS" \
    --search "-author:$ME $BOTS merged:>=$SINCE" --json number > "$OUT/list_others_merged.json"
  gh pr list -R "$REPO" --state closed --limit 100 \
    --search "is:unmerged -author:$ME $BOTS" --json number | jq ".[:$CLOSED]" > "$OUT/list_others_closed.json"
  for n in $(jq -r '.[].number' "$OUT"/list_*.json | sort -un); do
    echo "fetching #$n"; fetch "$n"
  done
fi

# Summaries. A human is any user who is not the PR author and not a bot.
: > "$OUT/summary.jsonl"; : > "$OUT/comments.jsonl"
for d in "$OUT"/raw/*/; do
  [[ -f "$d/done" ]] || continue
  jq -n -c \
    --slurpfile pr "$d/pr.json" --slurpfile rv "$d/reviews.json" \
    --slurpfile rc "$d/review_comments.json" --slurpfile ic "$d/issue_comments.json" \
    --slurpfile cm "$d/commits.json" --slurpfile tl "$d/timeline.json" --arg me "$ME" '
    def bot: (.user.type // "") == "Bot" or ((.user.login // "") | endswith("[bot]"));
    def t: fromdateiso8601;
    def days($a; $b): if $a == null or $b == null then null else ((($b | t) - ($a | t)) / 86400 | . * 10 | round / 10) end;
    $pr[0] as $p | $p.user.login as $author |
    ([$rv[0][] | select((bot | not) and .user.login != $author)]) as $hrv |
    ([$rc[0][] | select((bot | not) and .user.login != $author)]) as $hrc |
    ([$ic[0][] | select((bot | not) and .user.login != $author)]) as $hic |
    ([$hrv[].submitted_at, $hrc[].created_at, $hic[].created_at] | map(select(. != null)) | sort | first) as $first |
    ([$cm[0][] | .commit.committer.date] | map(select(. != null)) | sort) as $pushes |
    ([($hrv[] | select(.state != "APPROVED" or ((.body // "") != "")) | .submitted_at), $hrc[].created_at, $hic[].created_at]
      | map(select(. != null))) as $feedback |
    # A round is human feedback between two of the author'"'"'s commits: count the distinct
    # "number of commits so far" values over all feedback times. Inline replies in one round
    # count once, unlike the raw number of COMMENTED reviews.
    ([$feedback[] | . as $t | [$pushes[] | select(. <= $t)] | length] | unique | length) as $rounds |
    {
      number: $p.number, title: $p.title, author: $author, mine: ($author == $me),
      author_association: $p.author_association, base: $p.base.ref,
      state: (if $p.merged_at then "merged" elif $p.state == "closed" then "closed" else "open" end),
      created: $p.created_at, closed: ($p.merged_at // $p.closed_at), merged_by: $p.merged_by.login,
      additions: $p.additions, deletions: $p.deletions, changed_files: $p.changed_files,
      commits: ($cm[0] | length),
      force_pushes: ([$tl[0][] | select(.event == "head_ref_force_pushed")] | length),
      days_to_first_human_response: days($p.created_at; $first),
      days_to_close: days($p.created_at; ($p.merged_at // $p.closed_at)),
      human_reviewers: ([$hrv[].user.login, $hrc[].user.login, $hic[].user.login] | unique),
      rounds: $rounds,
      human_reviews: ([$hrv[] | select(.state == "CHANGES_REQUESTED" or .state == "COMMENTED")] | length),
      changes_requested: ([$hrv[] | select(.state == "CHANGES_REQUESTED")] | length),
      human_comments: (($hrc | length) + ($hic | length)),
      coderabbit_comments: ([$rc[0][] | select(.user.login == "coderabbitai[bot]")] | length)
    }' >> "$OUT/summary.jsonl"
  jq -c --arg n "$(basename "$d")" '
    .[] | select(((.user.type // "") != "Bot") and ((.user.login // "") | endswith("[bot]") | not))
    | {pr: ($n | tonumber), who: .user.login, assoc: .author_association, at: (.created_at // .submitted_at),
       path: .path, line: (.line // .original_line), body: ((.body // "") | .[0:600])}' \
    "$d/review_comments.json" "$d/issue_comments.json" "$d/reviews.json" \
    | jq -c --slurpfile pr "$d/pr.json" 'select(.who != $pr[0].user.login and .body != "")' >> "$OUT/comments.jsonl"
done

echo "PRs: $(wc -l < "$OUT/summary.jsonl"), human comments: $(wc -l < "$OUT/comments.jsonl")"
jq -s -r '
  def med: sort | if length == 0 then null else .[(length / 2 | floor)] end;
  group_by(.mine) | .[] |
  "\(if .[0].mine then "mine  " else "others" end) n=\(length) merged=\(map(select(.state=="merged"))|length) " +
  "median days to first response=\(map(.days_to_first_human_response)|map(select(.!=null))|med) " +
  "median days to close=\(map(.days_to_close)|map(select(.!=null))|med) " +
  "median human comments=\(map(.human_comments)|med) median rounds=\(map(.rounds)|med)"' "$OUT/summary.jsonl"
