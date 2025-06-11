from pathlib import Path
import shutil

useMac: bool = False  # Set to False if you are not using a Mac

if useMac:
    stick = pathlib.Path("/Volumes/AUTO")
    itunes_path = pathlib.Path(
        "/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal/iTunes Music"
    )
else:
    stick = Path("C:/Users/matze/Desktop/stick")
    itunes_path = Path("C:/Users/matze/OneDrive/iTunes Music")


class SyncMusic:
    def __init__(self, stick: Path | str):
        self.sources: list[str | Path] = []
        self.destinations: list[str | Path] = []
        self.stick = Path(stick)

    def sync(self):
        self.empty_folder(self.stick)
        stick.mkdir(parents=True, exist_ok=True)

        """Sync files from sources to destinations."""
        for source, destination in zip(self.sources, self.destinations):
            self.copy_files_to_usb(source, destination)

    def copy_files_to_usb(
        self, source: Path, dest: Path
    ):
        """Copy all files from the source folder to the USB stick folder."""

        print(f"Copying files from {source} to {dest}")

        if not source.exists():
            print(f"Source folder {source} does not exist.")
            return

        for item in source.rglob("*"):
            if item.is_file():
                relative_path = item.relative_to(source)
                destination = dest / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(str(item), str(destination))

    def empty_folder(self, folder: Path):
        """Remove all content in the folder but keep the folder structure."""
      
        if folder.exists():
            for item in folder.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                        print(f"Removed file {item}")
                    elif item.is_dir():
                        shutil.rmtree(item, ignore_errors=True)
                        print(f"Removed directory {item}")
                except Exception as e:
                    print(f"Error removing {item}: {e}")

    def add_to_sync(
        self, source_folder: str | Path, dest_folder: str | Path
    ):
        self.sources.append(Path(source_folder))
        self.destinations.append(Path(dest_folder))


def add(sync: SyncMusic):
    """Copy music files to the USB stick."""

    music_path = itunes_path / "Music"
    music_new_path = itunes_path / "neue musik"

    sync.add_to_sync(music_new_path / "Christoph Waltz", stick / "Christoph Waltz")

    sync.add_to_sync(music_path / "Arthur Conan Doyle", stick / "Krimis")
    sync.add_to_sync(
        music_new_path / "In Vino Veritas", stick / "Krimis" / "In Vino Veritas"
    )
    sync.add_to_sync(music_new_path / "stelter", stick / "Krimis" / "Stelter")
    sync.add_to_sync(
        music_new_path / "Agatha Christie", stick / "Krimis" / "Agatha Christie"
    )

    sync.add_to_sync(music_path / "Dirk Bach", stick / "Walter Moers")
    sync.add_to_sync(music_path / "Walter Moers", stick / "Walter Moers")
    sync.add_to_sync(
        music_new_path / "Moers_Einhörnchen", stick / "Walter Moers" / "Einhörnchen"
    )

    sync.add_to_sync(music_new_path / "Horst Evers", stick / "Horst Evers")

    sync.add_to_sync(music_path / "Marc-Uwe Kling", stick / "Marc-Uwe Kling")

    sync.add_to_sync(music_path / "Die Drei ___", stick / "Die Drei Fragezeichen")
    sync.add_to_sync(music_new_path / "paletti", stick / "paletti")

    sync.add_to_sync(music_new_path / "Christian Humberg", stick / "Christian Humberg")


if __name__ == "__main__":
    sync: SyncMusic = SyncMusic(stick)
    add(sync)
    sync.sync()
