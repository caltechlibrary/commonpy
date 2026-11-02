#!/usr/bin/env python3
# =============================================================================
# @file    bump_version.py
# @brief   Increment the version number everywhere it is stored
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/caltechlibrary/commonpy
#
# Usage: dev/bump_version.py patch|minor|major|X.Y.Z
#
# Reads the current version from setup.cfg, computes the next one, writes it
# into setup.cfg, commonpy/__init__.py, codemeta.json, and CITATION.cff, sets
# date-released in CITATION.cff to today, and prints the new version. It
# changes nothing else and commits nothing. The "Release" workflow runs it,
# and it can be run by hand from the top of the repository.
#
# Edits are line-based substitutions rather than parse-and-rewrite, so the
# files keep their formatting (and codemeta.json need not be valid JSON).
# =============================================================================

from datetime import date
from os import path
import re
import sys

ROOT = path.dirname(path.dirname(path.abspath(__file__)))

# Each entry is a file and a pattern whose second group is the version.
VERSION_FIELDS = [
    ('setup.cfg',            r'^(version\s*=\s*)(\S+)()$'),
    ('commonpy/__init__.py', r'''^(__version__\s*=\s*['"])([^'"]+)(['"])'''),
    ('codemeta.json',        r'^(\s*"version"\s*:\s*")([^"]+)(")'),
    ('CITATION.cff',         r'''^(version:\s*["']?)([^"'\s]+)(["']?)'''),
]
DATE_FIELD = ('CITATION.cff', r'^(date-released:\s*)(\S+)()$')


def fail(message):
    print(f'bump_version: {message}', file=sys.stderr)
    sys.exit(1)


def read(file):
    with open(path.join(ROOT, file), encoding='utf-8') as f:
        return f.read()


def write(file, text):
    with open(path.join(ROOT, file), 'w', encoding='utf-8') as f:
        f.write(text)


def replace_field(file, pattern, value):
    text = read(file)
    new_text, count = re.subn(pattern, lambda m: m[1] + value + m[3],
                              text, count=1, flags=re.M)
    if count == 0:
        fail(f'no version field found in {file}')
    write(file, new_text)


def next_version(current, bump):
    if re.fullmatch(r'\d+\.\d+\.\d+', bump):
        return bump
    match = re.fullmatch(r'(\d+)\.(\d+)\.(\d+)', current)
    if not match:
        fail(f'current version {current} is not of the form X.Y.Z')
    major, minor, patch = (int(n) for n in match.groups())
    if bump == 'major':
        return f'{major + 1}.0.0'
    if bump == 'minor':
        return f'{major}.{minor + 1}.0'
    if bump == 'patch':
        return f'{major}.{minor}.{patch + 1}'
    fail(f'expected patch, minor, major, or X.Y.Z, got {bump}')


def main(args):
    if len(args) != 1:
        fail('usage: bump_version.py patch|minor|major|X.Y.Z')
    file, pattern = VERSION_FIELDS[0]
    current = re.search(pattern, read(file), re.M)
    if not current:
        fail(f'no version field found in {file}')
    version = next_version(current[2], args[0])
    for file, pattern in VERSION_FIELDS:
        replace_field(file, pattern, version)
    replace_field(*DATE_FIELD, date.today().isoformat())
    print(version)


if __name__ == '__main__':
    main(sys.argv[1:])
