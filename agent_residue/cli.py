#!/usr/bin/env python3
"""agent-residue — find and clean leftovers from AI coding agents.

Dry-run by default. Cleaning quarantines by default; --purge deletes for real.
Targets live in targets.json so the catalog can grow without touching code.

Usage:
    agent-residue list
    agent-residue scan  [-a claude-code,codex] [--tier 1,2]
    agent-residue clean [...] [--purge --yes]
    agent-residue restore .agent-trash/20260101-120000/manifest.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

VERSION = "0.2.0"

TARGETS_FILE = Path(__file__).resolve().parent / "targets.json"
TRASH_DIR_NAME = ".agent-trash"

RE_PCT = re.compile(r"%([A-Za-z_][A-Za-z0-9_]*)%")
RE_ENV = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)")

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# --------------------------------------------------------------- catalog ---

def load_catalog(path: Path = TARGETS_FILE) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def expand(template: str, home: Path) -> Path | None:
    """Resolve ~ and %VARS% / $VARS. Return None when a variable is missing."""
    text = template
    if text == "~" or text.startswith("~/") or text.startswith("~\\"):
        text = str(home) + text[1:]

    def pct(match: re.Match) -> str:
        value = os.environ.get(match.group(1))
        if value is None:
            raise KeyError(match.group(1))
        return value

    def env(match: re.Match) -> str:
        name = match.group(1) or match.group(2)
        value = os.environ.get(name)
        if value is None:
            raise KeyError(name)
        return value

    try:
        text = RE_PCT.sub(pct, text)
        text = RE_ENV.sub(env, text)
    except KeyError:
        return None
    return Path(text)


@dataclass
class Target:
    agent: str
    agent_name: str
    label: str
    tier: int
    note: str
    path: Path
    size: int = 0
    files: int = 0
    mtime: float = 0.0


def discover(
    catalog: dict,
    home: Path,
    agents: list[str] | None,
    tiers: set[int],
    include_unverified: bool,
    older_than: int = 0,
) -> tuple[list[Target], list[dict]]:
    wanted = set(agents) if agents else None
    rows: list[Target] = []
    skipped: list[dict] = []

    for agent in catalog["agents"]:
        aid = agent["id"]
        if wanted is not None and aid not in wanted and "all" not in wanted:
            continue
        if not agent.get("verified", False) and not include_unverified:
            skipped.append({"agent": aid, "reason": "unverified (use --include-unverified)"})
            continue
        for entry in agent["paths"]:
            template, tier, label = entry[0], int(entry[1]), entry[2]
            note = entry[3] if len(entry) > 3 else ""
            if tier not in tiers:
                continue
            path = expand(template, home)
            if path is None or not path.exists() or path.is_symlink():
                continue
            size, files, mtime = path_stats(path)
            if older_than and mtime and mtime > time.time() - older_than * 86400:
                continue
            rows.append(
                Target(aid, agent["name"], label, tier, note, path, size, files, mtime)
            )
    return rows, skipped


def path_stats(path: Path) -> tuple[int, int, float]:
    if path.is_file():
        st = path.stat()
        return st.st_size, 1, st.st_mtime

    total = 0
    files = 0
    newest = 0.0
    stack = [str(path)]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    try:
                        st = entry.stat(follow_symlinks=False)
                    except OSError:
                        continue
                    newest = max(newest, st.st_mtime)
                    if entry.is_dir(follow_symlinks=False):
                        stack.append(entry.path)
                    elif entry.is_file(follow_symlinks=False):
                        total += st.st_size
                        files += 1
        except OSError:
            continue
    return total, files, newest


def human(size: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:,.1f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024.0
    return f"{size:.1f} TB"


# --------------------------------------------------------------- runtime ---

def running_processes(names: list[str]) -> list[str]:
    if not names:
        return []
    lowered = {n.lower() for n in names}
    found: list[str] = []
    try:
        import psutil  # optional, nicer when installed

        for proc in psutil.process_iter(["name"]):
            name = (proc.info.get("name") or "").lower()
            if name.removesuffix(".exe") in lowered:
                found.append(name)
        return sorted(set(found))
    except Exception:
        pass
    try:
        if os.name == "nt":
            out = subprocess.run(
                ["tasklist", "/FO", "CSV", "/NH"],
                capture_output=True, text=True, timeout=20, check=False,
            ).stdout
            for line in out.splitlines():
                if line.startswith('"'):
                    name = line.split('","')[0].strip('"').lower()
                    if name.removesuffix(".exe") in lowered:
                        found.append(name)
        else:
            out = subprocess.run(
                ["ps", "-A", "-o", "comm="],
                capture_output=True, text=True, timeout=20, check=False,
            ).stdout
            for line in out.splitlines():
                name = os.path.basename(line.strip()).lower()
                if name.removesuffix(".exe") in lowered:
                    found.append(name)
    except Exception:
        pass
    return sorted(set(found))


def guard(path: Path, home: Path) -> None:
    """Refuse anything that is not a deep path inside the user's home."""
    resolved = path.resolve()
    if len(resolved.parts) < 4:
        raise SystemExit(f"refusing shallow path: {resolved}")
    if resolved == home or resolved == Path(resolved.anchor):
        raise SystemExit(f"refusing to touch {resolved}")
    if not resolved.is_relative_to(home.resolve()):
        raise SystemExit(f"refusing path outside home: {resolved}")


def long_path(path: Path) -> str:
    text = str(path)
    if os.name == "nt" and len(text) >= 240 and not text.startswith("\\\\?\\"):
        return "\\\\?\\" + text
    return text


def remove_tree(path: Path) -> None:
    def on_error(func, target, exc_info):  # chmod then retry once
        try:
            os.chmod(target, 0o700)
            func(target)
        except Exception:
            raise

    if path.is_dir():
        shutil.rmtree(long_path(path), onerror=on_error)
    else:
        path.unlink()


# ------------------------------------------------------------------ output ---

def print_rows(rows: list[Target], catalog: dict) -> None:
    names = {a["id"]: a["name"] for a in catalog["agents"]}
    if not rows:
        print("nothing found for the selected tiers.")
        return
    width = max([len("AGENT")] + [len(names.get(r.agent, r.agent)) for r in rows]) + 2
    header = f"{'AGENT':<{width}}{'TIER':>5}{'SIZE':>12}{'FILES':>8}  {'LAST':<11}PATH"
    print(header)
    print("-" * len(header))
    for row in sorted(rows, key=lambda r: (-r.size, r.agent)):
        last = time.strftime("%Y-%m-%d", time.localtime(row.mtime)) if row.mtime else "-"
        name = names.get(row.agent, row.agent)
        print(f"{name:<{width}}{row.tier:>5}{human(row.size):>12}{row.files:>8}  {last:<11}{row.path}")


# ------------------------------------------------------------------ actions ---

def do_clean(rows, dest_root: Path, purge: bool, yes: bool, home: Path) -> tuple[list, list]:
    moved, failed = [], []
    batch = None if purge else dest_root / time.strftime("%Y%m%d-%H%M%S")
    if batch:
        batch.mkdir(parents=True, exist_ok=True)

    for index, row in enumerate(sorted(rows, key=lambda r: -r.size), start=1):
        try:
            guard(row.path, home)
        except SystemExit as exc:
            failed.append({"path": str(row.path), "error": str(exc)})
            continue
        try:
            if purge:
                remove_tree(row.path)
                print(f"  [del] {human(row.size):>10}  {row.path}")
            else:
                safe_label = re.sub(r"[^\w.-]+", "_", row.label)
                target = batch / f"{index:02d}-{row.agent}-{safe_label}"
                shutil.move(str(row.path), str(target))
                print(f"  [mv ] {human(row.size):>10}  {row.path}")
                moved.append(
                    {
                        "agent": row.agent,
                        "label": row.label,
                        "tier": row.tier,
                        "original": str(row.path),
                        "quarantined": str(target),
                        "bytes": row.size,
                    }
                )
        except Exception as exc:
            failed.append({"path": str(row.path), "error": str(exc)})
            print(f"  [fail] {row.path}: {exc}", file=sys.stderr)
    return moved, failed


def write_manifest(entries, batch: Path) -> Path:
    if os.name == "nt":
        host = os.environ.get("COMPUTERNAME", "")
    else:
        host = os.uname().nodename
    manifest = {
        "tool": "agent-residue",
        "version": VERSION,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "host": host,
        "entries": entries,
    }
    path = batch / "manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def do_restore(manifest_path: Path) -> int:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    restored = 0
    for entry in data["entries"]:
        source = Path(entry["quarantined"])
        target = Path(entry["original"])
        if not source.exists():
            print(f"skip (gone): {source}", file=sys.stderr)
            continue
        if target.exists():
            print(f"skip (occupied): {target}", file=sys.stderr)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(target))
        restored += 1
        print(f"  [back] {target}")
    return restored


# --------------------------------------------------------------------- cli ---

def parse_tiers(text: str) -> set[int]:
    tiers = set()
    for part in str(text).replace(" ", "").split(","):
        if not part:
            continue
        value = int(part)
        if value not in (0, 1, 2, 3):
            raise SystemExit(f"invalid tier: {value}")
        tiers.add(value)
    return tiers


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-residue",
        description="Find and clean leftovers from AI coding agents (dry-run by default).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    sub = parser.add_subparsers(dest="command")

    p_list = sub.add_parser("list", help="show supported agents and their paths")
    p_list.add_argument("--json", action="store_true")

    def add_common(p):
        p.add_argument("-a", "--agents", default="", help="comma separated ids, or 'all'")
        p.add_argument("--tier", default="1", help="comma separated tiers (default 1)")
        p.add_argument("--include-unverified", action="store_true")
        p.add_argument("--older-than", type=int, default=0, metavar="DAYS")
        p.add_argument("--exclude", action="append", default=[], metavar="PATTERN")
        p.add_argument("--home", default=str(Path.home()), metavar="DIR")
        p.add_argument("--json", action="store_true")

    p_scan = sub.add_parser("scan", help="report what could be reclaimed (read-only)")
    add_common(p_scan)

    p_clean = sub.add_parser("clean", help="quarantine (default) or delete the selected targets")
    add_common(p_clean)
    p_clean.add_argument("--purge", action="store_true", help="delete instead of quarantine")
    p_clean.add_argument("--yes", action="store_true", help="required with --purge")
    p_clean.add_argument("--quarantine", default="", metavar="DIR")
    p_clean.add_argument("--force", action="store_true", help="ignore running processes")

    p_restore = sub.add_parser("restore", help="undo a quarantine batch from its manifest.json")
    p_restore.add_argument("manifest")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 1

    catalog = load_catalog()

    if args.command == "list":
        if args.json:
            print(json.dumps(catalog, ensure_ascii=False, indent=2))
            return 0
        for agent in catalog["agents"]:
            mark = "verified" if agent.get("verified") else "unverified"
            print(f"{agent['id']:<16}{agent['name']:<22}{agent.get('vendor', ''):<14}{mark}")
            for entry in agent["paths"]:
                print(f"    T{entry[1]}  {entry[0]:<58}{entry[2]}")
        return 0

    if args.command == "restore":
        return 0 if do_restore(Path(args.manifest)) >= 0 else 1

    home = Path(args.home).expanduser()
    agents = [a.strip() for a in args.agents.split(",") if a.strip()] or None
    tiers = parse_tiers(args.tier)
    excludes = [e for e in args.exclude if e]

    rows, skipped = discover(
        catalog, home, agents, tiers, args.include_unverified, args.older_than
    )
    rows = [
        r for r in rows
        if not any(p.lower().strip("*") in r.label.lower() for p in excludes)
    ]

    if args.json:
        payload = {
            "version": VERSION,
            "agents": sorted({r.agent for r in rows}),
            "reclaimable": sum(r.size for r in rows),
            "targets": [
                {
                    "agent": r.agent, "label": r.label, "tier": r.tier,
                    "path": str(r.path), "bytes": r.size, "files": r.files,
                }
                for r in rows
            ],
            "skipped": skipped,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        if args.command == "clean":
            if not rows:
                return 0
            if args.purge and not args.yes:
                print("refusing to purge without --yes", file=sys.stderr)
                return 2
            dest = Path(args.quarantine).expanduser() if args.quarantine else Path.cwd() / TRASH_DIR_NAME
            do_clean(rows, dest, args.purge, args.yes, home)
        return 0

    total = sum(r.size for r in rows)
    print(f"agent-residue {VERSION}   home={home}")
    print(f"selected tiers: {','.join(str(t) for t in sorted(tiers))}"
          f"   reclaimable: {human(total)}")
    print()
    print_rows(rows, catalog)

    for item in skipped:
        print(f"  skip {item['agent']}: {item['reason']}", file=sys.stderr)

    if args.command == "scan":
        return 0

    if not rows:
        print("\nnothing to clean.")
        return 0

    if args.purge and not args.yes:
        print("\nrefusing to purge without --yes (this is irreversible).", file=sys.stderr)
        return 2

    blocked = {}
    for agent in catalog["agents"]:
        if any(r.agent == agent["id"] for r in rows):
            names = agent.get("processes") or []
            hits = running_processes(names)
            if hits:
                blocked[agent["id"]] = hits
    if blocked and not args.force:
        print("\nrunning processes detected; quit the app first (or pass --force):", file=sys.stderr)
        for aid, hits in blocked.items():
            print(f"  {aid}: {', '.join(hits)}", file=sys.stderr)
        return 3

    print()
    dest = Path(args.quarantine).expanduser() if args.quarantine else Path.cwd() / TRASH_DIR_NAME
    moved, failed = do_clean(rows, dest, args.purge, args.yes, home)

    if args.purge:
        print(f"\nremoved {len(rows) - len(failed)} targets, {human(total)} reclaimed.")
    elif moved:
        manifest = write_manifest(moved, Path(moved[0]["quarantined"]).parent)
        print(f"\nquarantined {len(moved)} targets, {human(sum(m['bytes'] for m in moved))}.")
        print(f"undo: agent-residue restore {manifest}")
    if failed:
        print(f"{len(failed)} target(s) failed; see above.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

