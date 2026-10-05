"""Tests for the stdlib RFC tooling (``scripts/rfc.py``).

This script runs unattended in CI and pushes to ``main``, so its parser and the
three subcommands are covered directly. Tests drive the public surface
(``Rfc``, ``generate_index``, ``main``) rather than internals, and use a
temporary RFC directory so the real ``docs/rfcs`` corpus is never touched.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from types import ModuleType

_RFC_PY = Path(__file__).resolve().parent.parent / "scripts" / "rfc.py"


def _load_rfc_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("rfc_tool", _RFC_PY)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


rfc = _load_rfc_module()


def _write_rfc(
    directory: Path,
    number: str,
    *,
    status: str = "accepted",
    title: str = "Example",
    rfc_type: str = "mixin",
    supersedes: str = "null",
    updated: str = "2026-01-01",
    author: str = "alice",
    extra_body: str = "",
) -> Path:
    """Write a minimal well-formed RFC file and return its path."""
    path = directory / f"{number}-example.md"
    path.write_text(
        f"---\n"
        f'rfc: "{number}"\n'
        f"title: {title}\n"
        f"type: {rfc_type}\n"
        f"status: {status}\n"
        f"created: 2026-01-01\n"
        f"updated: {updated}\n"
        f"author: {author}\n"
        f"github_pr: null\n"
        f"supersedes: {supersedes}\n"
        f"superseded_by: null\n"
        f"---\n\n"
        f"# {title}\n\n{extra_body}",
        encoding="utf-8",
    )
    return path


class TestValueRoundTrip:
    """``_load_value`` / ``_dump_value`` and comment handling."""

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("mixin", "mixin"),
            ('"0006"', "0006"),  # zero-padded id kept as a string
            ("'0006'", "0006"),  # single quotes too
            ("null", ""),
            ("proposed # draft | proposed | accepted", "proposed"),
            ("null # auto-filled by the workflow", ""),
            ("Add C# support", "Add C# support"),  # '#' with no space is kept
            ('"has # hash"', "has # hash"),  # '#' inside quotes is kept
            ("Foo # bar", "Foo"),  # whitespace-preceded '#' is a comment
        ],
    )
    def test_load_value(self, raw: str, expected: str) -> None:
        assert rfc._load_value(raw) == expected

    def test_dump_value_quotes_zero_padded_ids(self) -> None:
        assert rfc._dump_value("0006") == '"0006"'

    def test_dump_value_leaves_plain_words(self) -> None:
        assert rfc._dump_value("mixin") == "mixin"

    def test_dump_value_empty_is_null(self) -> None:
        assert rfc._dump_value("") == "null"

    def test_id_survives_round_trip(self) -> None:
        assert rfc._load_value(rfc._dump_value("0006")) == "0006"
        assert rfc._load_value(rfc._dump_value("")) == ""


class TestRfcParsing:
    def test_roundtrip_is_byte_identical(self, tmp_path: Path) -> None:
        path = _write_rfc(tmp_path, "0001", extra_body="Body with a\n\n---\n\nrule.\n")
        original = path.read_text(encoding="utf-8")
        parsed = rfc.Rfc(path)
        rebuilt = "---\n" + "\n".join(parsed.fm_lines) + "\n---\n\n" + parsed.body
        assert rebuilt == original

    def test_missing_frontmatter_raises(self, tmp_path: Path) -> None:
        path = tmp_path / "bad.md"
        path.write_text("no frontmatter here\n", encoding="utf-8")
        with pytest.raises(ValueError, match="missing frontmatter"):
            rfc.Rfc(path)

    def test_truncated_frontmatter_raises(self, tmp_path: Path) -> None:
        path = tmp_path / "bad.md"
        path.write_text('---\nrfc: "0001"\nno closing fence\n', encoding="utf-8")
        with pytest.raises(ValueError, match="malformed frontmatter"):
            rfc.Rfc(path)

    def test_set_preserves_inline_comment(self, tmp_path: Path) -> None:
        path = tmp_path / "x.md"
        path.write_text(
            '---\nrfc: "0099"\n'
            "github_pr: null # auto-filled by the workflow\n"
            "---\n\nb\n",
            encoding="utf-8",
        )
        r = rfc.Rfc(path)
        assert r.set("github_pr", "71") is True
        r.write()
        assert "github_pr: 71 # auto-filled by the workflow" in path.read_text()

    def test_set_no_change_returns_false(self, tmp_path: Path) -> None:
        path = _write_rfc(tmp_path, "0001", status="accepted")
        r = rfc.Rfc(path)
        assert r.set("status", "accepted") is False

    def test_set_appends_absent_key(self, tmp_path: Path) -> None:
        path = _write_rfc(tmp_path, "0001")
        r = rfc.Rfc(path)
        assert r.set("brand_new_key", "value") is True
        r.write()
        assert "brand_new_key: value" in path.read_text()

    def test_rejection_reason_extracted(self, tmp_path: Path) -> None:
        path = _write_rfc(
            tmp_path,
            "0001",
            status="rejected",
            extra_body="## Rejection Reason\n\n> a note\n\nToo niche to standardise.\n",
        )
        assert rfc.Rfc(path).rejection_reason() == "Too niche to standardise."

    def test_rejection_reason_absent_is_empty(self, tmp_path: Path) -> None:
        path = _write_rfc(tmp_path, "0001", status="rejected")
        assert rfc.Rfc(path).rejection_reason() == ""


class TestSetStatus:
    def test_stamps_status_and_pr(self, tmp_path: Path) -> None:
        path = _write_rfc(tmp_path, "0001", status="proposed")
        code = rfc.main(
            ["set-status", "--status", "accepted", "--pr", "71", str(path)],
        )
        assert code == 0
        r = rfc.Rfc(path)
        assert r.status == "accepted"
        assert r.get("github_pr") == "71"

    def test_is_idempotent(self, tmp_path: Path) -> None:
        path = _write_rfc(tmp_path, "0001", status="proposed")
        argv = ["set-status", "--status", "accepted", str(path)]
        rfc.main(argv)
        after_first = path.read_text(encoding="utf-8")
        rfc.main(argv)
        assert path.read_text(encoding="utf-8") == after_first

    def test_does_not_overwrite_existing_pr(self, tmp_path: Path) -> None:
        path = _write_rfc(tmp_path, "0001")
        rfc.main(["set-status", "--status", "accepted", "--pr", "10", str(path)])
        rfc.main(["set-status", "--status", "accepted", "--pr", "99", str(path)])
        assert rfc.Rfc(path).get("github_pr") == "10"

    def test_reserved_file_skipped(self, tmp_path: Path) -> None:
        reserved = tmp_path / "TEMPLATE.md"
        original = "---\nrfc: x\n---\n\nb\n"
        reserved.write_text(original, encoding="utf-8")
        code = rfc.main(["set-status", "--status", "accepted", str(reserved)])
        assert code == 0
        assert reserved.read_text(encoding="utf-8") == original  # untouched

    def test_missing_file_is_error(self, tmp_path: Path) -> None:
        missing = tmp_path / "0404-gone.md"
        code = rfc.main(["set-status", "--status", "accepted", str(missing)])
        assert code == 1


class TestSyncSupersedes:
    def _run(self, monkeypatch: pytest.MonkeyPatch, directory: Path) -> int:
        monkeypatch.setattr(rfc, "RFC_DIR", directory)
        return rfc.main(["sync-supersedes", "--date", "2026-07-06"])

    def test_accepted_rfc_retires_target(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        _write_rfc(tmp_path, "0002", status="accepted")
        _write_rfc(tmp_path, "0003", status="accepted", supersedes='"0002"')
        assert self._run(monkeypatch, tmp_path) == 0
        old = rfc.Rfc(tmp_path / "0002-example.md")
        assert old.status == "superseded"
        assert old.get("superseded_by") == "0003"

    def test_non_accepted_replacement_does_not_retire(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        _write_rfc(tmp_path, "0002", status="accepted")
        _write_rfc(tmp_path, "0003", status="rejected", supersedes='"0002"')
        assert self._run(monkeypatch, tmp_path) == 0
        assert rfc.Rfc(tmp_path / "0002-example.md").status == "accepted"

    def test_nonexistent_target_is_error(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        _write_rfc(tmp_path, "0003", status="accepted", supersedes='"0099"')
        assert self._run(monkeypatch, tmp_path) == 1


class TestGenerateIndex:
    def test_buckets_by_status(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        _write_rfc(tmp_path, "0001", status="accepted", title="Kept")
        _write_rfc(tmp_path, "0002", status="rejected", title="Nope")
        _write_rfc(
            tmp_path,
            "0003",
            status="superseded",
            title="Old",
        )
        monkeypatch.setattr(rfc, "RFC_DIR", tmp_path)
        index = rfc.generate_index()
        assert "## Active RFCs" in index
        assert "Kept" in index
        assert "Nope" in index
        assert "Old" in index
        # last-updated is the max ISO date across files
        assert "Last updated: 2026-01-01" in index

    def test_empty_dir_renders_placeholders(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(rfc, "RFC_DIR", tmp_path)
        index = rfc.generate_index()
        assert "_None yet._" in index
        assert "Last updated: —" in index
