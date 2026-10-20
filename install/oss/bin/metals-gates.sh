#!/usr/bin/env bash
# Local gates for a scalameta/metals change. Mirrors the CI jobs in .github/workflows/ci.yml
# that the changed paths can break. Costs no model tokens.
#
# Usage (from inside the Metals clone):
#   metals-gates.sh [--base upstream/main] [--tests "tests.FooSuite tests.BarLspSuite"]
#                   [--run-tests] [--heavy] [--dry-run] [--pr-body FILE]
#
#   --tests      extra unit suites that the change could break (see notes/map.md)
#   --run-tests  run every test gate with sbt. Without it: up to 5 unit suites are listed
#                for the Metals MCP `test` tool (Metals AGENTS.md: tests go through MCP).
#                MCP `test` runs one class per call, so more than 5 suites, and module-wide
#                runs (cross/test, javapc/test), run with sbt: AGENTS.md allows sbt for
#                what the MCP tools cannot do.
#   --heavy      also run the slow jobs here (+cross/test, slow build-tool suites,
#                sbt-metals/scripted). Without it they are listed for a cloud session.
#   --dry-run    print the plan, run nothing
#
# Always run with sbt, because MCP has no equivalent: scalafmt --test, scalafixCheck, the
# docs build, MiMa. Before each commit, also run `sbt --client scalafixAll` (AGENTS.md).
# Output: a summary table at the end. Paste it into the brief's evidence log.
set -uo pipefail

BASE="upstream/main"; TESTS=""; RUN_TESTS=0; HEAVY=0; DRY=0; PR_BODY=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --base) BASE="$2"; shift 2 ;;
    --tests) TESTS="$2"; shift 2 ;;
    --run-tests) RUN_TESTS=1; shift ;;
    --heavy) HEAVY=1; shift ;;
    --dry-run) DRY=1; shift ;;
    --pr-body) PR_BODY="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(git rev-parse --show-toplevel)" || exit 2
cd "$ROOT" || exit 2
[[ -f build.sbt && -d mtags ]] || { echo "not a Metals checkout: $ROOT" >&2; exit 2; }
git rev-parse --verify --quiet "$BASE" >/dev/null || { echo "base ref $BASE not found (git fetch upstream?)" >&2; exit 2; }

CHANGED="$( { git diff --name-only "$BASE"...HEAD; git diff --name-only; git diff --name-only --cached; } | sort -u)"
if [[ -z "$CHANGED" ]]; then
  echo "No changes against $BASE."
  if [[ $DRY -eq 1 ]]; then
    cat <<'PLAN'
Plan for any change:
  always:            scalafmt --test (changed files), lint-change.py, sbt scalafixCheck
  docs/, metals-docs/, UserConfiguration, ServerCommands, ClientCommands, Configs: docs build
  mtags-interfaces/: MiMa
  mtags/, mtags-shared/, tests/cross/: cross/test (sbt: module-wide), +cross/test (heavy)
  mtags-java/, tests/javapc/: javapc/test (sbt: module-wide)
  edited suites and subclasses of edited test base classes: up to 5 unit suites via MCP, more via sbt; slow ones (heavy)
  builds/ for a build tool, tests/slow/<tool>: slow suites for that tool (heavy)
  sbt-metals/: sbt-metals/scripted (heavy)
PLAN
  fi
  exit 0
fi
has() { grep -qE "$1" <<<"$CHANGED"; }
CLASS_RE='^[[:space:]]*((final|abstract|sealed|private|protected|case)[[:space:]]+)*(class|trait)[[:space:]]+([A-Za-z0-9_]+)'

declare -a NAMES=() RESULTS=() SECS=() LATER=() MCP=()
step() { # step <name> <command...>
  local name="$1"; shift
  echo; echo "=== $name"; echo "+ $*"
  if [[ $DRY -eq 1 ]]; then NAMES+=("$name"); RESULTS+=("dry-run"); SECS+=("-"); return; fi
  local t0=$SECONDS
  if "$@"; then RESULTS+=("PASS"); else RESULTS+=("FAIL"); fi
  NAMES+=("$name"); SECS+=("$((SECONDS - t0))")
}
testgate() { # testgate <name> <mcp hint, or "" if MCP cannot run it> <sbt command...>
  local name="$1" hint="$2"; shift 2
  if [[ $RUN_TESTS -eq 1 || -z "$hint" ]]; then step "$name" "$@"; else MCP+=("$name: $hint"); fi
}
heavy() { # heavy <name> <command...>
  if [[ $HEAVY -eq 1 ]]; then step "$@"; else local n="$1"; shift; LATER+=("$n: $*"); fi
}
classes_in() { # fully qualified Suite/base classes declared in a file at HEAD (or the worktree)
  local f="$1" pkg
  pkg="$(sed -nE 's/^package[[:space:]]+([A-Za-z0-9_.]+).*/\1/p' "$f" | head -1)"
  sed -nE "s/${CLASS_RE}.*/\4/p" "$f" | while read -r c; do echo "${pkg:+$pkg.}$c"; done
}

echo "Changed files against $BASE:"; sed 's/^/  /' <<<"$CHANGED"

# 1. CI job "Formatting": ./bin/scalafmt --test (here: only the changed files).
step "scalafmt (changed files)" ./bin/scalafmt --test --diff-branch "$BASE"

# 2. Shard registration, commit and PR-text rules, risky paths (no sbt needed).
LINT=(python3 -I "$HERE/lint-change.py" --repo "$ROOT" --base "$BASE" --head HEAD)
[[ -n "$PR_BODY" ]] && LINT+=(--pr-body "$PR_BODY")
step "lint-change (policy rules)" "${LINT[@]}"

# 3. CI job "Scalafix and docs", first half. Compiles everything with SemanticDB.
step "scalafixCheck" sbt --client scalafixCheck

# 4. The docs are generated from these sources, so build them when they change.
if has '^(docs/|metals-docs/|website/(docs|sidebars|siteConfig))|/(UserConfiguration|UserConfigurationOption|ServerCommands|ClientCommands|BaseCommand|Configs)\.scala$'; then
  step "docs build" sbt --client docs/docusaurusCreateSite
fi

# 5. CI job "MiMa": binary compatibility of the presentation compiler API.
if has '^mtags-interfaces/'; then
  step "MiMa (mtags-interfaces)" sbt --client interfaces/mimaReportBinaryIssues
fi

# 6. CI job "Scala cross tests" runs +cross/test. Locally: the default Scala 2 version.
if has '^(mtags/|mtags-shared/|tests/cross/)'; then
  testgate "cross/test (default Scala 2)" "" sbt --client cross/test
  heavy "+cross/test (all Scala versions)" sbt --client +cross/test
fi

# 7. CI job "Scala javapc tests".
if has '^(mtags-java/|tests/javapc/)'; then
  testgate "javapc/test" "" sbt --client javapc/test
fi

# 8. Suites the change can break: edited suites, every concrete subclass of an edited test
#    base class (transitively), and --tests. Slow ones go to the heavy list.
SEL="$(python3 -I "$HERE/test-selection.py" --repo "$ROOT" $CHANGED)"
SUITES="$(sed -n 's/^unit: //p' <<<"$SEL") $TESTS"
SLOW="$(sed -n 's/^slow: //p' <<<"$SEL")"
SUITES="$(tr ' ' '\n' <<<"$SUITES" | sed '/^$/d' | sort -u | tr '\n' ' ')"
n_suites="$(wc -w <<<"$SUITES")"
if [[ $n_suites -gt 5 ]]; then
  testgate "unit suites ($n_suites, too many for one-class MCP calls)" "" sbt --client "unit/testOnly $SUITES"
elif [[ $n_suites -gt 0 ]]; then
  testgate "unit suites: $SUITES" "MCP test, one call per suite" sbt --client "unit/testOnly $SUITES"
elif has '^tests/unit/src/main/'; then
  echo; echo "=== unit suites: a test base class changed but no concrete subclass was found. Pass --tests."
else
  echo; echo "=== unit suites: none detected. Pass --tests with the suites that cover the change (notes/map.md)."
fi
[[ -n "${SLOW// /}" ]] && heavy "slow suites: $SLOW" sbt --client "slow/testOnly $SLOW"

# 9. Build-tool integrations: CI runs slow/testOnly per tool. Heavy, so cloud by default.
for pair in "Sbt:sbt" "Mill:mill" "Gradle:gradle" "Maven:maven" "Bazel:bazel" "ScalaCli:scalacli"; do
  tool="${pair%%:*}"; pkg="${pair##*:}"
  if has "/builds/.*${tool}|tests/slow/src/test/scala/tests/${pkg}/"; then
    heavy "slow ${pkg} suites" sbt --client "slow/testOnly -- tests.${pkg}.*"
  fi
done
if has '^sbt-metals/'; then heavy "sbt-metals/scripted" sbt --client sbt-metals/scripted; fi

# Summary (paste into the evidence log).
echo; echo "| gate | result | seconds |"; echo "|------|--------|---------|"
fail=0
for i in "${!NAMES[@]}"; do
  echo "| ${NAMES[$i]} | ${RESULTS[$i]} | ${SECS[$i]} |"
  [[ "${RESULTS[$i]}" == "FAIL" ]] && fail=1
done
if [[ ${#MCP[@]} -gt 0 ]]; then
  echo; echo "Test gates to run with the Metals MCP test tool (or pass --run-tests):"
  printf '  - %s\n' "${MCP[@]}"
fi
if [[ ${#LATER[@]} -gt 0 ]]; then
  echo; echo "Not run locally (use --heavy, or a cloud session with templates/cloud-preamble.md):"
  printf '  - %s\n' "${LATER[@]}"
fi
echo; echo "Not covered by any local gate: Windows and macOS runners, JDK 17 vs 25 differences, other shards of unit/test."
exit $fail
