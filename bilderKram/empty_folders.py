from pathlib import Path
from typing import Iterator

def list_subfolders_without_files(root_folder: str) -> Iterator[Path]:
    """
    Recursively yield all subfolders inside the given root_folder that do not contain any files.

    Args:
        root_folder (str): The path to the root folder.

    Yields:
        Path: Path object for each subfolder found that contains no files.
    """
    root_path = Path(root_folder)
    for path in root_path.rglob('*'):
        if path.is_dir() and not any(item.is_file() for item in path.rglob('*')):
            yield path

def filter_nested_folders(folders: list[Path]) -> list[Path]:
    """
    Remove folders that are subfolders of other folders in the list.

    Args:
        folders (list[Path]): List of folder paths.

    Returns:
        list[Path]: Filtered list without nested folders.
    """
    sorted_folders = sorted(folders)
    result = []
    
    for folder in sorted_folders:
        is_nested = False
        for other_folder in sorted_folders:
            if folder != other_folder:
                try:
                    folder.relative_to(other_folder)
                    is_nested = True
                    break
                except ValueError:
                    continue
        
        if not is_nested:
            result.append(folder)
    
    return result

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="List all subfolders that do not contain any files, excluding nested folders.")
    parser.add_argument("folder", help="Path to the root folder")
    args = parser.parse_args()

    all_folders = list(list_subfolders_without_files(args.folder))
    filtered_folders = filter_nested_folders(all_folders)
    
    for subfolder in filtered_folders:
        print(subfolder, list(subfolder.rglob('*')))