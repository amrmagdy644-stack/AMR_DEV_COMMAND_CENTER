from analyzers.project_scanner import scan_project
from analyzers.project_structure import show_structure
from analyzers.system_doctor import run_system_doctor
from analyzers.backup_manager import create_backup
from analyzers.git_manager import git_menu


def main():
    while True:
        print("\n" + "=" * 45)
        print("       AMR DEV COMMAND CENTER")
        print("=" * 45)

        print("1. Scan Project")
        print("2. Start Project")
        print("3. Analyze Errors")
        print("4. Project Structure")
        print("5. Backup Project")
        print("6. Git Manager")
        print("7. System Doctor")
        print("8. Exit")

        print("=" * 45)

        choice = input("Select Command: ").strip()

        if choice == "1":
            path = input(
                "Enter Project Path (Enter for current folder): "
            ).strip() or "."

            scan_project(path)

        elif choice == "2":
            print("Start Project module is under development.")

        elif choice == "3":
            print("Analyze Errors module is under development.")

        elif choice == "4":
            path = input(
                "Enter Project Path (Enter for current folder): "
            ).strip() or "."

            show_structure(path)

        elif choice == "5":
            path = input(
                "Enter Project Path (Enter for current folder): "
            ).strip() or "."

            create_backup(path)

        elif choice == "6":
            git_menu()

        elif choice == "7":
            run_system_doctor()

        elif choice == "8":
            print("\nGoodbye!")
            break

        else:
            print("Invalid command.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()