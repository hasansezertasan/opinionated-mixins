#!/usr/bin/env python3
"""RFC tooling: frontmatter status sync and INDEX.md generation.

Dependency-free by design (stdlib only) so it runs in CI without an install
step and matches the project's zero-runtime-dependency philosophy.

Subcommands
-----------
``index``            Regenerate ``docs/rfcs/INDEX.md`` from all RFC frontmatters.
``set-status``       Write a status (from a merged PR's label) into RFC files.
``sync-supersedes``  Flip any RFC pointed at by another RFC's ``supersedes``
                     to ``superseded`` and back-link ``superseded_by``.

The frontmatter is intentionally *flat* (``key: value`` pairs only), so a tiny
line-based parser is enough — no YAML dependency required.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RFC_DIR = Path(__file__).resolve().parent.parent / "docs" / "rfcs"
RESERVED = {"TEMPLATE.md", "README.md", "INDEX.md"}

ACTIVE_STATUSES = ("accepted", "proposed")
CLOSED_STATUSES = ("rejected", "deferred", "withdrawn")

_FRONTMATTER_PARTS = 3  # leading "", frontmatter, body
_MIN_QUOTED_LEN = 2  # opening + closing quote

TYPE_ORDER = ("mixin", "field", "framework", "breaking-change")
TYPE_LABELS = {
    "mixin": "Mixin RFCs",
    "field": "Field RFCs",
    "framework": "Framework RFCs",
    "breaking-change": "Breaking-change RFCs",
}


class Rfc:
    """A parsed RFC file: ordered frontmatter lines plus the markdown body."""

    def __init__(self, path: Path) -> None:
        self.path = path
        text = path.read_text(encoding="utf-8")
        self.fm_lines, self.body = _split_frontmatter(text, path)
        self.meta = _parse_frontmatter(self.fm_lines)

    # -- accessors -----------------------------------------------------------
    def get(self, key: str, default: str = "") -> str:
        return self.meta.get(key, default)

    @property
    def rfc(self) -> str:
        return self.get("rfc")

    @property
    def status(self) -> str:
        return self.get("status")

    # -- mutation ------------------------------------------------------------
    def set(self, key: str, value: str) -> bool:
        """Set ``key`` to ``value`` in the frontmatter. Returns True if changed."""
        if self.meta.get(key) == value:
            return False
        self.meta[key] = value
        for i, line in enumerate(self.fm_lines):
            m = re.match(rf"^(\s*{re.escape(key)}\s*:\s*)(.*?)(\s*#.*)?$", line)
            if m:
                comment = m.group(3) or ""
                self.fm_lines[i] = f"{m.group(1)}{_dump_value(value)}{comment}"
                return True
        # key absent — append before the closing block
        self.fm_lines.append(f"{key}: {_dump_value(value)}")
        return True

    def write(self) -> None:
        text = "---\n" + "\n".join(self.fm_lines) + "\n---\n\n" + self.body
        self.path.write_text(text, encoding="utf-8")

    def rejection_reason(self) -> str:
        """First non-empty line under a ``## Rejection Reason`` / ``## Reason``."""
        m = re.search(
            r"^##\s+(?:Rejection Reason|Reason)\s*$(.*?)(?=^##\s|\Z)",
            self.body,
            re.MULTILINE | re.DOTALL,
        )
        if not m:
            return ""
        for raw in m.group(1).splitlines():
            line = raw.strip()
            if line and not line.startswith(">"):
                return line
        return ""


# -- frontmatter primitives --------------------------------------------------
def _split_frontmatter(text: str, path: Path) -> tuple[list[str], str]:
    if not text.startswith("---"):
        msg = f"{path}: missing frontmatter block"
        raise ValueError(msg)
    parts = text.split("---", 2)
    if len(parts) < _FRONTMATTER_PARTS:
        msg = f"{path}: malformed frontmatter block"
        raise ValueError(msg)
    fm_lines = parts[1].strip("\n").splitlines()
    body = parts[2].lstrip("\n")
    return fm_lines, body


def _parse_frontmatter(lines: list[str]) -> dict[str, str]:
    meta: dict[str, str] = {}
    for line in lines:
        m = re.match(r"^\s*([A-Za-z0-9_]+)\s*:\s*(.*?)(\s*#.*)?$", line)
        if m:
            meta[m.group(1)] = _load_value(m.group(2))
    return meta


def _load_value(raw: str) -> str:
    raw = raw.strip()
    quoted = len(raw) >= _MIN_QUOTED_LEN and raw[0] in "\"'" and raw[-1] == raw[0]
    if quoted:
        return raw[1:-1]
    if raw == "null":
        return ""
    return raw


def _dump_value(value: str) -> str:
    if value == "":
        return "null"
    # keep zero-padded numeric ids quoted so YAML preserves them as strings
    if value.isdigit() and value.startswith("0"):
        return f'"{value}"'
    return value


# -- loading -----------------------------------------------------------------
def load_rfcs() -> list[Rfc]:
    rfcs = [Rfc(p) for p in sorted(RFC_DIR.glob("*.md")) if p.name not in RESERVED]
    return sorted(rfcs, key=lambda r: r.rfc)


# -- index generation --------------------------------------------------------
def _link(r: Rfc) -> str:
    return f"[{r.rfc}]({r.path.name})"


def generate_index() -> str:
    rfcs = load_rfcs()
    updated_dates = [r.get("updated") for r in rfcs if r.get("updated")]
    last_updated = max(updated_dates) if updated_dates else "—"

    active = [r for r in rfcs if r.status in ACTIVE_STATUSES]
    closed = [r for r in rfcs if r.status in CLOSED_STATUSES]
    superseded = [r for r in rfcs if r.status == "superseded"]

    out: list[str] = []
    out.append("# RFC Index")
    out.append("")
    out.append(
        "<!-- Auto-generated by scripts/rfc.py — do not edit by hand. "
        "See README.md for the RFC process. -->",
    )
    out.append("")
    out.append(f"Last updated: {last_updated}")
    out.append("")

    out.append("## Active RFCs")
    out.append("")
    if active:
        out.append("| RFC | Title | Type | Status | Created | Author |")
        out.append("| --- | ----- | ---- | ------ | ------- | ------ |")
        out.extend(
            f"| {_link(r)} | {r.get('title')} | {r.get('type')} | "
            f"{r.status} | {r.get('created')} | {r.get('author')} |"
            for r in active
        )
    else:
        out.append("_None yet._")
    out.append("")

    out.append("## Rejected / Deferred / Withdrawn")
    out.append("")
    if closed:
        out.append("| RFC | Title | Type | Status | Reason |")
        out.append("| --- | ----- | ---- | ------ | ------ |")
        out.extend(
            f"| {_link(r)} | {r.get('title')} | {r.get('type')} | "
            f"{r.status} | {r.rejection_reason()} |"
            for r in closed
        )
    else:
        out.append("_None yet._")
    out.append("")

    out.append("## Superseded")
    out.append("")
    if superseded:
        out.append("| RFC | Title | Superseded By |")
        out.append("| --- | ----- | ------------- |")
        for r in superseded:
            by = r.get("superseded_by")
            by_link = f"[{by}]({_filename_for(rfcs, by)})" if by else "—"
            out.append(f"| {_link(r)} | {r.get('title')} | {by_link} |")
    else:
        out.append("_None yet._")
    out.append("")

    out.append("## By Type")
    out.append("")
    for t in TYPE_ORDER:
        nums = [r.rfc for r in rfcs if r.get("type") == t]
        listing = ", ".join(nums) if nums else "(none yet)"
        out.append(f"- **{TYPE_LABELS[t]}**: {listing}")
    out.append("")

    return "\n".join(out)


def _filename_for(rfcs: list[Rfc], number: str) -> str:
    for r in rfcs:
        if r.rfc == number:
            return r.path.name
    return "#"


# -- commands ----------------------------------------------------------------
def cmd_index(_args: argparse.Namespace) -> int:
    (RFC_DIR / "INDEX.md").write_text(generate_index(), encoding="utf-8")
    print(f"Wrote {RFC_DIR / 'INDEX.md'}")
    return 0


def cmd_set_status(args: argparse.Namespace) -> int:
    changed = 0
    for file in args.files:
        path = Path(file)
        if path.name in RESERVED or not path.exists():
            print(f"skip {file}")
            continue
        r = Rfc(path)
        dirty = r.set("status", args.status)
        if args.date:
            dirty |= r.set("updated", args.date)
        if args.pr and not r.get("github_pr"):
            dirty |= r.set("github_pr", args.pr)
        if dirty:
            r.write()
            changed += 1
            print(f"updated {path.name} -> status={args.status}")
    print(f"{changed} file(s) updated")
    return 0


def cmd_sync_supersedes(args: argparse.Namespace) -> int:
    rfcs = load_rfcs()
    by_number = {r.rfc: r for r in rfcs}
    changed = 0
    for r in rfcs:
        target = r.get("supersedes")
        if target and target in by_number:
            old = by_number[target]
            dirty = old.set("status", "superseded")
            dirty |= old.set("superseded_by", r.rfc)
            if args.date:
                dirty |= old.set("updated", args.date)
            if dirty:
                old.write()
                changed += 1
                print(f"{old.path.name} -> superseded by {r.rfc}")
    print(f"{changed} file(s) updated")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("index", help="regenerate INDEX.md").set_defaults(func=cmd_index)

    p_status = sub.add_parser("set-status", help="write status into RFC files")
    p_status.add_argument(
        "--status",
        required=True,
        choices=(*ACTIVE_STATUSES, *CLOSED_STATUSES),
    )
    p_status.add_argument("--pr", default="", help="PR number to stamp into github_pr")
    p_status.add_argument("--date", default="", help="ISO date for the updated field")
    p_status.add_argument("files", nargs="+", help="RFC files changed by the PR")
    p_status.set_defaults(func=cmd_set_status)

    p_sup = sub.add_parser("sync-supersedes", help="derive superseded statuses")
    p_sup.add_argument("--date", default="", help="ISO date for the updated field")
    p_sup.set_defaults(func=cmd_sync_supersedes)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
