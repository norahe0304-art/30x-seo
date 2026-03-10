"""Tests for skill directory structure and orchestrator routing table consistency."""

import os
import re

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(PROJECT_ROOT, "skills")
ORCHESTRATOR_SKILL_MD = os.path.join(PROJECT_ROOT, "seo", "SKILL.md")

# The 26 expected skill directories
EXPECTED_SKILLS = [
    "30x-seo-ai-visibility",
    "30x-seo-architecture",
    "30x-seo-backlinks",
    "30x-seo-cannibalization",
    "30x-seo-competitor-pages",
    "30x-seo-content-audit",
    "30x-seo-content-brief",
    "30x-seo-content-decay",
    "30x-seo-content-writer",
    "30x-seo-discover",
    "30x-seo-fake-freshness",
    "30x-seo-geo-technical",
    "30x-seo-hreflang",
    "30x-seo-images",
    "30x-seo-internal-links",
    "30x-seo-keywords",
    "30x-seo-mobile-parity",
    "30x-seo-monitor",
    "30x-seo-page",
    "30x-seo-plan",
    "30x-seo-programmatic",
    "30x-seo-redirects",
    "30x-seo-schema",
    "30x-seo-serp",
    "30x-seo-sitemap",
    "30x-seo-technical",
]


def _parse_yaml_frontmatter(filepath):
    """Parse YAML frontmatter from a SKILL.md file (simple parser, no pyyaml needed)."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return None

    end = content.find("---", 3)
    if end == -1:
        return None

    frontmatter = content[3:end].strip()
    result = {}

    # Extract name
    name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
    if name_match:
        result["name"] = name_match.group(1).strip()

    # Extract description (may be multi-line with > folded scalar)
    # First try multi-line: "description: >" followed by indented lines
    desc_match = re.search(r"^description:\s*>\s*\n((?:[ \t]+.+\n?)+)", frontmatter, re.MULTILINE)
    if desc_match:
        result["description"] = " ".join(desc_match.group(1).strip().split())
    else:
        # Single-line description
        desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
        if desc_match:
            result["description"] = desc_match.group(1).strip().strip(">")

    # Extract allowed-tools
    tools_section = re.search(r"^allowed-tools:\s*\n((?:\s+-\s+.+\n?)*)", frontmatter, re.MULTILINE)
    if tools_section:
        tools = re.findall(r"-\s+(\S+)", tools_section.group(1))
        result["allowed-tools"] = tools

    return result


def _parse_routing_table(filepath):
    """Extract the command-to-skill routing table from orchestrator SKILL.md."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Find the routing table section
    routing = {}
    for match in re.finditer(r"\|\s*`(\S+)`\s*\|\s*(\S+)\s*\|", content):
        command = match.group(1)
        skill = match.group(2)
        if command != "Command" and skill != "Loads":  # skip header
            routing[command] = skill

    return routing


class TestSkillDirectoriesExist:
    @pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
    def test_skill_directory_exists(self, skill_name):
        skill_dir = os.path.join(SKILLS_DIR, skill_name)
        assert os.path.isdir(skill_dir), f"Skill directory missing: {skill_dir}"


class TestSkillMdFiles:
    @pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
    def test_skill_md_exists(self, skill_name):
        skill_md = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
        assert os.path.isfile(skill_md), f"SKILL.md missing for {skill_name}"

    @pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
    def test_skill_md_has_yaml_frontmatter(self, skill_name):
        skill_md = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
        with open(skill_md) as f:
            content = f.read()
        assert content.startswith("---"), (
            f"{skill_name}/SKILL.md missing YAML frontmatter delimiter"
        )
        assert content.find("---", 3) > 3, (
            f"{skill_name}/SKILL.md missing closing frontmatter delimiter"
        )

    @pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
    def test_skill_md_has_name(self, skill_name):
        skill_md = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
        fm = _parse_yaml_frontmatter(skill_md)
        assert fm is not None, f"Could not parse frontmatter for {skill_name}"
        assert "name" in fm, f"{skill_name}/SKILL.md missing 'name' in frontmatter"
        assert fm["name"] == skill_name, (
            f"{skill_name}/SKILL.md 'name' mismatch: expected '{skill_name}', got '{fm['name']}'"
        )

    @pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
    def test_skill_md_has_description(self, skill_name):
        skill_md = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
        fm = _parse_yaml_frontmatter(skill_md)
        assert fm is not None
        assert "description" in fm, f"{skill_name}/SKILL.md missing 'description'"
        assert len(fm["description"]) > 10, f"{skill_name}/SKILL.md description too short"

    @pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
    def test_skill_md_has_allowed_tools(self, skill_name):
        skill_md = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
        fm = _parse_yaml_frontmatter(skill_md)
        assert fm is not None
        assert "allowed-tools" in fm, f"{skill_name}/SKILL.md missing 'allowed-tools'"
        assert len(fm["allowed-tools"]) >= 1, f"{skill_name}/SKILL.md has no allowed tools"


class TestOrchestratorRoutingTable:
    def test_orchestrator_skill_md_exists(self):
        assert os.path.isfile(ORCHESTRATOR_SKILL_MD), "Orchestrator seo/SKILL.md not found"

    def test_routing_table_has_entries(self):
        routing = _parse_routing_table(ORCHESTRATOR_SKILL_MD)
        assert len(routing) >= 26, (
            f"Expected at least 26 routing entries, "
            f"got {len(routing)}: {list(routing.keys())}"
        )

    def test_all_routed_skills_have_directories(self):
        routing = _parse_routing_table(ORCHESTRATOR_SKILL_MD)
        for command, skill_name in routing.items():
            skill_dir = os.path.join(SKILLS_DIR, skill_name)
            assert os.path.isdir(skill_dir), (
                f"Routing table maps '{command}' to '{skill_name}' but directory does not exist"
            )

    def test_all_skill_directories_are_routed(self):
        routing = _parse_routing_table(ORCHESTRATOR_SKILL_MD)
        routed_skills = set(routing.values())
        for skill_name in EXPECTED_SKILLS:
            assert skill_name in routed_skills, (
                f"Skill '{skill_name}' exists but is not in the routing table"
            )

    def test_routing_skills_match_skill_md_names(self):
        routing = _parse_routing_table(ORCHESTRATOR_SKILL_MD)
        for command, skill_name in routing.items():
            skill_md = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
            if os.path.isfile(skill_md):
                fm = _parse_yaml_frontmatter(skill_md)
                if fm and "name" in fm:
                    assert fm["name"] == skill_name, (
                        f"Routing maps '{command}' to '{skill_name}' "
                        f"but SKILL.md name is '{fm['name']}'"
                    )


class TestOrchestratorSkillMd:
    def test_orchestrator_has_frontmatter(self):
        fm = _parse_yaml_frontmatter(ORCHESTRATOR_SKILL_MD)
        assert fm is not None

    def test_orchestrator_name(self):
        fm = _parse_yaml_frontmatter(ORCHESTRATOR_SKILL_MD)
        assert fm["name"] == "seo"

    def test_orchestrator_has_description(self):
        fm = _parse_yaml_frontmatter(ORCHESTRATOR_SKILL_MD)
        assert "description" in fm
        assert len(fm["description"]) > 20

    def test_orchestrator_has_allowed_tools(self):
        fm = _parse_yaml_frontmatter(ORCHESTRATOR_SKILL_MD)
        assert "allowed-tools" in fm
        assert "Read" in fm["allowed-tools"]
