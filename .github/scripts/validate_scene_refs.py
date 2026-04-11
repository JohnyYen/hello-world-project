#!/usr/bin/env python3
"""Validate that all script references in .tscn scene files point to existing .gd files."""

import os
import re
import sys
from pathlib import Path


def find_tscn_files(root_dir: str) -> list[str]:
    """Find all .tscn files recursively."""
    tscn_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".tscn"):
                tscn_files.append(os.path.join(dirpath, filename))
    return tscn_files


def extract_script_refs(tscn_path: str) -> list[str]:
    """Extract res:// paths from script references in a .tscn file."""
    refs = []
    with open(tscn_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Match ext_resource script paths: path="res://..."
    pattern = r'\[ext_resource[^]]*type="Script"[^]]*path="(res://[^"]+)"'
    for match in re.finditer(pattern, content):
        refs.append(match.group(1))

    # Also match inline script references: script = ExtResource("...")
    # These are already captured by ext_resource above
    return refs


def validate_scene_refs(game_dir: str) -> tuple[bool, list[str]]:
    """
    Validate all script references in .tscn files point to existing .gd files.

    Returns:
        (is_valid, errors)
    """
    errors = []
    tscn_files = find_tscn_files(game_dir)

    if not tscn_files:
        print(f"WARNING: No .tscn files found in {game_dir}")
        return True, errors

    print(f"Checking {len(tscn_files)} scene files...")

    for tscn_path in tscn_files:
        rel_path = os.path.relpath(tscn_path, game_dir)
        script_refs = extract_script_refs(tscn_path)

        if not script_refs:
            continue

        for res_path in script_refs:
            # Skip addon references - addons are installed separately, not committed
            if res_path.startswith("res://addons/"):
                continue

            # Convert res:// to actual file path
            file_path = res_path.replace("res://", game_dir + "/")

            # Check if the file exists
            if not os.path.exists(file_path):
                errors.append(f"  MISSING: {rel_path} references {res_path}")

    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_scene_refs.py <game_directory>")
        print("Example: python validate_scene_refs.py apps/game/")
        sys.exit(1)

    game_dir = sys.argv[1]

    if not os.path.isdir(game_dir):
        print(f"ERROR: Directory not found: {game_dir}")
        sys.exit(1)

    print(f"Validating scene script references in: {game_dir}")
    is_valid, errors = validate_scene_refs(game_dir)

    if is_valid:
        print("All scene script references are valid.")
        sys.exit(0)
    else:
        print(f"\nFound {len(errors)} broken script reference(s):")
        for error in errors:
            print(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
