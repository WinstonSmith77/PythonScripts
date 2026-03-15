
"""

M4 MIN  4832     30:24      JPG Full 
nuc     4748    1:18:49     JPG Full

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
import sys
import time
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



class EventTimerHandler(FileSystemEventHandler):
    """
    Handles file system events and logs time since the first event.
    """
    def __init__(self) -> None:
        super().__init__()
        self.start_time: float | None = None

    def on_any_event(self, event) -> None:
        """
        Called on any file system event. Starts timer on first event and logs time since first event for subsequent events.
        Args:
            event: The file system event object.
        """
        if self.start_time is None:
            self.start_time = time.time()
            print(f"First event: {event.event_type} - {event.src_path}")
        else:
            elapsed: float = time.time() - self.start_time
            hours: int = int(elapsed // 3600)
            minutes: int = int((elapsed % 3600) // 60)
            seconds: int = int(elapsed % 60)
            time_str: str = f"{hours:02}:{minutes:02}:{seconds:02}"
            print(f"Event: {event.event_type} - {event.src_path} | Time since first event: {time_str}")



def main(folder: Path) -> None:
    """
    Start watching the specified folder for file system events.
    Args:
        folder (Path): The folder to watch.
    """
    if not folder.is_dir():
        print(f"Error: {folder} is not a valid directory.")
        sys.exit(1)

    event_handler: EventTimerHandler = EventTimerHandler()
    observer: Observer = Observer()
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
    Returns:
        argparse.Namespace: Parsed arguments.
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
    args: argparse.Namespace = parse_args()
    main(Path(args.folder))
