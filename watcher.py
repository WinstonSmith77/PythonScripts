import time
import argparse
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class FolderWatcher(FileSystemEventHandler):
    def on_any_event(self, event):
        kind = "directory" if event.is_directory else "file"
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {kind} | {event.event_type} | {event.src_path}")

def main(path: Path):
    if not path.exists():
        raise FileNotFoundError(path)

    handler = FolderWatcher()
    observer = Observer()
    observer.schedule(handler, str(path), recursive=True)
    observer.start()
    print(f"Watching {path.resolve()} (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Watch a directory for file system events.")
    parser.add_argument("-f", "--folder", required=True, type=Path, help="Folder to monitor.")
    args = parser.parse_args()
    main(args.folder)
    


    