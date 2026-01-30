import time
import argparse
import threading
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FolderWatcher(FileSystemEventHandler):
    def __init__(self, debounce_seconds: float = 1, event=None):
        super().__init__()
        self._debounce_seconds = debounce_seconds
        self._event = event
        self._timer: threading.Timer | None = None
        self._pending_event: tuple[str, str, str] | None = None
        self._lock = threading.Lock()

    def on_any_event(self, event):
        kind = "directory" if event.is_directory else "file"
        event_info = (kind, event.event_type, event.src_path)

        with self._lock:
            self._pending_event = event_info
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(
                self._debounce_seconds, self._emit_pending)
            self._timer.daemon = True
            self._timer.start()

    def stop(self):
        with self._lock:
            if self._timer:
                self._timer.cancel()
                self._timer = None
            self._pending_event = None

    def _emit_pending(self):
        with self._lock:
            event_info = self._pending_event
            self._pending_event = None
            self._timer = None

        if not event_info:
            return

        if not self._event:
            return

        timestamp = get_time_stamp()
        self._event(event_info, timestamp)


def get_time_stamp():
    now = time.localtime()
    timestamp = f"{now.tm_mday:02d}_{now.tm_mon:02d}_{now.tm_year:02d}__{now.tm_hour:02d}:{now.tm_min:02d}:{now.tm_sec:02d}"
    return timestamp


def parse_time_stamp(timestamp: str):
    return time.strptime(timestamp, "%d_%m_%Y__%H:%M:%S")


def main(path: Path, copy_dest: Path | None = None):
    def event_handler(event_info, timestamp):
        print(event_info)
        print(timestamp)

        print(parse_time_stamp(timestamp))

    if not path.exists():
        raise FileNotFoundError(path)

    if copy_dest and not copy_dest.exists():
        raise FileNotFoundError(copy_dest)

    handler = FolderWatcher(debounce_seconds=1, event=event_handler)
    observer = Observer()
    observer.schedule(handler, str(path), recursive=True)
    observer.start()
    print(f"Watching {path.resolve()} (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handler.stop()
        observer.stop()
    observer.join()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Watch a directory for file system events.")
    parser.add_argument("-f", "--folder", required=True,
                        type=Path, help="Folder to monitor.")
    parser.add_argument("-c", "--copyDest", type=Path,
                        help="Optional folder to copy changes to.")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    main(args.folder, args.copyDest)
