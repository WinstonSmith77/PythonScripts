"""List file stem names and sizes for all files in a folder recursively.

Usage:
    python list_stems_and_sizes.py /path/to/folder_a /path/to/folder_b
"""
import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path

from PIL import Image
from PIL.ExifTags import TAGS



def collect_stems_and_sizes(folder: Path) -> dict[tuple[str, int, datetime], Path]:
    """Collect file stem and file size in bytes for all files in a folder tree."""
    results:dict[tuple[str, int, datetime], Path] = {}

    for path in folder.rglob("*"):
        if not path.is_file():
            continue

        try:
            size = path.stat().st_size
            creating_date = read_jpg_creation_date(path)
            results[(path.parts[-1], size, creating_date)] = path
        except OSError:
            # Skip files that cannot be accessed.
            continue

    return results

def MakeStats(items: dict[tuple[str, int, datetime], Path]) -> Counter:
    return Counter(HandleSuffix(item.suffix) for item in items.values())

def HandleSuffix(suffix: str) -> str:
    result = suffix.lower()
    if result == ".jpeg":
        return "jpg"
    return result


_EXIF_DATE_FORMAT = "%Y:%m:%d %H:%M:%S"
_EXIF_DATE_TAGS = ("DateTimeOriginal", "DateTime")


def read_jpg_creation_date(path: Path) -> datetime | None:
    """Return the creation date from EXIF data of a JPEG file.

    Tries DateTimeOriginal first, then falls back to DateTime.
    Returns None if no readable date tag is found or the file is not a valid image.
    """
    try:
        with Image.open(path) as img:
            exif_data = img._getexif()  # type: ignore[attr-defined]
    except Exception:
        return None

    if not exif_data:
        return None

    tag_map = {TAGS.get(tag_id, tag_id): value for tag_id, value in exif_data.items()}

    for tag_name in _EXIF_DATE_TAGS:
        raw = tag_map.get(tag_name)
        if raw:
            try:
                return datetime.strptime(raw, _EXIF_DATE_FORMAT)
            except ValueError:
                continue

    return None


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
    print("stem\tsize_bytes\tcreation_date")
    for (stem, size, creation_date), path in items.items():
        print(f" {stem} {size} {creation_date} -> {path}")
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
