#!/usr/bin/env python3
"""Install local skills or build a CC Switch ZIP. Python 3.10+, standard library only."""
import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import zipfile

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parent.parent
SKILLS = ("ingchips-docs",)
# Paths follow the linked upstream documentation in README.md (2026-10-23).
TARGETS = {
    "codex": (".agents/skills", ".agents/skills"),
    "claude-code": (".claude/skills", ".claude/skills"),
    "cursor": (".agents/skills", ".cursor/skills"),
    "gemini-cli": (".agents/skills", ".gemini/skills"),
    "opencode": (".agents/skills", ".config/opencode/skills"),
    "github-copilot": (".agents/skills", ".copilot/skills"),
}
TOP_LEVEL = {"SKILL.md", "INDEX.md", "catalog.json", "sources.json", "guides", "scripts",
             "references", "agents", "LICENSE", "NOTICE", "licenses"}
REQUIRED = {"SKILL.md", "INDEX.md", "catalog.json", "sources.json", "LICENSE", "NOTICE",
            "licenses/FreeRTOS-CC-BY-SA-4.0.txt",
            "scripts/search_docs.py", "scripts/read_excerpt.py", "scripts/doclib.py"}


def is_link(path):
    # Windows junctions are reparse points, even when Path.is_symlink() is false.
    attrs = getattr(path.lstat(), "st_file_attributes", 0)
    return path.is_symlink() or bool(attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def files_under(root, source=False):
    result = {}
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in list(dirs):
            path = Path(directory) / name
            if is_link(path):
                raise ValueError(f"Refusing linked directory: {path}")
            if source and name in ("__pycache__", ".git", ".cache"):
                dirs.remove(name)
        for name in files:
            path = Path(directory) / name
            if is_link(path):
                raise ValueError(f"Refusing linked file: {path}")
            relative = path.relative_to(root).as_posix()
            if source:
                if path.suffix in (".pyc", ".pyo") or name in (".DS_Store", "Thumbs.db"):
                    continue
                if relative.split("/")[0] not in TOP_LEVEL:
                    raise ValueError(f"Unexpected skill content (not silently packaged): {relative}")
            result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def source_payload(skill):
    root = REPO / skill
    if not root.is_dir() or is_link(root):
        raise ValueError(f"Invalid source skill: {root}")
    files = files_under(root, source=True)
    missing = REQUIRED - files.keys()
    if missing:
        raise ValueError(f"Incomplete skill: {sorted(missing)}")
    data = json.loads((root / "catalog.json").read_text("utf-8"))
    for item in data["files"]:
        if files.get("references/" + item["path"]) != item["sha256"]:
            raise ValueError(f"Stale or missing corpus file: {item['path']}; maintainer must rebuild")
    return root, files


def target_root(agent, scope, project=None, home=None):
    home = home or Path.home()
    base = Path(project or Path.cwd()) if scope == "project" else home
    relative = TARGETS[agent][0 if scope == "project" else 1]
    return base / relative


def prepare_plan(skill, roots, replace=False):
    source, payload = source_payload(skill)
    plan, seen = [], set()
    for raw_root in roots:
        root = raw_root.expanduser().absolute()
        raw_dest = root / skill
        if raw_dest.exists() or raw_dest.is_symlink():
            if is_link(raw_dest):
                raise ValueError(f"Target is a link/junction; manage it with its original installer: {raw_dest}")
            if not raw_dest.is_dir():
                raise ValueError(f"Target is not a directory: {raw_dest}")
        dest = raw_dest.resolve()
        if dest in seen:
            continue
        seen.add(dest)
        src = source.resolve()
        if dest == src or dest.is_relative_to(src) or src.is_relative_to(dest):
            raise ValueError(f"Source and installation must be separate: {dest}")
        action = "install"
        if dest.exists():
            if files_under(dest) == payload:
                action = "unchanged"
            elif not replace:
                raise ValueError(f"Existing skill differs: {dest}; use --replace to back it up and replace")
            else:
                action = "replace"
        plan.append(dict(destination=dest, action=action))
    return source, payload, plan


def execute_install(source, payload, plan):
    records = []
    with ExitStack() as stack:
        prepared = []
        # Finish every copy before replacing any installed directory.
        for item in plan:
            if item["action"] == "unchanged":
                continue
            dest = item["destination"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            stage_parent = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix=".ingchips-install-", dir=dest.parent)))
            stage = stage_parent / source.name
            stage.mkdir()
            for relative in sorted(payload):
                path = stage / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source / relative, path)
            if files_under(stage) != payload:
                raise ValueError("Source changed during installation; no installation was published")
            prepared.append((item, stage))
        try:
            for item, stage in prepared:
                dest = item["destination"]
                backup = None
                if item["action"] == "replace":
                    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
                    backup = dest.parent.parent / ".ingchips-skill-backups" / f"{source.name}-{stamp}"
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    dest.rename(backup)
                records.append(dict(destination=dest, backup=backup, stage=stage, installed=False))
                # Reject another process creating the destination after preflight.
                if dest.exists() or dest.is_symlink():
                    raise ValueError(f"Target appeared during installation: {dest}")
                stage.rename(dest)
                records[-1]["installed"] = True
        except BaseException:
            for record in reversed(records):
                if record["installed"]:
                    record["destination"].rename(record["stage"])
                if record["backup"] is not None:
                    record["backup"].rename(record["destination"])
            raise
    return records


def package(skill, output, replace=False):
    source, payload = source_payload(skill)
    raw_output = output.expanduser().absolute()
    if (raw_output.exists() or raw_output.is_symlink()) and is_link(raw_output):
        raise ValueError(f"Refusing linked ZIP output: {raw_output}")
    output = raw_output.resolve()
    if output.suffix.lower() != ".zip" or output.is_relative_to(source.resolve()):
        raise ValueError("ZIP output must end in .zip and be outside the source skill")
    checksum = output.with_suffix(output.suffix + ".sha256")
    if checksum.is_symlink() or (checksum.exists() and is_link(checksum)):
        raise ValueError(f"Refusing linked checksum: {checksum}")
    if (output.exists() or checksum.exists()) and not replace:
        raise ValueError(f"Package exists: {output}; use --replace to rebuild")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".ingchips-package-", dir=output.parent) as td:
        staged = Path(td) / output.name
        with zipfile.ZipFile(staged, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for relative in sorted(payload):
                info = zipfile.ZipInfo(f"{skill}/{relative}", date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                data = (source / relative).read_bytes()
                if hashlib.sha256(data).hexdigest() != payload[relative]:
                    raise ValueError("Source changed during packaging")
                archive.writestr(info, data)
        digest = hashlib.sha256(staged.read_bytes()).hexdigest()
        staged.replace(output)
        checksum.write_text(f"{digest}  {output.name}\n", encoding="ascii")
    return output, digest, len(payload)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("targets", help="print supported project/user directories")
    install = sub.add_parser("install", help="copy a skill; no network or application config changes")
    install.add_argument("--skill", choices=SKILLS, default=SKILLS[0])
    selection = install.add_mutually_exclusive_group(required=True)
    selection.add_argument("--agent", choices=sorted(TARGETS), nargs="+")
    selection.add_argument("--dest", type=Path, help="custom skills container; skill name is appended")
    install.add_argument("--scope", choices=("project", "global"), default="project")
    install.add_argument("--project", type=Path, help="project root; defaults to current directory")
    install.add_argument("--dry-run", action="store_true")
    install.add_argument("--replace", action="store_true", help="back up a different installed directory before replacement")
    pack = sub.add_parser("package", help="create a skill-only ZIP for CC Switch")
    pack.add_argument("--skill", choices=SKILLS, default=SKILLS[0])
    pack.add_argument("--output", type=Path, default=REPO / "dist" / "ingchips-docs.zip")
    pack.add_argument("--replace", action="store_true")
    args = ap.parse_args()
    try:
        if args.command == "targets":
            for name, (project, user) in TARGETS.items():
                print(f"{name:16} project={project}  global=~/{user}")
            print("Custom directories: install --dest <skills-directory>. CC Switch: package, then import ZIP in its UI.")
        elif args.command == "package":
            path, digest, count = package(args.skill, args.output, args.replace)
            print(f"ZIP: {path}\nSHA256: {digest}\nFiles: {count}")
        else:
            if args.project and (args.scope != "project" or args.dest):
                raise ValueError("--project requires --agent and --scope project")
            if args.dest and args.scope != "project":
                raise ValueError("--dest is explicit; do not combine it with --scope global")
            roots = [args.dest] if args.dest else [target_root(a, args.scope, args.project) for a in args.agent]
            source, payload, plan = prepare_plan(args.skill, roots, args.replace)
            for item in plan:
                print(f"{item['action']}: {item['destination']}")
            print(f"Payload: {len(payload)} files; copy only {args.skill}/")
            if args.dry_run:
                print("Dry run: no files written.")
            else:
                for record in execute_install(source, payload, plan):
                    if record['backup']:
                        print(f"Backup: {record['backup']}")
                print("Done. Refresh skills or start a new agent session.")
    except (OSError, ValueError) as exc:
        ap.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
