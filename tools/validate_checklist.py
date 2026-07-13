#!/usr/bin/env python3
"""Validate checklist.yaml against the contract documented in CHECKLIST.md.

Exits non-zero on any violation: invalid YAML, non-kebab or duplicate step id,
missing required field, wrong how_on_hanzo keys, unresolved depends_on, or a
dependency cycle. Run from the repo root: python3 tools/validate_checklist.py
"""
import re
import sys
from collections import deque
from pathlib import Path

import yaml

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
STEP_FIELDS = ("id", "title", "why", "how_on_hanzo", "done_criteria", "depends_on")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    path = Path(__file__).resolve().parent.parent / "checklist.yaml"
    try:
        doc = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        fail(f"invalid YAML: {e}")

    if doc.get("schema_version") != 1:
        fail(f"schema_version must be 1, got {doc.get('schema_version')!r}")
    if not KEBAB.match(str(doc.get("curriculum", ""))):
        fail(f"curriculum id not kebab-case: {doc.get('curriculum')!r}")

    steps: dict[str, dict] = {}
    for stage in doc.get("stages", []):
        if not KEBAB.match(stage.get("id", "")):
            fail(f"stage id not kebab-case: {stage.get('id')!r}")
        for step in stage.get("steps", []):
            sid = step.get("id", "")
            if not KEBAB.match(sid):
                fail(f"step id not kebab-case: {sid!r}")
            if sid in steps:
                fail(f"duplicate step id: {sid}")
            for field in STEP_FIELDS:
                if field not in step:
                    fail(f"{sid} missing required field: {field}")
            if set(step["how_on_hanzo"]) != {"product", "route"}:
                fail(f"{sid} how_on_hanzo keys must be exactly {{product, route}}")
            if not isinstance(step["depends_on"], list):
                fail(f"{sid} depends_on must be a list")
            steps[sid] = step

    # every dependency must resolve
    for sid, step in steps.items():
        for dep in step["depends_on"]:
            if dep not in steps:
                fail(f"{sid} depends on unknown step id: {dep}")

    # DAG: topological sort must consume every node
    indeg = {sid: 0 for sid in steps}
    adj: dict[str, list[str]] = {sid: [] for sid in steps}
    for sid, step in steps.items():
        for dep in step["depends_on"]:
            adj[dep].append(sid)
            indeg[sid] += 1
    queue = deque(sid for sid, d in indeg.items() if d == 0)
    resolved = 0
    while queue:
        node = queue.popleft()
        resolved += 1
        for nxt in adj[node]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    if resolved != len(steps):
        cyclic = sorted(sid for sid, d in indeg.items() if d > 0)
        fail(f"dependency cycle among: {cyclic}")

    print(
        f"OK: {len(doc['stages'])} stages, {len(steps)} steps, "
        "all ids kebab+unique, all deps resolve, no cycles"
    )


if __name__ == "__main__":
    main()
