from pathlib import Path
from collections import Counter


EXCLUDED_DIRS = {
    ".venv",
    "venv",
    ".git",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build",
}


def detect_project_type(root):
    files = {p.name.lower() for p in root.iterdir() if p.is_file()}
    folders = {p.name.lower() for p in root.iterdir() if p.is_dir()}

    types = []

    if "manage.py" in files:
        types.append("Django")

    if "odoo-bin" in files or "__manifest__.py" in files:
        types.append("Odoo")

    if any(name.endswith(".sln") for name in files):
        types.append(".NET / C#")

    if "package.json" in files:
        types.append("Node.js / JavaScript")

    if "requirements.txt" in files or "pyproject.toml" in files:
        types.append("Python")

    if "index.html" in files:
        types.append("HTML / Web")

    if not types:
        types.append("Unknown Project")

    return types


def scan_project(project_path):
    root = Path(project_path).expanduser().resolve()

    if not root.exists() or not root.is_dir():
        print("\nERROR: Project folder does not exist.")
        return

    total_files = 0
    total_folders = 0
    extensions = Counter()

    print("\nStarting Project Scan...")
    print(f"Project: {root}")

    for current_path in root.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in current_path.parts):
            continue

        if current_path.is_dir():
            total_folders += 1

        elif current_path.is_file():
            total_files += 1
            extension = current_path.suffix.lower() or "[No Extension]"
            extensions[extension] += 1

    project_types = detect_project_type(root)

    print("\n" + "=" * 45)
    print("          PROJECT SCAN REPORT")
    print("=" * 45)

    print(f"Project Name: {root.name}")
    print(f"Project Type: {', '.join(project_types)}")
    print(f"Total Files: {total_files}")
    print(f"Total Folders: {total_folders}")

    print("\nFile Extensions:")

    for extension, count in extensions.most_common():
        print(f"{extension}: {count}")

    print("\nScan Completed Successfully.")
    print("=" * 45)


if __name__ == "__main__":
    path = input("Enter Project Path (or press Enter for current folder): ").strip()

    if not path:
        path = "."

    scan_project(path)