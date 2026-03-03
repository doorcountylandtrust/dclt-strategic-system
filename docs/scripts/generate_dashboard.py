#!/usr/bin/env python3
"""
DCLT Strategic Dashboard Generator
===================================
Scans your markdown workspace, reads YAML frontmatter, and generates
a DASHBOARD.md at the root of your project.

Usage:
    python scripts/generate_dashboard.py [path_to_workspace]

If no path is given, uses the current directory.
"""

import os
import sys
import re
from datetime import datetime, date
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Directories to skip entirely
SKIP_DIRS = {
    'legacy_site_content', 'node_modules', '.git', '__pycache__',
    'attachment', 'wordpress-posts', 'current-site-screenshots',
    'export', 'overrides'
}

# Files to skip
SKIP_FILES = {'index.md', 'README.md', 'DASHBOARD.md', 'SCHEMA.md'}

# ---------------------------------------------------------------------------
# Frontmatter Parser (no external dependencies)
# ---------------------------------------------------------------------------

def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file.
    
    Returns a dict of frontmatter fields, or None if no frontmatter found.
    Uses a simple parser to avoid requiring PyYAML as a dependency.
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read(4096)  # Only read first 4KB for frontmatter
    except Exception:
        return None

    # Check for frontmatter delimiters
    if not content.startswith('---'):
        return None

    end = content.find('---', 3)
    if end == -1:
        return None

    raw = content[3:end].strip()
    if not raw:
        return None

    fm = {}
    current_key = None
    current_list = None

    for line in raw.split('\n'):
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith('#'):
            continue

        # List item under a key
        if stripped.startswith('- ') and current_key and current_list is not None:
            current_list.append(stripped[2:].strip().strip('"').strip("'"))
            continue

        # Key-value pair
        if ':' in stripped:
            key, _, value = stripped.partition(':')
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if value:
                fm[key] = value
                current_key = key
                current_list = None
            else:
                # Start of a list or empty value
                current_key = key
                current_list = []
                fm[key] = current_list

    return fm if fm else None


def get_title_from_content(filepath):
    """Fall back to reading the first H1/H2 from markdown content."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line.lstrip('# ').strip()
                if line.startswith('## '):
                    return line.lstrip('# ').strip()
        return None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def scan_workspace(root):
    """Walk the workspace and collect file metadata."""
    files = []
    root = Path(root).resolve()

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune skipped directories
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        rel_dir = Path(dirpath).relative_to(root)

        for fname in sorted(filenames):
            if not fname.endswith('.md'):
                continue
            if fname in SKIP_FILES:
                continue

            filepath = Path(dirpath) / fname
            rel_path = rel_dir / fname

            fm = parse_frontmatter(filepath)

            # Build record
            record = {
                'path': str(rel_path),
                'filename': fname,
                'dir': str(rel_dir),
                'layer': _get_layer(str(rel_dir)),
            }

            if fm:
                record['has_frontmatter'] = True
                record['title'] = fm.get('title', get_title_from_content(filepath) or fname.replace('.md', '').replace('-', ' ').replace('_', ' '))
                record['status'] = fm.get('status', 'unknown')
                record['priority'] = fm.get('priority', '')
                record['type'] = fm.get('type', '')
                record['project'] = fm.get('project', '')
                record['owner'] = fm.get('owner', '')
                record['due'] = fm.get('due', fm.get('target_launch', ''))
                record['tags'] = fm.get('tags', [])
                record['updated'] = fm.get('updated', '')
                record['created'] = fm.get('created', '')
            else:
                record['has_frontmatter'] = False
                record['title'] = get_title_from_content(filepath) or fname.replace('.md', '').replace('-', ' ').replace('_', ' ')
                record['status'] = 'untagged'
                record['priority'] = ''
                record['type'] = ''
                record['project'] = ''
                record['owner'] = ''
                record['due'] = ''
                record['tags'] = []
                record['updated'] = ''
                record['created'] = ''

            files.append(record)

    return files


def _get_layer(dir_path):
    """Determine which layer a file belongs to."""
    if dir_path.startswith('01_STRATEGY'):
        return 'strategy'
    elif dir_path.startswith('02_EXECUTION'):
        return 'execution'
    elif dir_path.startswith('03_REFERENCE'):
        return 'reference'
    elif dir_path.startswith('04_DAILY'):
        return 'daily'
    else:
        return 'root'


# ---------------------------------------------------------------------------
# Dashboard Generator
# ---------------------------------------------------------------------------

def generate_dashboard(files, root):
    """Generate DASHBOARD.md content."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    today = date.today()

    # Categorize
    active = [f for f in files if f['status'] == 'active']
    planning = [f for f in files if f['status'] == 'planning']
    on_hold = [f for f in files if f['status'] == 'on-hold']
    untagged = [f for f in files if f['status'] == 'untagged']

    # Sort active by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2, '': 3}
    active.sort(key=lambda f: (priority_order.get(f['priority'], 3), f['title']))
    planning.sort(key=lambda f: f['title'])
    on_hold.sort(key=lambda f: f['title'])

    # Count by layer
    layer_counts = defaultdict(int)
    for f in files:
        layer_counts[f['layer']] += 1

    # Frontmatter coverage
    with_fm = sum(1 for f in files if f['has_frontmatter'])
    total = len(files)
    coverage_pct = (with_fm / total * 100) if total > 0 else 0

    # Files with due dates
    upcoming = []
    overdue = []
    for f in active + planning:
        if f['due']:
            try:
                due_str = str(f['due'])
                if len(due_str) == 7:  # YYYY-MM
                    due_date = date(int(due_str[:4]), int(due_str[5:7]), 28)
                elif len(due_str) == 10:  # YYYY-MM-DD
                    due_date = date.fromisoformat(due_str)
                else:
                    continue
                
                if due_date < today:
                    overdue.append((f, due_date))
                else:
                    upcoming.append((f, due_date))
            except (ValueError, TypeError):
                continue

    upcoming.sort(key=lambda x: x[1])
    overdue.sort(key=lambda x: x[1])

    # Build dashboard
    lines = []
    lines.append('# DCLT Strategic Dashboard')
    lines.append(f'*Generated {now}*')
    lines.append('')

    # Quick stats
    lines.append('---')
    lines.append('')
    lines.append(f'**{len(active)}** active · **{len(planning)}** planning · **{len(on_hold)}** on hold · **{len(overdue)}** overdue · **{coverage_pct:.0f}%** frontmatter coverage')
    lines.append('')

    # Overdue
    if overdue:
        lines.append('---')
        lines.append('')
        lines.append('## ⚠️ Overdue')
        lines.append('')
        lines.append('| Project | Due | Priority | Path |')
        lines.append('|---------|-----|----------|------|')
        for f, due_date in overdue:
            p = f['priority'].upper() if f['priority'] else '—'
            lines.append(f"| {f['title']} | {due_date} | {p} | `{f['path']}` |")
        lines.append('')

    # Upcoming deadlines
    if upcoming:
        lines.append('---')
        lines.append('')
        lines.append('## 📅 Upcoming Deadlines')
        lines.append('')
        lines.append('| Project | Due | Priority | Path |')
        lines.append('|---------|-----|----------|------|')
        for f, due_date in upcoming[:10]:
            p = f['priority'].upper() if f['priority'] else '—'
            lines.append(f"| {f['title']} | {due_date} | {p} | `{f['path']}` |")
        lines.append('')

    # Active projects
    if active:
        lines.append('---')
        lines.append('')
        lines.append('## 🔥 Active Projects')
        lines.append('')
        lines.append('| Project | Priority | Owner | Due | Layer | Path |')
        lines.append('|---------|----------|-------|-----|-------|------|')
        for f in active:
            p = f['priority'].upper() if f['priority'] else '—'
            owner = f['owner'] or '—'
            due = f['due'] or '—'
            layer = f['layer'].title()
            lines.append(f"| {f['title']} | {p} | {owner} | {due} | {layer} | `{f['path']}` |")
        lines.append('')

    # Planning
    if planning:
        lines.append('---')
        lines.append('')
        lines.append('## 📋 In Planning')
        lines.append('')
        lines.append('| Project | Priority | Path |')
        lines.append('|---------|----------|------|')
        for f in planning:
            p = f['priority'] or '—'
            lines.append(f"| {f['title']} | {p} | `{f['path']}` |")
        lines.append('')

    # On hold
    if on_hold:
        lines.append('---')
        lines.append('')
        lines.append('## ⏸️ On Hold')
        lines.append('')
        lines.append('| Project | Reason | Path |')
        lines.append('|---------|--------|------|')
        for f in on_hold:
            lines.append(f"| {f['title']} | — | `{f['path']}` |")
        lines.append('')

    # Workspace health
    lines.append('---')
    lines.append('')
    lines.append('## 🏗️ Workspace Health')
    lines.append('')
    lines.append(f'| Layer | Files |')
    lines.append(f'|-------|-------|')
    for layer_name, display in [('strategy', 'Strategy'), ('execution', 'Execution'), ('reference', 'Reference'), ('daily', 'Daily Focus'), ('root', 'Root')]:
        if layer_counts[layer_name]:
            lines.append(f'| {display} | {layer_counts[layer_name]} |')
    lines.append(f'| **Total** | **{total}** |')
    lines.append('')
    lines.append(f'**Frontmatter coverage:** {with_fm}/{total} files ({coverage_pct:.0f}%)')
    lines.append('')

    # Untagged files (first 20)
    if untagged:
        lines.append('---')
        lines.append('')
        lines.append(f'## 📭 Untagged Files ({len(untagged)} total)')
        lines.append('')
        lines.append('These files have no YAML frontmatter. Add frontmatter to include them in tracking.')
        lines.append('')
        shown = untagged[:20]
        for f in shown:
            lines.append(f"- `{f['path']}` — *{f['title']}*")
        if len(untagged) > 20:
            lines.append(f'- ... and {len(untagged) - 20} more')
        lines.append('')

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    root = Path(root).resolve()

    if not root.is_dir():
        print(f"Error: {root} is not a directory")
        sys.exit(1)

    print(f"Scanning {root}...")
    files = scan_workspace(root)
    print(f"Found {len(files)} markdown files")

    dashboard = generate_dashboard(files, root)

    out_path = root / 'DASHBOARD.md'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(dashboard)

    print(f"Dashboard written to {out_path}")

    # Quick summary
    statuses = defaultdict(int)
    for f in files:
        statuses[f['status']] += 1
    for status, count in sorted(statuses.items()):
        print(f"  {status}: {count}")


if __name__ == '__main__':
    main()