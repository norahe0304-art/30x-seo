"""Tests for scripts/telemetry.py - local usage telemetry."""

import json

import telemetry


class TestRecord:
    def test_creates_jsonl_entry(self, tmp_path, monkeypatch):
        tel_dir = tmp_path / "tel"
        tel_file = tel_dir / "telemetry.jsonl"
        monkeypatch.setattr(telemetry, "TELEMETRY_DIR", tel_dir)
        monkeypatch.setattr(telemetry, "TELEMETRY_FILE", tel_file)
        monkeypatch.setattr(telemetry, "DISABLED_FLAG", tel_dir / "disabled")

        telemetry.record("seo-page", duration=2.5, success=True)

        lines = tel_file.read_text().strip().splitlines()
        assert len(lines) == 1
        entry = json.loads(lines[0])
        assert entry["skill"] == "seo-page"
        assert entry["duration_s"] == 2.5
        assert entry["success"] is True
        assert "ts" in entry

    def test_respects_disabled_flag(self, tmp_path, monkeypatch):
        tel_dir = tmp_path / "tel"
        tel_dir.mkdir()
        tel_file = tel_dir / "telemetry.jsonl"
        disabled_flag = tel_dir / "disabled"
        disabled_flag.touch()

        monkeypatch.setattr(telemetry, "TELEMETRY_DIR", tel_dir)
        monkeypatch.setattr(telemetry, "TELEMETRY_FILE", tel_file)
        monkeypatch.setattr(telemetry, "DISABLED_FLAG", disabled_flag)

        telemetry.record("seo-page")
        assert not tel_file.exists()

    def test_appends_multiple_entries(self, tmp_path, monkeypatch):
        tel_dir = tmp_path / "tel"
        tel_file = tel_dir / "telemetry.jsonl"
        monkeypatch.setattr(telemetry, "TELEMETRY_DIR", tel_dir)
        monkeypatch.setattr(telemetry, "TELEMETRY_FILE", tel_file)
        monkeypatch.setattr(telemetry, "DISABLED_FLAG", tel_dir / "disabled")

        telemetry.record("skill-a")
        telemetry.record("skill-b")
        lines = tel_file.read_text().strip().splitlines()
        assert len(lines) == 2

    def test_omits_duration_when_none(self, tmp_path, monkeypatch):
        tel_dir = tmp_path / "tel"
        tel_file = tel_dir / "telemetry.jsonl"
        monkeypatch.setattr(telemetry, "TELEMETRY_DIR", tel_dir)
        monkeypatch.setattr(telemetry, "TELEMETRY_FILE", tel_file)
        monkeypatch.setattr(telemetry, "DISABLED_FLAG", tel_dir / "disabled")

        telemetry.record("seo-page")
        entry = json.loads(tel_file.read_text().strip())
        assert "duration_s" not in entry


class TestLoadEntries:
    def test_parses_jsonl(self, tmp_path, monkeypatch):
        tel_file = tmp_path / "telemetry.jsonl"
        tel_file.write_text(
            '{"skill": "a", "ts": "2025-01-01T00:00:00Z", "success": true}\n'
            '{"skill": "b", "ts": "2025-01-02T00:00:00Z", "success": false}\n'
        )
        monkeypatch.setattr(telemetry, "TELEMETRY_FILE", tel_file)
        entries = telemetry.load_entries()
        assert len(entries) == 2
        assert entries[0]["skill"] == "a"
        assert entries[1]["skill"] == "b"

    def test_handles_empty_file(self, tmp_path, monkeypatch):
        tel_file = tmp_path / "telemetry.jsonl"
        tel_file.write_text("")
        monkeypatch.setattr(telemetry, "TELEMETRY_FILE", tel_file)
        assert telemetry.load_entries() == []

    def test_handles_missing_file(self, tmp_path, monkeypatch):
        tel_file = tmp_path / "nonexistent.jsonl"
        monkeypatch.setattr(telemetry, "TELEMETRY_FILE", tel_file)
        assert telemetry.load_entries() == []

    def test_skips_invalid_json_lines(self, tmp_path, monkeypatch):
        tel_file = tmp_path / "telemetry.jsonl"
        tel_file.write_text(
            '{"skill": "good"}\n'
            "NOT JSON\n"
            '{"skill": "also-good"}\n'
        )
        monkeypatch.setattr(telemetry, "TELEMETRY_FILE", tel_file)
        entries = telemetry.load_entries()
        assert len(entries) == 2


class TestGenerateReport:
    def _write_entries(self, tmp_path, monkeypatch, entries):
        tel_file = tmp_path / "telemetry.jsonl"
        tel_file.write_text(
            "\n".join(json.dumps(e) for e in entries) + "\n"
        )
        monkeypatch.setattr(telemetry, "TELEMETRY_FILE", tel_file)

    def test_empty_data(self, tmp_path, monkeypatch):
        monkeypatch.setattr(telemetry, "TELEMETRY_FILE", tmp_path / "nope.jsonl")
        result = telemetry.generate_report()
        assert "No telemetry data" in result

    def test_aggregates_counts(self, tmp_path, monkeypatch):
        entries = [
            {"skill": "page", "ts": "2025-01-01T00:00:00Z", "success": True, "duration_s": 1.0},
            {"skill": "page", "ts": "2025-01-02T00:00:00Z", "success": True, "duration_s": 3.0},
            {"skill": "links", "ts": "2025-01-03T00:00:00Z", "success": False, "duration_s": 2.0},
        ]
        self._write_entries(tmp_path, monkeypatch, entries)
        result = telemetry.generate_report()
        assert "page" in result
        assert "links" in result

    def test_json_mode(self, tmp_path, monkeypatch):
        entries = [
            {"skill": "page", "ts": "2025-01-01T00:00:00Z", "success": True, "duration_s": 1.0},
            {"skill": "page", "ts": "2025-01-02T00:00:00Z", "success": False, "duration_s": 3.0},
        ]
        self._write_entries(tmp_path, monkeypatch, entries)
        raw = telemetry.generate_report(as_json=True)
        data = json.loads(raw)
        assert data["total_invocations"] == 2
        assert data["skills"]["page"]["count"] == 2
        assert data["skills"]["page"]["success"] == 1
        assert data["skills"]["page"]["fail"] == 1
        assert data["skills"]["page"]["avg_duration_s"] == 2.0

    def test_json_mode_empty(self, tmp_path, monkeypatch):
        monkeypatch.setattr(telemetry, "TELEMETRY_FILE", tmp_path / "nope.jsonl")
        raw = telemetry.generate_report(as_json=True)
        data = json.loads(raw)
        assert data["total_invocations"] == 0
        assert data["skills"] == {}


class TestEnableDisable:
    def test_is_enabled_default(self, tmp_path, monkeypatch):
        monkeypatch.setattr(telemetry, "DISABLED_FLAG", tmp_path / "disabled")
        assert telemetry.is_enabled() is True

    def test_disable_creates_flag(self, tmp_path, monkeypatch):
        tel_dir = tmp_path / "tel"
        disabled_flag = tel_dir / "disabled"
        monkeypatch.setattr(telemetry, "TELEMETRY_DIR", tel_dir)
        monkeypatch.setattr(telemetry, "DISABLED_FLAG", disabled_flag)
        telemetry.disable()
        assert disabled_flag.exists()
        assert telemetry.is_enabled() is False

    def test_enable_removes_flag(self, tmp_path, monkeypatch):
        tel_dir = tmp_path / "tel"
        tel_dir.mkdir()
        disabled_flag = tel_dir / "disabled"
        disabled_flag.touch()
        monkeypatch.setattr(telemetry, "TELEMETRY_DIR", tel_dir)
        monkeypatch.setattr(telemetry, "DISABLED_FLAG", disabled_flag)
        telemetry.enable()
        assert not disabled_flag.exists()
        assert telemetry.is_enabled() is True


class TestClearData:
    def test_removes_file(self, tmp_path, monkeypatch):
        tel_file = tmp_path / "telemetry.jsonl"
        tel_file.write_text('{"skill":"x"}\n')
        monkeypatch.setattr(telemetry, "TELEMETRY_FILE", tel_file)
        telemetry.clear_data()
        assert not tel_file.exists()

    def test_no_error_when_missing(self, tmp_path, monkeypatch):
        tel_file = tmp_path / "nonexistent.jsonl"
        monkeypatch.setattr(telemetry, "TELEMETRY_FILE", tel_file)
        telemetry.clear_data()  # should not raise
