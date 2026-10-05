from pathlib import Path

import pytest

from tools import build_docs
from tools.build_docs import inject_version_switcher


class TestInjectVersionSwitcher:
    def test_injects_relative_script_and_is_idempotent(self, tmp_path: Path) -> None:
        version_root = tmp_path / "0.3"
        nested = version_root / "guide"
        nested.mkdir(parents=True)
        script_source = tmp_path / "versions-switcher.js"
        script_source.write_text("// switcher", encoding="utf-8")
        page = nested / "index.html"
        page.write_text("<html><body><main></main></body></html>", encoding="utf-8")

        inject_version_switcher(version_root, script_source)
        inject_version_switcher(version_root, script_source)

        contents = page.read_text(encoding="utf-8")
        assert (
            '<script src="../_static/versions-switcher.js" defer></script>' in contents
        )
        assert contents.count("versions-switcher.js") == 1
        assert (
            version_root / "_static/versions-switcher.js"
        ).read_text() == "// switcher"

    def test_requires_a_body_tag(self, tmp_path: Path) -> None:
        version_root = tmp_path / "0.3"
        version_root.mkdir()
        script_source = tmp_path / "versions-switcher.js"
        script_source.write_text("// switcher", encoding="utf-8")
        (version_root / "index.html").write_text("<html></html>", encoding="utf-8")

        with pytest.raises(RuntimeError, match="no </body> tag"):
            inject_version_switcher(version_root, script_source)

    def test_refresh_updates_shared_manifest_on_preserved_versions(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        html_root = tmp_path / "html"
        source_static = html_root / "_static"
        source_static.mkdir(parents=True)
        (source_static / "versions-switcher.js").write_text("// live", encoding="utf-8")
        (source_static / "versions.json").write_text(
            '{"versions":["0.4","0.3"],"latest":"0.4"}', encoding="utf-8"
        )
        monkeypatch.setattr(build_docs, "HTML_DIR", html_root)

        site_root = tmp_path / "site"
        old_version = site_root / "0.3"
        (old_version / "guide").mkdir(parents=True)
        old_page = old_version / "guide" / "index.html"
        old_page.write_text("<html><body></body></html>", encoding="utf-8")
        latest_static = site_root / "latest" / "_static"
        latest_static.mkdir(parents=True)
        old_manifest = latest_static / "versions.json"
        old_manifest.write_text('{"versions":["0.3"],"latest":"0.3"}')

        build_docs.refresh_version_switchers(site_root, {"0.3", "latest"})

        assert "versions-switcher.js" in old_page.read_text(encoding="utf-8")
        assert old_manifest.read_text(encoding="utf-8") == (
            '{"versions":["0.4","0.3"],"latest":"0.4"}'
        )
