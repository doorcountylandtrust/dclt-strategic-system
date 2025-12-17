import re
from pathlib import Path

# --- Configuration ---
DOCS_DIR = Path("docs")  # Adjust this if your root is different
LOG_FILE = Path("fix_log.txt")

# --- Regex patterns ---
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

def resolve_link(md_file: Path, target: str) -> Path:
    """Resolve a link target relative to the Markdown file."""
    target_path = Path(target)
    if not target_path.is_absolute():
        return (md_file.parent / target_path).resolve()
    return target_path

def append_log(message: str):
    """Append a message to the log file."""
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(message + "\n")

def fix_markdown_file(file_path: Path, repo_root: Path):
    changed = False
    output_lines = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        new_line = line

        for pattern in [LINK_PATTERN, IMAGE_PATTERN]:
            matches = list(pattern.finditer(new_line))
            for match in matches:
                full_match = match.group(0)
                label, target = match.groups()
                resolved = resolve_link(file_path, target)

                if not resolved.exists():
                    # Try to find a close file match in the same directory
                    possible_matches = list(file_path.parent.glob("*.md"))
                    guessed = None
                    for pm in possible_matches:
                        if label.lower().strip().replace(" ", "_") in pm.name.lower():
                            guessed = pm.name
                            break

                    if guessed:
                        new_target = guessed
                        fixed = f"[{label}]({new_target})"
                        new_line = new_line.replace(full_match, fixed)
                        append_log(f"[FIXED] {file_path} → {label} ➝ {guessed}")
                        changed = True
                    else:
                        # Comment out broken link
                        commented = f"<!-- BROKEN LINK: {full_match} -->"
                        new_line = new_line.replace(full_match, commented)
                        append_log(f"[REMOVED] {file_path} → {target}")
                        changed = True

        output_lines.append(new_line)

    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(output_lines)

def main():
    if LOG_FILE.exists():
        LOG_FILE.unlink()

    print("🔍 Scanning and fixing broken Markdown links in /docs...\n")

    for path in DOCS_DIR.rglob("*.md"):
        fix_markdown_file(path, DOCS_DIR)

    print(f"\n✅ Done! Changes logged in: {LOG_FILE.absolute()}")

if __name__ == "__main__":
    main()