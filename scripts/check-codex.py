#!/usr/bin/env python3
"""Check discovery links and exercise installation without touching user settings."""
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
skills = root / '.agents/skills'
for skill in skills.iterdir():
    assert (skill / 'SKILL.md').is_file(), f'Broken skill: {skill}'
    if skill.is_symlink():
        assert not Path(skill.readlink()).is_absolute(), f'Nonportable link: {skill}'
        assert skill.resolve().is_relative_to(root), f'Link escapes toolbox: {skill}'
    text = (skill / 'SKILL.md').read_text()
    assert text.startswith('---\n'), f'Missing metadata: {skill}'
    front = text.split('---', 2)[1]
    assert '\nname:' in front and '\ndescription:' in front, skill

with tempfile.TemporaryDirectory(prefix='codex-toolbox-') as temp:
    target = Path(temp) / 'project with spaces'
    command = [sys.executable, str(root / 'scripts/install-codex-skills.py'), '--target', str(target)]
    def run(*extra, success=True):
        result = subprocess.run(command + list(extra), capture_output=True, text=True)
        assert (result.returncode == 0) == success, result.stderr
        return result
    run('--dry-run')
    assert not target.exists(), 'Dry run wrote files'
    run()
    installed = target / '.agents/skills'
    assert len(list(installed.iterdir())) == len(list(skills.iterdir()))
    for item in installed.iterdir():
        assert (item / 'SKILL.md').is_file(), item
    assert 'LINK ' not in run().stdout, 'Repeat install was not idempotent'
    run('--skill', 'missing-skill', success=False)
    conflict = installed / 'graphify'
    conflict.unlink()
    conflict.mkdir()
    (conflict / 'keep.txt').write_text('preserve me')
    pending = installed / 'api-design'
    pending.unlink()
    run(success=False)
    assert (conflict / 'keep.txt').read_text() == 'preserve me'
    assert not pending.exists(), 'Conflict caused a partial install'
    run('--skill', 'api-design')
    assert (pending / 'SKILL.md').is_file()
print(f'PASS: {len(list(skills.iterdir()))} skills; dry run, install, repeat, selection and conflict protection')
