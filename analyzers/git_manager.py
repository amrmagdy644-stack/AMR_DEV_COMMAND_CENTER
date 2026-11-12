import subprocess
import shutil
from pathlib import Path


# ==========================================
# GIT COMMAND RUNNER
# ==========================================

def get_git_repo(project_path):
    root = Path(project_path).expanduser().resolve()
    git = shutil.which("git")

    if not root.is_dir():
        print("ERROR: Invalid project directory.")
        return None, None

    if not git:
        print("ERROR: Git is not installed.")
        return None, None

    if not (root / ".git").exists():
        print("ERROR: This folder is not a Git repository.")
        return None, None

    return root, git


def execute_git(root, git, args, timeout=30):
    return subprocess.run(
        [git] + args,
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout
    )


def run_git(project_path, command):
    root, git = get_git_repo(project_path)

    if not git:
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
        result = execute_git(root, git, commands[command])

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
    root, git = get_git_repo(project_path)

    if not git:
        return

    try:
        check = execute_git(
            root, git, ["branch", "--list", "main"]
        )

        if check.returncode != 0:
            print(check.stderr)
            return

        if not check.stdout.strip():
            print("Main branch does not exist.")
            return

        result = execute_git(
            root, git, ["switch", "main"]
        )

        print(result.stdout or result.stderr or "Connected to main.")

    except Exception as error:
        print("ERROR:", error)


# ==========================================
# GIT ADD
# ==========================================

def git_add(project_path):
    root, git = get_git_repo(project_path)

    if not git:
        return

    try:
        result = execute_git(root, git, ["add", "-A"])

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
    root, git = get_git_repo(project_path)

    if not git:
        return

    try:
        check = execute_git(
            root, git, ["diff", "--cached", "--quiet"]
        )

        if check.returncode == 0:
            print("Nothing to commit. Working tree clean.")
            return

        if check.returncode != 1:
            print("Could not check staged changes.")
            return

        message = input("Enter commit message: ").strip()

        if not message:
            print("Commit message cannot be empty.")
            return

        result = execute_git(
            root, git, ["commit", "-m", message]
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
    root, git = get_git_repo(project_path)

    if not git:
        return

    confirm = input(
        "Are you sure you want to push changes? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("Push cancelled.")
        return

    try:
        result = execute_git(
            root, git, ["push"], timeout=60
        )

        print(result.stdout or result.stderr)

        if result.returncode != 0:
            print("Push failed. Check remote and authentication.")
        else:
            print("Push completed successfully.")

    except subprocess.TimeoutExpired:
        print("ERROR: Git push timed out.")

    except Exception as error:
        print("ERROR:", error)


# ==========================================
# SYNC ALL
# ==========================================

def sync_all(project_path):
    root, git = get_git_repo(project_path)

    if not git:
        return

    print("\n" + "=" * 45)
    print("          GIT SYNC ALL")
    print("=" * 45)

    try:
        # STEP 1: Check remote
        remote = execute_git(
            root, git, ["remote", "get-url", "origin"]
        )

        if remote.returncode != 0:
            print("ERROR: No origin remote configured.")
            return

        print("\n[1/5] Remote connection found.")

        # STEP 2: Add changes
        add = execute_git(root, git, ["add", "-A"])

        if add.returncode != 0:
            print("Git Add failed:", add.stderr)
            return

        print("[2/5] Files added successfully.")

        # STEP 3: Check staged changes
        check = execute_git(
            root, git, ["diff", "--cached", "--quiet"]
        )

        if check.returncode == 1:
            message = input(
                "\nEnter commit message: "
            ).strip()

            if not message:
                print("Commit cancelled: Empty message.")
                return

            commit = execute_git(
                root, git, ["commit", "-m", message]
            )

            print(commit.stdout or commit.stderr)

            if commit.returncode != 0:
                print("Commit failed. Sync stopped.")
                return

            print("[3/5] Commit completed.")

        elif check.returncode == 0:
            print("[3/5] No new changes to commit.")

        else:
            print("Could not check staged changes.")
            return

        # STEP 4: Confirm push
        confirm = input(
            "\nPush changes to GitHub? (y/n): "
        ).strip().lower()

        if confirm != "y":
            print("Push cancelled. Local changes are saved.")
            return

        # STEP 5: Push
        push = execute_git(
            root, git, ["push"], timeout=60
        )

        print("\n" + "=" * 45)
        print("GITHUB PUSH RESULT")
        print("=" * 45)

        print(push.stdout or push.stderr)

        if push.returncode == 0:
            print("\nSYNC COMPLETED SUCCESSFULLY!")
        else:
            print("\nPUSH FAILED. Check GitHub connection.")

    except subprocess.TimeoutExpired:
        print("ERROR: Git operation timed out.")

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
        print("9. Sync All")
        print("0. Back")

        choice = input("\nSelect Option: ").strip()

        if choice == "0":
            return

        if choice not in [
            "1", "2", "3", "4", "5",
            "6", "7", "8", "9"
        ]:
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

        elif choice == "9":
            sync_all(path)

        input("\nPress Enter to continue...")


# ==========================================
# RUN DIRECTLY
# ==========================================

if __name__ == "__main__":
    git_menu()