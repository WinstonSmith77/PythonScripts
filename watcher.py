import time
from argparse import ArgumentParser, ArgumentTypeError
import threading
import shutil
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
    timestamp = f"{now.tm_mday:02d}_{now.tm_mon:02d}_{now.tm_year:02d}__{now.tm_hour:02d}_{now.tm_min:02d}_{now.tm_sec:02d}"
    return timestamp


def prune_snapshots(base_dir: Path, keep: int | None) -> None:
    if keep is None:
        return

    dirsAndParsedTime = ((entry, parse_time_stamp(
        entry.parts[-1])) for entry in base_dir.iterdir())
    snapshots = [
        entry for entry in dirsAndParsedTime if entry[0].is_dir() and entry[1]]

    if len(snapshots) <= keep:
        return

    snapshots = sorted(
        snapshots, key=lambda pathAndParsedTime: pathAndParsedTime[1], reverse=True)[keep:]
    for obsolete in (snapshot[0] for snapshot in snapshots):
        try:
            shutil.rmtree(obsolete)
            print(f"Removed snapshot {obsolete}")
        except Exception as exc:
            print(f"Failed to remove snapshot {obsolete}: {exc}")


def parse_time_stamp(timestamp: str) -> time.struct_time | None:
    try:
        return time.strptime(timestamp, "%d_%m_%Y__%H_%M_%S")
    except:
        return None


def is_subpath(child: Path, parent: Path):
    # .resolve() makes the path absolute and follows symlinks
    child = Path(child).resolve()
    parent = Path(parent).resolve()

    # Check if parent is actually a parent (or the same as) child
    return parent.is_relative_to(child)


def main(toWatch: Path, keep: int | None, copy_dest: Path):
    def event_handler(event_info, timestamp):
        print(event_info)
        print(timestamp)

        print(parse_time_stamp(timestamp))

        if copy_dest:
            try:
                destination = copy_dest / timestamp / toWatch.parts[-1]
                shutil.copytree(toWatch, destination,
                                dirs_exist_ok=True, ignore=shutil.ignore_patterns('.git'))
                print(f"Copied {toWatch} to {destination}")
            except Exception as exc:
                print(f"Failed to copy {toWatch} to {destination}: {exc}")

            prune_snapshots(copy_dest, keep=keep)

    if not toWatch.exists():
        raise FileNotFoundError(toWatch)

    if keep is not None and keep < 1:
        raise ValueError("keep must be at least 1 or None")

    if not copy_dest.exists():
        raise FileNotFoundError(copy_dest)
    if not copy_dest.is_dir():
        raise NotADirectoryError(copy_dest)
    if is_subpath(copy_dest, toWatch):
        raise FileNotFoundError(
            f"{copy_dest} is inside or equal {toWatch}")

    event_handler("init", get_time_stamp())

    handler = FolderWatcher(debounce_seconds=1, event=event_handler)
    observer = Observer()
    observer.schedule(handler, toWatch, recursive=True)
    observer.start()
    print(f"Watching {toWatch.resolve()} (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handler.stop()
        observer.stop()
    observer.join()


def parse_args():
    def parse_keep_arg(raw: str) -> int | None:
        if raw.lower() == "none":
            return None
        try:
            value = int(raw)
        except ValueError as exc:
            raise ArgumentTypeError(
                "keep must be an integer or 'none'") from exc
        if value < 1:
            raise ArgumentTypeError("keep must be at least 1 or 'none'")
        return value

    parser = ArgumentParser(
        description="Watch a directory for file system events.")
    parser.add_argument("-f", "--folder", required=True,
                        type=Path, help="Folder to monitor.")
    parser.add_argument("-c", "--copyDest", type=Path, required=True,
                        help="Folder to copy changes to.")
    parser.add_argument("-k", "--keep", type=parse_keep_arg, default=10,
                        help="Snapshots to retain (integer) or 'none' to keep everything (default: 10)")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    main(toWatch=args.folder, copy_dest=args.copyDest, keep=args.keep)
