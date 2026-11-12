from pathlib import Path
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED


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


def create_backup(project_path="."):
    root = Path(project_path).expanduser().resolve()

    if not root.exists() or not root.is_dir():
        print("ERROR: Invalid project directory.")
        return None

    # Backup destination
    tool_root = Path(__file__).resolve().parent.parent
    backup_folder = tool_root / "backups"
    backup_folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{root.name}_{timestamp}.zip"
    backup_path = backup_folder / backup_name

    total_files = 0
    total_size = 0

    print("\nStarting Backup...")
    print(f"Source: {root}")

    try:
        with ZipFile(
            backup_path,
            "w",
            compression=ZIP_DEFLATED
        ) as archive:

            for current_file in root.rglob("*"):

                if not current_file.is_file():
                    continue

                if any(
                    part in EXCLUDED_DIRS
                    for part in current_file.relative_to(root).parts
                ):
                    continue

                # Avoid including the backup itself
                if current_file.is_relative_to(backup_folder):
                    continue

                relative_path = current_file.relative_to(root)

                archive.write(current_file, relative_path)

                total_files += 1
                total_size += current_file.stat().st_size

        print("\n" + "=" * 45)
        print("          BACKUP REPORT")
        print("=" * 45)
        print(f"Project: {root.name}")
        print(f"Files Backed Up: {total_files}")
        print(f"Original Size: {total_size / 1024:.2f} KB")
        print(f"Backup File: {backup_path}")
        print("\nBackup Completed Successfully!")
        print("=" * 45)

        return backup_path

    except Exception as error:
        if backup_path.exists():
            backup_path.unlink()

        print(f"\nBackup Failed: {error}")
        return None


if __name__ == "__main__":
    path = input("Enter Project Path: ").strip()

    if not path:
        path = "."

    create_backup(path)