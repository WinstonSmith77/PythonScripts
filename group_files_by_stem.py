import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict, List


def group_files_by_stem(directory: Path) -> Dict[str, List[Path]]:
    """
    Scans a directory and groups files by their stem (filename without extension).

    Args:
        directory (Path): The directory to scan.

    Returns:
        Dict[str, List[Path]]: A dictionary where keys are file stems and values
                               are lists of Paths sharing that stem.
    """
    grouped_files: Dict[str, List[Path]] = defaultdict(list)

    if not directory.exists():
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")

    if not directory.is_dir():
        raise NotADirectoryError(f"The path '{directory}' is not a directory.")

    for item in directory.rglob("*"):
        if item.is_file():
            # item.stem returns the filename without the last suffix
            # If you have files like data.tar.gz, stem is data.tar
            # If strict "name before first dot" is needed, split on '.'
            grouped_files[item.stem].append(item)

    return grouped_files


def main() -> None:
    """
    Main function to parse arguments and print grouped files.
    """
    parser = argparse.ArgumentParser(
        description="List all files in a folder and group them by file stem."
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="The path to the directory to scan.",
        nargs="?",
        default=Path("."),
    )

    args = parser.parse_args()
    directory: Path = args.directory

    try:
        grouped = group_files_by_stem(directory)

        # Filter to keep only stems with more than one file
        grouped = {k: v for k, v in grouped.items() if len(v) > 1}

        #print(grouped)

        # Filter out groups that only contain .xmp and .rw2 files (case-insensitive)
        ignored_extensions = {".xmp", ".rw2"}
        grouped = {
            stem: files
            for stem, files in grouped.items()
            # Keep if NOT (all files have ignored extensions)
            if not all(f.suffix.lower() in ignored_extensions for f in files)
        }

        if not grouped:
            print(f"No groups with multiple files found in '{directory}'.")
            return

        print(f"Files in '{directory}' grouped by stem (duplicates only):\n")
        
        # Sort by stem for consistent output
        for stem in sorted(grouped.keys()):
            files = grouped[stem]
            print(f"Stem: {stem}")
            for file_path in sorted(files):
                print(f"  - {file_path.name} ({file_path.parent})")
            print() # Empty line between groups

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
