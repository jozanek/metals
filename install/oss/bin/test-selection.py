#!/usr/bin/env python3
"""Which test suites can a change break? Used by metals-gates.sh. No model tokens.

Usage: test-selection.py --repo PATH CHANGED_FILE...
Prints two lines: "unit: <fqcn> ..." and "slow: <fqcn> ...".

- An edited suite under tests/unit/src/test or tests/slow/src/test selects itself.
- An edited class or trait anywhere under tests/ selects every concrete suite that
  inherits from it, transitively (BaseLspSuite -> BaseCompletionLspSuite -> ...).
- Abstract classes and traits are never selected: they cannot run.
Inheritance is read from source text (`extends X`, `with X`), so it is approximate:
it misses inheritance through type aliases and generated code.
"""
import argparse
import os
import re
import subprocess
from collections import defaultdict

# The header runs to the body's "{" (or a blank line), so multi-line constructor parameter
# lists before `extends` are read too.
DECL = re.compile(
    r"(?:^|\n)[ \t]*((?:(?:final|abstract|sealed|private|protected|case|open)[ \t]+)*)(class|trait|object)[ \t]+(\w+)"
    r"(.{0,3000}?)(?=\{|\n[ \t]*\n|\Z)",
    re.DOTALL,
)
PARENT = re.compile(r"\b(?:extends|with)\s+([A-Z]\w*)")


def scala_files(repo):
    out = subprocess.run(["git", "-C", repo, "ls-files", "tests/*.scala"], capture_output=True, text=True, check=True)
    return [f for f in out.stdout.splitlines() if "/src/" in f]


def declarations(repo, path):
    try:
        src = open(os.path.join(repo, path), encoding="utf-8", errors="replace").read()
    except OSError:
        return "", []
    pkg = re.search(r"^package\s+([\w.]+)", src, re.MULTILINE)
    decls = []
    for mods, kind, name, tail in DECL.findall(src):
        decls.append({"name": name, "kind": kind, "abstract": "abstract" in mods or kind == "trait",
                      "parents": PARENT.findall(tail), "fqcn": f"{pkg.group(1)}.{name}" if pkg else name, "path": path})
    return src, decls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("changed", nargs="*")
    a = ap.parse_args()
    all_decls, children = [], defaultdict(list)
    for f in scala_files(a.repo):
        for d in declarations(a.repo, f)[1]:
            all_decls.append(d)
            for p in d["parents"]:
                children[p].append(d)
    selected, frontier = {}, []
    for f in a.changed:
        if not (f.startswith("tests/") and f.endswith(".scala")):
            continue
        for d in declarations(a.repo, f)[1]:
            selected[d["fqcn"]] = d
            frontier.append(d["name"])
    seen = set()
    while frontier:
        name = frontier.pop()
        if name in seen:
            continue
        seen.add(name)
        for child in children.get(name, []):
            selected[child["fqcn"]] = child
            frontier.append(child["name"])
    runnable = [d for d in selected.values() if d["kind"] == "class" and not d["abstract"] and d["name"].endswith("Suite")]
    unit = sorted(d["fqcn"] for d in runnable if d["path"].startswith("tests/unit/src/test/"))
    slow = sorted(d["fqcn"] for d in runnable if d["path"].startswith("tests/slow/src/test/"))
    print("unit: " + " ".join(unit))
    print("slow: " + " ".join(slow))


if __name__ == "__main__":
    main()
