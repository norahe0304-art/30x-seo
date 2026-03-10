"""Tests for scripts/validate_skills.py - skill and agent metadata validation."""

import validate_skills


class TestParseeFrontmatter:
    def test_valid_frontmatter(self, tmp_path):
        md_file = tmp_path / "test.md"
        md_file.write_text("---\nname: foo\ndescription: bar\n---\nBody text")
        result = validate_skills.parse_frontmatter(md_file)
        assert result == {"name": "foo", "description": "bar"}

    def test_missing_frontmatter(self, tmp_path):
        md_file = tmp_path / "test.md"
        md_file.write_text("No frontmatter here")
        result = validate_skills.parse_frontmatter(md_file)
        assert result is None

    def test_invalid_yaml(self, tmp_path, monkeypatch):
        md_file = tmp_path / "test.md"
        md_file.write_text("---\n: [invalid yaml\n---\nBody")
        # Reset module-level errors list
        monkeypatch.setattr(validate_skills, "errors", [])
        result = validate_skills.parse_frontmatter(md_file)
        assert result is None


class TestValidateSkills:
    def test_valid_skill_directory(self, tmp_path, monkeypatch):
        skills_dir = tmp_path / "skills"
        skill = skills_dir / "my-skill"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: A test skill\n---\nContent"
        )
        monkeypatch.setattr(validate_skills, "SKILLS_DIR", skills_dir)
        monkeypatch.setattr(validate_skills, "errors", [])
        validate_skills.validate_skills()
        assert validate_skills.errors == []

    def test_missing_skill_md(self, tmp_path, monkeypatch):
        skills_dir = tmp_path / "skills"
        (skills_dir / "empty-skill").mkdir(parents=True)
        monkeypatch.setattr(validate_skills, "SKILLS_DIR", skills_dir)
        monkeypatch.setattr(validate_skills, "errors", [])
        validate_skills.validate_skills()
        assert any("missing SKILL.md" in e for e in validate_skills.errors)

    def test_missing_frontmatter_fields(self, tmp_path, monkeypatch):
        skills_dir = tmp_path / "skills"
        skill = skills_dir / "partial"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: partial\n---\nBody")
        monkeypatch.setattr(validate_skills, "SKILLS_DIR", skills_dir)
        monkeypatch.setattr(validate_skills, "errors", [])
        validate_skills.validate_skills()
        assert any("missing 'description'" in e for e in validate_skills.errors)

    def test_no_skills_directory(self, tmp_path, monkeypatch):
        monkeypatch.setattr(validate_skills, "SKILLS_DIR", tmp_path / "nope")
        monkeypatch.setattr(validate_skills, "errors", [])
        validate_skills.validate_skills()
        assert any("not found" in e for e in validate_skills.errors)

    def test_missing_name_field(self, tmp_path, monkeypatch):
        skills_dir = tmp_path / "skills"
        skill = skills_dir / "no-name"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\ndescription: something\n---\nBody")
        monkeypatch.setattr(validate_skills, "SKILLS_DIR", skills_dir)
        monkeypatch.setattr(validate_skills, "errors", [])
        validate_skills.validate_skills()
        assert any("missing 'name'" in e for e in validate_skills.errors)


class TestValidateAgents:
    def test_valid_agent(self, tmp_path, monkeypatch):
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "agent.md").write_text(
            "---\nname: a\ndescription: b\ntools:\n  - t\n---\nBody"
        )
        monkeypatch.setattr(validate_skills, "AGENTS_DIR", agents_dir)
        monkeypatch.setattr(validate_skills, "errors", [])
        validate_skills.validate_agents()
        assert validate_skills.errors == []

    def test_missing_agent_fields(self, tmp_path, monkeypatch):
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "agent.md").write_text("---\nname: a\n---\nBody")
        monkeypatch.setattr(validate_skills, "AGENTS_DIR", agents_dir)
        monkeypatch.setattr(validate_skills, "errors", [])
        validate_skills.validate_agents()
        assert any("missing 'description'" in e for e in validate_skills.errors)
        assert any("missing 'tools'" in e for e in validate_skills.errors)

    def test_missing_frontmatter(self, tmp_path, monkeypatch):
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "bad.md").write_text("No frontmatter")
        monkeypatch.setattr(validate_skills, "AGENTS_DIR", agents_dir)
        monkeypatch.setattr(validate_skills, "errors", [])
        validate_skills.validate_agents()
        assert any("missing YAML frontmatter" in e for e in validate_skills.errors)

    def test_no_agents_directory(self, tmp_path, monkeypatch):
        monkeypatch.setattr(validate_skills, "AGENTS_DIR", tmp_path / "nope")
        monkeypatch.setattr(validate_skills, "errors", [])
        validate_skills.validate_agents()
        assert any("not found" in e for e in validate_skills.errors)


class TestValidateRoutingTable:
    def test_all_skills_routed(self, tmp_path, monkeypatch):
        skills_dir = tmp_path / "skills"
        (skills_dir / "30x-seo-page").mkdir(parents=True)
        orchestrator = tmp_path / "seo" / "SKILL.md"
        orchestrator.parent.mkdir(parents=True)
        orchestrator.write_text("| `page` | 30x-seo-page | Page audit |")
        monkeypatch.setattr(validate_skills, "SKILLS_DIR", skills_dir)
        monkeypatch.setattr(validate_skills, "ORCHESTRATOR", orchestrator)
        monkeypatch.setattr(validate_skills, "errors", [])
        validate_skills.validate_routing_table()
        assert validate_skills.errors == []

    def test_unrouted_skill_detected(self, tmp_path, monkeypatch):
        skills_dir = tmp_path / "skills"
        (skills_dir / "30x-seo-orphan").mkdir(parents=True)
        orchestrator = tmp_path / "seo" / "SKILL.md"
        orchestrator.parent.mkdir(parents=True)
        orchestrator.write_text("No routes here")
        monkeypatch.setattr(validate_skills, "SKILLS_DIR", skills_dir)
        monkeypatch.setattr(validate_skills, "ORCHESTRATOR", orchestrator)
        monkeypatch.setattr(validate_skills, "errors", [])
        validate_skills.validate_routing_table()
        assert any("no entry" in e for e in validate_skills.errors)

    def test_missing_orchestrator(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            validate_skills, "ORCHESTRATOR", tmp_path / "seo" / "SKILL.md"
        )
        monkeypatch.setattr(validate_skills, "errors", [])
        validate_skills.validate_routing_table()
        assert any("not found" in e for e in validate_skills.errors)

    def test_skips_non_directory_entries(self, tmp_path, monkeypatch):
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        # Create a file, not a directory, inside skills/
        (skills_dir / "README.md").write_text("Not a skill dir")
        (skills_dir / "30x-seo-page").mkdir()
        orchestrator = tmp_path / "seo" / "SKILL.md"
        orchestrator.parent.mkdir(parents=True)
        orchestrator.write_text("| `page` | 30x-seo-page | desc |")
        monkeypatch.setattr(validate_skills, "SKILLS_DIR", skills_dir)
        monkeypatch.setattr(validate_skills, "ORCHESTRATOR", orchestrator)
        monkeypatch.setattr(validate_skills, "errors", [])
        validate_skills.validate_routing_table()
        assert validate_skills.errors == []
