import argparse
from datetime import datetime
from pathlib import Path


def list_file_creation_dates(folder_path: Path) -> None:
    """
    List all files in the given folder along with their creation dates.

    Args:
        folder_path: The path to the folder to inspect.
    """
    if not folder_path.is_dir():
        print(f"Error: The path '{folder_path}' is not a valid directory.")
        return

    print(f"Listing unique creation dates for files in: {folder_path.resolve()}\n")

    unique_dates = set()

    try:
        # Iterate recursively over all items in the folder and subfolders
        for file_path in folder_path.rglob("*"):
            if file_path.is_file():
                try:
                    # st_ctime is the file creation time on Windows
                    stat_info = file_path.stat()
                    creation_time = datetime.fromtimestamp(stat_info.st_ctime)
                    unique_dates.add(creation_time.strftime("%Y-%m-%d"))
                except OSError as e:
                    print(f"Could not read stats for {file_path.name}: {e}")

        # Print the identified dates in chronological order
        for date in sorted(unique_dates):
            print(date)

    except PermissionError as e:
        print(f"Permission denied when accessing '{folder_path}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main() -> None:
    """Parse command-line arguments and run the primary logic."""
    parser = argparse.ArgumentParser(
        description="List the creation dates of all files in a specified folder."
    )
    parser.add_argument(
        "folder",
        type=str,
        nargs="?",
        default=".",
        help="Path to the folder (defaults to the current directory)."
    )

    args = parser.parse_args()
    folder_path = Path(args.folder)

    list_file_creation_dates(folder_path)


if __name__ == "__main__":
    main()
