"""List file stem names and sizes for all files in a folder recursively.

Usage:
    python list_stems_and_sizes.py /path/to/folder_a /path/to/folder_b
"""
import argparse
from pathlib import Path
from collections import Counter



def collect_stems_and_sizes(folder: Path) -> dict[tuple[str, int], Path]:
    """Collect file stem and file size in bytes for all files in a folder tree."""
    results: dict[tuple[str, int], Path]= {}

    for path in folder.rglob("*"):
        if not path.is_file():
            continue

        try:
            size = path.stat().st_size
            results[(path.parts[-1], size)] = path
        except OSError:
            # Skip files that cannot be accessed.
            continue

    return results

def MakeStats(items: dict[tuple[str, int], Path]) -> Counter:
    return Counter(HandleSuffix(item.suffix) for item in items.values())

def HandleSuffix(suffix: str) -> str:
    result = suffix.lower()
    if result in (".jpg", ".jpeg"):
        return "jpg"
    return result

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Recursively list file stem names and file sizes for two folders."
    )
    parser.add_argument(
        "a",
        type=Path,
        help="First folder to scan recursively.",
    )
    parser.add_argument(
        "b",
        type=Path,
        help="Second folder to scan recursively.",
    )
    return parser.parse_args()


def print_folder_items(folder_name: str, folder: Path) -> None:
    """Print stem and size rows for all files in a folder."""
    if not folder.exists():
        raise FileNotFoundError(f"Folder '{folder_name}' does not exist: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Folder '{folder_name}' is not a directory: {folder}")

    items = collect_stems_and_sizes(folder)
    stats = MakeStats(items)

    print(f"{folder_name}: {folder}")
    print("stem\tsize_bytes")
    for (stem, size), path in items.items():
        print(f" {stem} {size} -> {path}")
    print(stats)    
    print()


def main() -> None:
    """Run the CLI."""
    args = parse_args()
    folder_a: Path = args.a
    folder_b: Path = args.b

    print_folder_items("a", folder_a)
    print_folder_items("b", folder_b)


if __name__ == "__main__":
    main()
