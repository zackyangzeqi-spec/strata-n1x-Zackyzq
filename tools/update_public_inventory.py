#!/usr/bin/env python3
"""Rebuild PACKAGE.json files from the Git index, without staging or publishing.

Stage the intended public changes first. Run without --write to inspect changes,
then run with --write, review PACKAGE.json and stage it explicitly.
Only tracked index blobs are read; untracked files are never scanned or added.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write the working-tree manifest only")
    mode.add_argument("--check", action="store_true", help="read-only; return nonzero if inventory differs from index")
    args = parser.parse_args()
    root = Path(git(args.repo, "rev-parse", "--show-toplevel").decode().strip())
    manifest_path = root / "PACKAGE.json"
    if manifest_path.is_symlink():
        raise ValueError("PACKAGE.json must be a regular file")
    staged = git(root, "show", ":PACKAGE.json")
    # Preserve intentional metadata changes only after the owner has staged them.
    if manifest_path.read_bytes().replace(b"\r\n", b"\n") != staged.replace(b"\r\n", b"\n"):
        raise ValueError("PACKAGE.json has unstaged changes; review and stage it first")
    manifest = json.loads(staged)
    records = []
    for entry in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not entry:
            continue
        info, raw_path = entry.split(b"\t", 1)
        mode, object_id, stage = info.decode("ascii").split()
        path = raw_path.decode("utf-8")
        if stage != "0":
            raise ValueError("Resolve index conflict first: " + path)
        if mode not in ("100644", "100755"):
            raise ValueError("Unsupported link/submodule entry: " + path)
        if path == "PACKAGE.json":
            continue
        data = git(root, "cat-file", "blob", object_id)
        records.append({"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    records.sort(key=lambda item: item["path"].casefold())
    previous = {item["path"]: item for item in manifest.get("files", [])}
    current = {item["path"]: item for item in records}
    changed = sorted(path for path in current if previous.get(path) != current[path])
    removed = sorted(set(previous) - set(current))
    print(json.dumps({"tracked_files": len(records), "changed_or_added": changed,
                      "removed_from_index": removed, "write": args.write, "check": args.check}, ensure_ascii=False, indent=2))
    if args.check:
        if changed or removed or len(previous) != len(manifest.get("files", [])):
            raise ValueError("PACKAGE.json does not match the current Git index")
        print("PASS: public file inventory matches the current Git index.")
        return
    manifest["files"] = records
    if "visibility_update" in manifest:
        manifest["visibility_update"]["inventory_basis"] = (
            "Final staged Git index bytes; PACKAGE.json excluded from its own file list.")
    if args.write:
        manifest_path.write_bytes((json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        print("Wrote PACKAGE.json only. Review it, then git add PACKAGE.json.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print("Inventory update stopped: " + str(exc), file=sys.stderr)
        sys.exit(1)
