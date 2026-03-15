#!/usr/bin/env python3
"""
Finds all folders recursively that only contain files ending with .xmp.

This script searches the given directory (or current directory) recursively
and prints the paths of folders that contain at least one visible file,
and where all visible files have the .xmp extension.
Hidden files (starting with .) are ignored.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import List


def find_and_move_xmp_folders(start_path: Path, destination: Path = None, dry_run: bool = False) -> None:
    """
    Recursively finds folders that only contain .xmp files (and no subdirectories)
    and optionally moves them to a destination folder.

    Args:
        start_path (Path): The directory to search in.
        destination (Path, optional): The directory to move matching folders to.
        dry_run (bool): If True, only print what would be done.
    """
    matching_folders: List[Path] = []
    
    destination_resolved = destination.resolve() if destination else None

    # Walk top-down so we can potentially skip directories if needed,
    # though for this logic, we just collect and then process.
    for root, dirs, files in os.walk(start_path):
        current_dir = Path(root).resolve()

        # Safety check: If we are scanning the destination folder itself or its children, skip them.
        if destination_resolved:
            # Check if current_dir is the destination or inside it
            if current_dir == destination_resolved or destination_resolved in current_dir.parents:
                # We are inside the destination folder. Don't touch things here.
                # Also, prevent descending further into this branch to save time.
                dirs[:] = [] 
                continue

        # Filter out hidden files (like .DS_Store, .gitignore)
        relevant_files = [f for f in files if not f.startswith('.')]
        
        # Filter out hidden directories to avoid traversing into .git etc
        visible_dirs = [d for d in dirs if not d.startswith('.')]

        # Conditions:
        # 1. Must contain at least one relevant file
        # 2. All relevant files must end with .xmp
        # 3. Must NOT contain any visible subdirectories (to ensure we move 'leaves' and avoid nesting issues)
        if relevant_files and not visible_dirs:
            if all(f.lower().endswith('.xmp') for f in relevant_files):
                matching_folders.append(current_dir)

    # Sort matching folders to process them in a deterministic order
    matching_folders.sort()

    if not matching_folders:
        print("No matching folders found.")
        return

    print(f"Found {len(matching_folders)} folders matching criteria.")

    for folder in matching_folders:
        if destination:
            # Determine new path
            # We move the folder *into* the destination.
            # If folder is /path/to/123, and destination is /dest
            # New path should be /dest/123.
            target_path = destination / folder.name
            
            print(f"Moving '{folder}' to '{target_path}'...")
            
            if not dry_run:
                try:
                    if target_path.exists():
                        print(f"  WARNING: Target '{target_path}' already exists. Skipping.")
                        continue
                    
                    # Ensure destination exists
                    destination.mkdir(parents=True, exist_ok=True)
                    
                    shutil.move(str(folder), str(target_path))
                except Exception as e:
                    print(f"  ERROR: Failed to move '{folder}': {e}")
        else:
            print(folder)


def main() -> None:
    """
    Main function to parse arguments and execute the search/move.
    """
    parser = argparse.ArgumentParser(
        description="Find all folders recursively that only contain .xmp files (and no subfolders), and optionally move them."
    )
    parser.add_argument(
        "--source", "-s", 
        nargs="?",
        default=".",
        help="The directory to search in (default: current directory)"
    )
    parser.add_argument(
        "--destination", "-d",
        type=str,
        help="The destination directory to move matching folders to."
    )

    args = parser.parse_args()
    directory = Path(args.source).resolve()
    
    if args.destination:
        destination = Path(args.destination).resolve()
    else:
        destination = None

    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        return

    if not directory.is_dir():
        print(f"Error: Path '{directory}' is not a directory.")
        return

    find_and_move_xmp_folders(directory, destination, args.dry_run)


if __name__ == "__main__":
    main()
