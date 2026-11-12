import subprocess
import shutil
from pathlib import Path


# ==========================================
# GIT COMMAND RUNNER
# ==========================================

def run_git(project_path, command):
    root = Path(project_path).expanduser().resolve()
    git = shutil.which("git")

    if not root.is_dir():
        print("ERROR: Invalid project directory.")
        return

    if not git:
        print("ERROR: Git is not installed.")
        return

    if not (root / ".git").exists():
        print("ERROR: This folder is not a Git repository.")
        return

    commands = {
        "status": ["status", "--short", "--branch"],
        "log": ["log", "-5", "--oneline"],
        "branches": ["branch", "-a"],
        "remote": ["remote", "-v"],
    }

    if command not in commands:
        print("ERROR: Unsupported Git command.")
        return

    try:
        result = subprocess.run(
            [git] + commands[command],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30
        )

        print("\n" + "=" * 45)
        print("GIT MANAGER:", command.upper())
        print("=" * 45)
        print(result.stdout or result.stderr or "No output.")

        if result.returncode != 0:
            print("Git Error:", result.returncode)

    except subprocess.TimeoutExpired:
        print("ERROR: Git command timed out.")

    except Exception as error:
        print("ERROR:", error)


# ==========================================
# CONNECT TO MAIN
# ==========================================

def connect_main(project_path):
    root = Path(project_path).expanduser().resolve()
    git = shutil.which("git")

    if not root.is_dir() or not git:
        print("Invalid directory or Git is not installed.")
        return

    if not (root / ".git").exists():
        print("This folder is not a Git repository.")
        return

    try:
        check = subprocess.run(
            [git, "branch", "--list", "main"],
            cwd=root,
            capture_output=True,
            text=True
        )

        if check.returncode != 0:
            print(check.stderr)
            return

        if not check.stdout.strip():
            create = subprocess.run(
                [git, "branch", "main"],
                cwd=root,
                capture_output=True,
                text=True
            )

            if create.returncode != 0:
                print(create.stderr)
                return

        result = subprocess.run(
            [git, "switch", "main"],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        print(result.stdout or result.stderr or "Connected to main.")

    except Exception as error:
        print("ERROR:", error)


# ==========================================
# GIT ADD
# ==========================================

def git_add(project_path):
    root = Path(project_path).expanduser().resolve()
    git = shutil.which("git")

    if not root.is_dir() or not git or not (root / ".git").exists():
        print("ERROR: Invalid Git repository.")
        return

    try:
        result = subprocess.run(
            [git, "add", "-A"],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30
        )

        if result.returncode == 0:
            print("All changes added successfully.")
        else:
            print("Git Error:", result.stderr)

    except Exception as error:
        print("ERROR:", error)


# ==========================================
# GIT COMMIT
# ==========================================

def git_commit(project_path):
    root = Path(project_path).expanduser().resolve()
    git = shutil.which("git")

    if not root.is_dir() or not git or not (root / ".git").exists():
        print("ERROR: Invalid Git repository.")
        return

    message = input("Enter commit message: ").strip()

    if not message:
        print("Commit message cannot be empty.")
        return

    try:
        result = subprocess.run(
            [git, "commit", "-m", message],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30
        )

        print(result.stdout or result.stderr)

        if result.returncode != 0:
            print("Commit failed.")

    except Exception as error:
        print("ERROR:", error)


# ==========================================
# GIT PUSH
# ==========================================

def git_push(project_path):
    root = Path(project_path).expanduser().resolve()
    git = shutil.which("git")

    if not root.is_dir() or not git or not (root / ".git").exists():
        print("ERROR: Invalid Git repository.")
        return

    confirm = input(
        "Are you sure you want to push changes? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("Push cancelled.")
        return

    try:
        result = subprocess.run(
            [git, "push"],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60
        )

        print(result.stdout or result.stderr)

        if result.returncode != 0:
            print("Push failed. Check your remote and authentication.")

    except subprocess.TimeoutExpired:
        print("ERROR: Git push timed out.")

    except Exception as error:
        print("ERROR:", error)


# ==========================================
# GIT MANAGER MENU
# ==========================================

def git_menu():

    while True:

        print("\n" + "=" * 45)
        print("          AMR GIT MANAGER")
        print("=" * 45)

        print("1. Git Status")
        print("2. Recent Commits")
        print("3. Branches")
        print("4. Remote Repositories")
        print("5. Connect to Main")
        print("6. Git Add")
        print("7. Git Commit")
        print("8. Git Push")
        print("0. Back")

        choice = input("\nSelect Option: ").strip()

        if choice == "0":
            return

        if choice not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            print("Invalid option.")
            input("\nPress Enter to continue...")
            continue

        path = input("Enter Project Path: ").strip() or "."

        if choice == "1":
            run_git(path, "status")

        elif choice == "2":
            run_git(path, "log")

        elif choice == "3":
            run_git(path, "branches")

        elif choice == "4":
            run_git(path, "remote")

        elif choice == "5":
            connect_main(path)

        elif choice == "6":
            git_add(path)

        elif choice == "7":
            git_commit(path)

        elif choice == "8":
            git_push(path)

        input("\nPress Enter to continue...")


# ==========================================
# RUN DIRECTLY
# ==========================================

if __name__ == "__main__":
    git_menu()