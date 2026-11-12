import sys
import shutil
from pathlib import Path
from importlib.util import find_spec


def run_system_doctor(project_path="."):
    root = Path(project_path).expanduser().resolve()

    print("\n" + "=" * 50)
    print("          AMR SYSTEM DOCTOR")
    print("=" * 50)

    checks = []

    # Python version
    python_ok = sys.version_info >= (3, 10)
    checks.append((
        "Python Version",
        python_ok,
        sys.version.split()[0]
    ))

    # Python environment
    checks.append((
        "Virtual Environment",
        sys.prefix != sys.base_prefix,
        sys.prefix
    ))

    # Project folder
    checks.append((
        "Project Directory",
        root.exists() and root.is_dir(),
        str(root)
    ))

    # Required files
    required_files = [
        "main.py",
        "analyzers/project_scanner.py",
        "analyzers/project_structure.py",
        "analyzers/system_doctor.py",
    ]

    for filename in required_files:
        exists = (root / filename).is_file()
        checks.append((
            filename,
            exists,
            "Found" if exists else "Missing"
        ))

    # Required folders
    required_folders = [
        "analyzers",
        "core",
        "commands",
        "reports",
        "backups",
        "tests",
    ]

    for folder in required_folders:
        exists = (root / folder).is_dir()
        checks.append((
            f"Folder: {folder}",
            exists,
            "Found" if exists else "Missing"
        ))

    # Git
    git_path = shutil.which("git")
    checks.append((
        "Git Installation",
        git_path is not None,
        git_path or "Not Installed"
    ))

    # Python package manager
    checks.append((
        "Pip",
        find_spec("pip") is not None,
        "Available" if find_spec("pip") else "Missing"
    ))

    passed = 0
    failed = 0

    print("\nSYSTEM CHECKS:\n")

    for name, status, details in checks:
        if status:
            passed += 1
            result = "OK"
        else:
            failed += 1
            result = "WARNING"

        print(f"[{result}] {name}: {details}")

    print("\n" + "=" * 50)
    print(f"Passed: {passed}")
    print(f"Warnings: {failed}")
    print(f"Total Checks: {len(checks)}")
    print("=" * 50)

    print("\nSystem Doctor Completed.")
    return failed == 0


if __name__ == "__main__":
    run_system_doctor()