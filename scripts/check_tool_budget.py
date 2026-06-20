#!/usr/bin/env python3
"""Check that the openmc-agent tool list is within budget and contains no private deps.

Usage:
    python scripts/check_tool_budget.py [--max N]

Exit codes:
    0 — all checks pass
    1 — tool budget exceeded
    2 — private dependency found
    3 — YAML parse error
"""

import re
import sys
from pathlib import Path

AGENT_FILE = Path(__file__).resolve().parent.parent / "openmc-agent.agent.md"

# ── Hard cap ──
DEFAULT_MAX = 25

# ── Private tool names that must NOT appear ──
BLOCKLIST = [
    "scnetresource",
    "dify-knowledge",
    "dify_knowledge",
    "session-memor",
    "plausibility-check",
    "de-ai-fier",
    "deai_review",
    "vale_gate",
    "project-manag",
    "formatforge",
    "tikz-writer",
    "citation-lint",
    "manuscript-lint",
    "factcheck-gate",
    "image-worker",
    "fusion-terms",
    "fusion_materials",
]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Check openmc-agent tool budget")
    parser.add_argument("--max", type=int, default=DEFAULT_MAX, help="Maximum allowed tools")
    args = parser.parse_args()

    if not AGENT_FILE.exists():
        print(f"ERROR: {AGENT_FILE} not found")
        sys.exit(4)

    content = AGENT_FILE.read_text()

    # Parse YAML frontmatter
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        print("ERROR: No YAML frontmatter found")
        sys.exit(3)

    try:
        import yaml
        parsed = yaml.safe_load(match.group(1))
    except ImportError:
        print("ERROR: PyYAML not installed (pip install pyyaml)")
        sys.exit(3)
    except Exception as e:
        print(f"ERROR: YAML parse error: {e}")
        sys.exit(3)

    tools = parsed.get("tools", [])
    tool_names = [t if isinstance(t, str) else str(t) for t in tools]

    exit_code = 0

    # ── Check 1: Tool budget ──
    count = len(tool_names)
    print(f"Tool count: {count}/{args.max}")
    if count > args.max:
        print(f"FAIL: Tool count {count} exceeds cap {args.max}")
        exit_code = max(exit_code, 1)
    else:
        print("PASS: Tool count within budget")

    # ── Check 2: No private deps ──
    violations = []
    for tn in tool_names:
        tn_lower = tn.lower()
        for bl in BLOCKLIST:
            if bl.lower() in tn_lower:
                violations.append(f"  {tn} (matches '{bl}')")
                break

    if violations:
        print("FAIL: Private dependency references found:")
        for v in violations:
            print(v)
        exit_code = max(exit_code, 2)
    else:
        print("PASS: No private dependencies")

    # ── Summary ──
    status = "PASS" if exit_code == 0 else f"FAIL (code {exit_code})"
    print(f"\nOverall: {status}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
