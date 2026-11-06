#!/usr/bin/env python3
"""Link this toolbox's skills into another project's Codex discovery directory."""
import argparse
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, required=True,
                        help='Project root (skills go into .agents/skills)')
    parser.add_argument('--skill', action='append', default=[], help='Install only this folder name; repeatable')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / '.agents' / 'skills'
    available = {p.name: p for p in sorted(source.iterdir()) if (p / 'SKILL.md').is_file()}
    unknown = set(args.skill) - available.keys()
    if unknown:
        parser.error('Unknown skills: ' + ', '.join(sorted(unknown)))
    destination = args.target.expanduser().resolve() / '.agents' / 'skills'
    selected = args.skill or list(available)
    conflicts = []
    planned = []
    for name in dict.fromkeys(selected):
        src = available[name].resolve()
        dst = destination / name
        if dst.is_symlink() and dst.resolve() == src:
            print(f'OK {name}')
        elif os.path.lexists(dst):
            conflicts.append(name)
        else:
            planned.append((src, dst))
    if conflicts:
        parser.error('Existing skills were not changed: ' + ', '.join(conflicts))
    if not args.dry_run:
        destination.mkdir(parents=True, exist_ok=True)
    for src, dst in planned:
        print(f'{"WOULD LINK" if args.dry_run else "LINK"} {dst} -> {src}')
        if not args.dry_run:
            dst.symlink_to(os.path.relpath(src, dst.parent), target_is_directory=True)


if __name__ == '__main__':
    main()
