from pathlib import Path
import shutil

useMac: bool = False  # Set to False if you are not using a Mac

if useMac:
    stick = Path("/Volumes/AUTO")
    itunes_path = Path(
        "/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal/iTunes Music"
    )
else:
    stick = Path("C:/Users/matze/Desktop/stick")
    itunes_path = Path("C:/Users/matze/OneDrive/iTunes Music")


def delete_emypty_folders(path: Path):
    """Delete empty folders in the given path."""
    for item in path.iterdir():
        if item.is_dir():
            delete_emypty_folders(item)
            if not any(item.iterdir()):  # Check if the directory is empty
                item.rmdir()
                print(f"Deleted empty folder: {item}")


class SyncMusic:
    def __init__(self, stick: Path | str):
        self.sources: list[Path] = []
        self.destinations: list[Path] = []
        self.stick = Path(stick)

    def sync(self):
        # self.empty_or_make_folder(self.stick)
        stick.mkdir(parents=True, exist_ok=True)

        all_files: set[Path] = set(self.stick.rglob("*"))

        """Sync files from sources to destinations."""
        for source, destination in zip(self.sources, self.destinations):
            self.copy_files_to_usb(source, destination, all_files)

        files_to_delete = [file for file in all_files if file.is_file()]
        for to_delete in files_to_delete:
            to_delete.unlink()
            print(f"Deleted {to_delete}")

        folders_to_delete = [dir for dir in all_files if dir.is_dir()]
        for folder_to_delete in folders_to_delete:
            delete_emypty_folders(folder_to_delete)

    def copy_files_to_usb(self, source: Path, dest_folder: Path, all_files: set[Path]):
        total_dest_folder = stick / dest_folder
        print(f"Copying files from {source} to {total_dest_folder}")

        if not source.exists():
            print(f"Source folder {source} does not exist.")
            return

        for item in source.rglob("*"):
            if item.is_file():
                relative_path = item.relative_to(source)

                destination = total_dest_folder / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination in all_files:
                    print("~", end="", flush=True)
                    all_files.remove(destination)  # Remove from set to avoid duplicates
                    folder = destination
                    while True:
                        folder = folder.parent
                        if folder in all_files:
                            all_files.remove(folder)  # Remove parent folder as well
                        if folder == total_dest_folder:
                            break

                else:
                    shutil.copyfile(item, destination)
                    print("+", end="", flush=True)
        print()

    def add_to_sync(self, source_folder: str | Path, dest_folder: str | Path):
        self.sources.append(Path(source_folder))
        self.destinations.append(Path(dest_folder))


def add(sync: SyncMusic):
    """Copy music files to the USB stick."""

    music_path = itunes_path / "Music"
    music_new_path = itunes_path / "neue musik"

    sync.add_to_sync(music_new_path / "Christoph Waltz", "Christoph Waltz")

    sync.add_to_sync(music_path / "Arthur Conan Doyle", "Krimis")
    sync.add_to_sync(music_new_path / "In Vino Veritas", "Krimis/In Vino Veritas")
    sync.add_to_sync(music_new_path / "stelter", "Krimis/Stelter")
    sync.add_to_sync(music_new_path / "Agatha Christie", "Krimis/Agatha Christie")

    sync.add_to_sync(music_path / "Dirk Bach", "Walter Moers")
    sync.add_to_sync(music_path / "Walter Moers", "Walter Moers")
    sync.add_to_sync(music_new_path / "Moers_Einhörnchen", "Walter Moers/Einhörnchen")

    sync.add_to_sync(music_new_path / "Horst Evers", "Horst Evers")

    sync.add_to_sync(music_path / "Marc-Uwe Kling", "Marc-Uwe Kling")

    sync.add_to_sync(music_path / "Die Drei ___", "Die Drei Fragezeichen")
    sync.add_to_sync(music_new_path / "paletti", "paletti")

    sync.add_to_sync(music_new_path / "Christian Humberg", "Eifel/Christian Humberg")


if __name__ == "__main__":
    sync: SyncMusic = SyncMusic(stick)
    add(sync)
    sync.sync()
