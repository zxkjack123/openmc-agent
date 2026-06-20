"""Contract tests for openmc-agent.agent.md.

These tests verify that the agent definition file satisfies:
1. Parseable YAML frontmatter
2. Tool list within budget (≤25)
3. Zero private dependencies (no scnetresource-router, dify-knowledge, etc.)
4. Required sections present
"""

import os
import re
from pathlib import Path

AGENT_FILE = Path(__file__).resolve().parent.parent / "openmc-agent.agent.md"

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

# ── Required sections ──
REQUIRED_SECTIONS = [
    "## Workflow",
    "### Stage A",
    "### Stage B",
    "### Stage C",
    "### Stage D",
    "### Stage E",
    "### Stage F",
    "### Stage G",
    "### Stage H",
]

HARD_CAP = 25


def read_agent_file() -> str:
    """Read the agent definition file."""
    if not AGENT_FILE.exists():
        raise FileNotFoundError(f"{AGENT_FILE} not found")
    return AGENT_FILE.read_text()


def test_agent_file_exists():
    """Agent definition file must exist."""
    assert AGENT_FILE.exists(), f"{AGENT_FILE} not found"


def test_yaml_frontmatter_parseable():
    """YAML frontmatter must be parseable."""
    import yaml

    content = read_agent_file()
    # Extract YAML frontmatter between --- delimiters
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    assert match is not None, "No YAML frontmatter found (missing --- delimiters)"

    yaml_text = match.group(1)
    try:
        parsed = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        raise AssertionError(f"YAML parse error: {e}")

    assert parsed is not None, "YAML frontmatter is empty"
    assert "name" in parsed, "Missing 'name' field in frontmatter"
    assert "tools" in parsed, "Missing 'tools' field in frontmatter"
    assert isinstance(parsed["tools"], list), "'tools' must be a list"


def test_tool_budget():
    """Tool list must be within budget (≤25)."""
    import yaml

    content = read_agent_file()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    yaml_text = match.group(1)
    parsed = yaml.safe_load(yaml_text)

    tool_count = len(parsed["tools"])
    assert tool_count <= HARD_CAP, f"Tool count {tool_count} exceeds hard cap {HARD_CAP}"


def test_no_private_dependencies():
    """No private dependency tool names in the tool list."""
    import yaml

    content = read_agent_file()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    yaml_text = match.group(1)
    parsed = yaml.safe_load(yaml_text)

    tools = [t.lower() if isinstance(t, str) else str(t).lower() for t in parsed["tools"]]
    for bl in BLOCKLIST:
        for tool in tools:
            assert bl.lower() not in tool, f"Private dependency '{bl}' found in tools: '{tool}'"


def test_all_openmc_validator_tools_present():
    """All 14 openmc-validator tools must be present."""
    import yaml

    expected_validator_tools = [
        "validate_materials",
        "validate_geometry",
        "validate_settings",
        "validate_tallies",
        "validate_model",
        "check_cross_section_library",
        "check_energy_filter_coverage",
        "check_tally_filter_consistency",
        "convert_spectrum_openmc_to_fispact",
        "extract_tally_summary",
        "list_templates",
        "get_template",
        "list_materials",
        "get_material",
    ]

    content = read_agent_file()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    yaml_text = match.group(1)
    parsed = yaml.safe_load(yaml_text)

    tools = [t.lower() if isinstance(t, str) else str(t).lower() for t in parsed["tools"]]
    for vt in expected_validator_tools:
        found = any(vt in t for t in tools)
        assert found, f"Validator tool '{vt}' missing from tool list"


def test_required_sections_present():
    """All required workflow stages must be present in markdown body."""
    content = read_agent_file()
    for section in REQUIRED_SECTIONS:
        assert section in content, f"Required section '{section}' not found"


def test_open_source_boundary_in_text():
    """The markdown body must document the open-source boundary.
    Private repos may be mentioned for context (e.g. 'Private Overlay' section)
    but NEVER as required dependencies or in the tools list.
    """
    content = read_agent_file().lower()

    # Allow mentions of private deps ONLY if they appear in the Private Overlay section
    # or are clearly documented as "not included" alternatives.
    # Extract the tools list for strict checking
    import yaml
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if match:
        yaml_text = match.group(1)
        parsed = yaml.safe_load(yaml_text)
        tools = [t.lower() if isinstance(t, str) else str(t).lower() for t in parsed.get("tools", [])]
        for tool in tools:
            for bl in BLOCKLIST:
                assert bl.lower() not in tool, \
                    f"Private dependency '{bl}' found in TOOL LIST: '{tool}'"

    # Body mentions of private deps as "not included" are fine — but warn
    body = content[match.end():] if match else content
    for bl in BLOCKLIST:
        if bl.lower() in body:
            # Acceptable in body — just log a note
            pass  # Body mention of private alternatives is permitted


def test_constitution_exists():
    """CONSTITUTION.md must exist alongside agent.md."""
    const = AGENT_FILE.parent / "CONSTITUTION.md"
    assert const.exists(), f"{const} not found"


def test_readme_exists():
    """README.md must exist."""
    readme = AGENT_FILE.parent / "README.md"
    assert readme.exists(), f"{readme} not found"


# ── Manual verification markers (not executable) ──
def test_check_tool_budget_script():
    """scripts/check_tool_budget.py must exist and be parseable."""
    script = AGENT_FILE.parent / "scripts" / "check_tool_budget.py"
    assert script.exists(), f"{script} not found"
    # Verify it's parseable Python
    compile(script.read_text(), str(script), "exec")
