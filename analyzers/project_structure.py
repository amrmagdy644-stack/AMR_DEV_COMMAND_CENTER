from pathlib import Path

EXCLUDED_DIRS = {
    ".venv",
    "venv",
    ".git",
    "__pycache__",
    "node_modules",
    ".idea",
    "dist",
    "build",
}


def show_structure(project_path, max_depth=4):
    root = Path(project_path).expanduser().resolve()

    if not root.exists() or not root.is_dir():
        print("ERROR: Invalid project path.")
        return

    print("\n" + "=" * 50)
    print(f"PROJECT STRUCTURE: {root.name}")
    print("=" * 50)

    def display(folder, prefix="", depth=0):
        if depth >= max_depth:
            return

        try:
            entries = sorted(
                [
                    item for item in folder.iterdir()
                    if item.name not in EXCLUDED_DIRS
                ],
                key=lambda item: (item.is_file(), item.name.lower())
            )
        except PermissionError:
            print(prefix + "[Access Denied]")
            return

        for index, item in enumerate(entries):
            last = index == len(entries) - 1
            connector = "└── " if last else "├── "

            print(prefix + connector + item.name)

            if item.is_dir():
                new_prefix = prefix + ("    " if last else "│   ")
                display(item, new_prefix, depth + 1)

    print(root.name)
    display(root)

    print("\nStructure Analysis Completed.")
    print("=" * 50)


if __name__ == "__main__":
    path = input("Enter Project Path: ").strip()

    if path:
        show_structure(path)
    else:
        show_structure(".")