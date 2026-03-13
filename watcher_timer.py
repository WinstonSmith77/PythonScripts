
"""
Script to watch a folder and log the time since the first event for each consecutive event.

Usage:
    python watcher_timer.py <folder_to_watch>

Arguments:
    folder_to_watch: Path to the folder to monitor for file system events.

Features:
    - Uses watchdog for file system events.
    - Starts a timer on the first event.
    - Logs time since first event for each subsequent event.
    - Uses argparse for argument parsing.
    - Follows PEP 8 and project coding guidelines.
"""


from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import sys
import argparse


class EventTimerHandler(FileSystemEventHandler):
    """
    Handles file system events and logs time since the first event.
    """
    def __init__(self) -> None:
        super().__init__()
        self.start_time: float | None = None

    def on_any_event(self, event) -> None:
        if self.start_time is None:
            self.start_time = time.time()
            print(f"First event: {event.event_type} - {event.src_path}")
        else:
            elapsed: float = time.time() - self.start_time
            print(f"Event: {event.event_type} - {event.src_path} | Time since first event: {elapsed:.2f} seconds")



def main(folder: Path) -> None:
    """
    Start watching the specified folder for file system events.

    Args:
        folder (Path): The folder to watch.
    """
    if not folder.is_dir():
        print(f"Error: {folder} is not a valid directory.")
        sys.exit(1)

    event_handler = EventTimerHandler()
    observer = Observer()
    observer.schedule(event_handler, str(folder), recursive=True)
    observer.start()
    print(f"Watching folder: {folder}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments using argparse.
    """
    parser = argparse.ArgumentParser(
        description="Watch a folder and log time since first event for each consecutive event."
    )
    parser.add_argument(
        "folder",
        type=str,
        help="Path to the folder to watch."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(Path(args.folder))
