"""Tests for scripts/health_check.py - installation health checks."""

from pathlib import Path

from health_check import (
    check_agents,
    check_credentials,
    check_python_deps,
    check_routing,
    check_scripts,
    check_skills,
    run_health_check,
)


class TestCheckPythonDeps:
    def test_finds_installed_packages(self):
        results = check_python_deps()
        # requests is in the test environment
        names = [r["check"] for r in results]
        assert any("requests" in n for n in names)

    def test_result_structure(self):
        results = check_python_deps()
        for r in results:
            assert "check" in r
            assert "status" in r
            assert r["status"] in ("pass", "fail", "skip")
            assert "detail" in r

    def test_missing_package_reports_fail(self, monkeypatch):
        import importlib

        original = importlib.import_module

        def mock_import(name):
            if name == "requests":
                raise ImportError("mocked")
            return original(name)

        monkeypatch.setattr(importlib, "import_module", mock_import)
        results = check_python_deps()
        requests_result = [r for r in results if "requests" in r["check"]][0]
        assert requests_result["status"] == "fail"
        assert "fix" in requests_result


class TestCheckCredentials:
    def test_missing_credential_files(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
        results = check_credentials()
        statuses = [r["status"] for r in results]
        assert "skip" in statuses

    def test_present_credential_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
        auth_path = tmp_path / ".config" / "dataforseo" / "auth"
        auth_path.parent.mkdir(parents=True)
        auth_path.write_text("dXNlcjpwYXNzd29yZA==")  # base64, >10 chars
        results = check_credentials()
        dfs_result = [r for r in results if "DataForSEO" in r["check"]][0]
        assert dfs_result["status"] == "pass"

    def test_short_credential_warns(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
        auth_path = tmp_path / ".config" / "dataforseo" / "auth"
        auth_path.parent.mkdir(parents=True)
        auth_path.write_text("short")
        results = check_credentials()
        dfs_result = [r for r in results if "DataForSEO" in r["check"]][0]
        assert dfs_result["status"] == "warn"


class TestCheckSkills:
    def test_valid_skill(self, tmp_path):
        skills_dir = tmp_path / "skills"
        skill = skills_dir / "my-skill"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: A good skill\n---\nBody text"
        )
        results = check_skills(tmp_path)
        assert results[0]["status"] == "pass"
        assert "1/1" in results[0]["detail"]

    def test_missing_skill_md(self, tmp_path):
        skills_dir = tmp_path / "skills"
        (skills_dir / "bad-skill").mkdir(parents=True)
        results = check_skills(tmp_path)
        assert results[0]["status"] == "warn"
        assert any("missing SKILL.md" in i for i in results[0]["issues"])

    def test_missing_frontmatter(self, tmp_path):
        skills_dir = tmp_path / "skills"
        skill = skills_dir / "no-fm"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("No frontmatter here")
        results = check_skills(tmp_path)
        assert results[0]["status"] == "warn"
        assert any("missing YAML frontmatter" in i for i in results[0]["issues"])

    def test_missing_name_field(self, tmp_path):
        skills_dir = tmp_path / "skills"
        skill = skills_dir / "no-name"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\ndescription: something\n---\nBody"
        )
        results = check_skills(tmp_path)
        assert results[0]["status"] == "warn"
        assert any("missing 'name'" in i for i in results[0]["issues"])

    def test_missing_description_field(self, tmp_path):
        skills_dir = tmp_path / "skills"
        skill = skills_dir / "no-desc"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: foo\n---\nBody")
        results = check_skills(tmp_path)
        assert results[0]["status"] == "warn"
        assert any("missing 'description'" in i for i in results[0]["issues"])

    def test_no_skills_dir(self, tmp_path):
        results = check_skills(tmp_path)
        assert results[0]["status"] == "fail"


class TestCheckAgents:
    def test_valid_agent(self, tmp_path):
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "agent.md").write_text(
            "---\nname: a\ndescription: b\ntools:\n  - t\n---\nBody"
        )
        results = check_agents(tmp_path)
        assert results[0]["status"] == "pass"
        assert "1/1" in results[0]["detail"]

    def test_missing_agent_fields(self, tmp_path):
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "agent.md").write_text("---\nname: a\n---\nBody")
        results = check_agents(tmp_path)
        assert results[0]["status"] == "warn"
        assert any("missing fields" in i for i in results[0]["issues"])

    def test_no_agents_dir(self, tmp_path):
        results = check_agents(tmp_path)
        assert results[0]["status"] == "fail"

    def test_malformed_frontmatter(self, tmp_path):
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "bad.md").write_text("No frontmatter at all")
        results = check_agents(tmp_path)
        assert results[0]["status"] == "warn"
        assert any("missing YAML frontmatter" in i for i in results[0]["issues"])


class TestCheckRouting:
    def test_all_routes_match(self, tmp_path):
        seo_dir = tmp_path / "seo"
        seo_dir.mkdir()
        skills_dir = tmp_path / "skills"
        (skills_dir / "30x-seo-page").mkdir(parents=True)
        (seo_dir / "SKILL.md").write_text(
            "| `page` | 30x-seo-page | Page audit |"
        )
        results = check_routing(tmp_path)
        assert results[0]["status"] == "pass"

    def test_missing_skill_dir_for_route(self, tmp_path):
        seo_dir = tmp_path / "seo"
        seo_dir.mkdir()
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        (seo_dir / "SKILL.md").write_text(
            "| `ghost` | 30x-seo-ghost | Ghost skill |"
        )
        results = check_routing(tmp_path)
        assert results[0]["status"] == "warn"
        assert any("directory missing" in i for i in results[0]["issues"])

    def test_unrouted_skill(self, tmp_path):
        seo_dir = tmp_path / "seo"
        seo_dir.mkdir()
        skills_dir = tmp_path / "skills"
        (skills_dir / "30x-seo-orphan").mkdir(parents=True)
        (seo_dir / "SKILL.md").write_text("No routes here")
        results = check_routing(tmp_path)
        assert results[0]["status"] == "warn"
        assert any("no route" in i for i in results[0]["issues"])

    def test_no_orchestrator_file(self, tmp_path):
        results = check_routing(tmp_path)
        assert results[0]["status"] == "fail"


class TestCheckScripts:
    def test_valid_scripts(self, tmp_path):
        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "good.py").write_text("x = 1 + 2\n")
        results = check_scripts(tmp_path)
        assert results[0]["status"] == "pass"

    def test_syntax_error(self, tmp_path):
        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "bad.py").write_text("def broken(\n")
        results = check_scripts(tmp_path)
        assert results[0]["status"] == "fail"
        assert any("syntax error" in i for i in results[0]["issues"])

    def test_no_scripts_dir(self, tmp_path):
        results = check_scripts(tmp_path)
        assert results == []


class TestRunHealthCheck:
    def test_returns_summary_structure(self, tmp_path):
        # Create minimal valid project
        (tmp_path / "skills").mkdir()
        (tmp_path / "agents").mkdir()
        (tmp_path / "seo").mkdir()
        (tmp_path / "seo" / "SKILL.md").write_text("")
        (tmp_path / "scripts").mkdir()

        report = run_health_check(tmp_path)
        assert "project_root" in report
        assert "summary" in report
        assert "checks" in report
        summary = report["summary"]
        assert "total" in summary
        assert "pass" in summary
        assert "fail" in summary
        assert "warn" in summary
        assert "skip" in summary
        assert "healthy" in summary
        assert isinstance(summary["healthy"], bool)

    def test_healthy_when_no_failures(self, tmp_path):
        (tmp_path / "skills").mkdir()
        (tmp_path / "agents").mkdir()
        (tmp_path / "seo").mkdir()
        (tmp_path / "seo" / "SKILL.md").write_text("")
        (tmp_path / "scripts").mkdir()

        report = run_health_check(tmp_path)
        # No fail-level checks from empty dirs
        assert report["summary"]["fail"] == 0
        assert report["summary"]["healthy"] is True
