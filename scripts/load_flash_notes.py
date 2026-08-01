#!/usr/bin/env python3
"""Load data/flash_notes.js JSON safely (string-aware brace matching)."""
import json
import re
import sys


def load(path="data/flash_notes.js"):
    src = open(path, encoding="utf-8").read()
    start = src.index("{")
    depth = 0
    in_str = False
    esc = False
    end = None
    for i in range(start, len(src)):
        ch = src[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    obj = src[start:end]
    data = json.loads(obj)
    items = []
    for dept, arr in data.get("byDept", {}).items():
        for d in arr:
            d["_dept"] = dept
            items.append(d)
    return data, items


if __name__ == "__main__":
    data, items = load()
    print("total:", data["total"], "flattened:", len(items))
    if len(sys.argv) > 1 and sys.argv[1] == "stats":
        from collections import Counter

        frags = [d for d in items if d.get("_merged_into")]
        repaired = [d for d in items if d.get("_repaired_2026")]
        disputed = [d for d in items if d.get("_answer_disputed")]
        noopt = [d for d in items if len(d.get("options", [])) < 2]
        print("merged fragments:", len(frags))
        print("repaired:", len(repaired))
        print("answer_disputed:", len(disputed))
        print("items with <2 options:", len(noopt))
        c = Counter(d.get("_dept") for d in items)
        print("byDept:", dict(c))
