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
            # Get the filename without any suffixes (e.g., image.tar.gz -> image)
            # strictly taking the name before the first dot
            stem = item.name.split('.')[0]
            grouped_files[stem].append(item)

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

        # Filter to keep only stems that contain BOTH .jpg and .rw2 files (case-insensitive)
        required_extensions = {".jpg", ".rw2"}
        
        filtered_grouped = {}
        for stem, files in grouped.items():
            # Get unique extensions in this group
            extensions = {f.suffix.lower() for f in files}
            
            # Check if BOTH .jpg and .rw2 are present
            if required_extensions.issubset(extensions):
                filtered_grouped[stem] = files
                
        grouped = filtered_grouped

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
