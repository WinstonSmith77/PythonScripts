from pathlib import Path
import shutil
#from mutagen.mp3 import MP3

use_mac: bool = True  # Set to False if you are not using a Mac

if use_mac:
    demo = True

    stick = Path("/Volumes/Matze/matze/Desktop/stick" if demo else "/Volumes/AUTO")
    itunes_path = Path(
        "/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal/iTunes Music"
    )
else:
    stick = Path("C:/Users/matze/Desktop/stick")
    itunes_path = Path("C:/Users/matze/OneDrive/iTunes Music")


def delete_emypty_folders_recursive(path: Path):
    """Delete empty folders in the given path."""
    for item in path.iterdir():
        if item.is_dir():
            delete_emypty_folders_recursive(item)
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

        all_files: set[Path] = set(file for file in self.stick.rglob("*", case_sensitive=True) if file.is_file())

        """Sync files from sources to destinations."""
        for source, destination in zip(self.sources, self.destinations):
          #  self.__check_mp3(source)
            self.__copy_files_to_usb(source, destination, all_files)

        files_to_delete = [file for file in all_files if file.is_file()]
        for to_delete in files_to_delete:
            to_delete.unlink()
            print(f"Deleted {to_delete}")

        delete_emypty_folders_recursive(self.stick)



    def __check_mp3(self,  source):
        if not source.exists():
            print(f"Source folder {source} does not exist.")
            return

        for item in source.rglob("*", case_sensitive=False):
            if item.is_file() and item.suffix.lower() == ".mp3":
                try:
                    audio = MP3(item)
                    print(f"{item}: {audio.pprint()}")
                except Exception as e:
                    print(f"Error reading MP3 metadata for {item}: {e}")
                
                
        


    def __copy_files_to_usb(
        self, source: Path, dest_folder: Path, all_files: set[Path]
    ):
        total_dest_folder = stick / dest_folder
        print(f"Copying files from {source} to {total_dest_folder}")

        if not source.exists():
            print(f"Source folder {source} does not exist.")
            return

        for item in source.rglob("*", case_sensitive=False):
            if item.is_file():
                relative_path = item.relative_to(source)

                destination = total_dest_folder / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination in all_files:
                    print("~", end="", flush=True)
                    all_files.remove(destination)  # Remove from set to avoid duplicates

                else:
                    shutil.copyfile(item, destination)
                    print("+", end="", flush=True)
        print()

    def add_to_sync(self, source_folder: str | Path, dest_folder: str | Path):
        self.sources.append(Path(source_folder))
        self.destinations.append(Path(dest_folder))


def add_stuff(sync: SyncMusic):
    """Copy music files to the USB stick."""

    music_path = itunes_path / "Music"
    music_new_path = itunes_path / "neue musik"

    krimis = "Krimis"

    sync.add_to_sync(music_path / "Arthur Conan Doyle", f"{krimis}")
   
    sync.add_to_sync(music_new_path / "stelter", f"{krimis}/Stelter")
    sync.add_to_sync(music_new_path / "Agatha Christie", f"{krimis}/Agatha Christie")
    sync.add_to_sync(music_new_path / "Gisbert Haefs", f"{krimis}/Gisbert Haefs")
    sync.add_to_sync(music_new_path / "durbridge", f"{krimis}/durbridge")
    


    wm = "Walter Moers"
    sync.add_to_sync(music_path / "Dirk Bach", wm)
    sync.add_to_sync(music_path / wm, wm)
    sync.add_to_sync(music_new_path / "Moers_Einhörnchen", f"{wm}/Einhörnchen")

    humor = "witzig"
    sync.add_to_sync(music_new_path / "Horst Evers", f"{humor}/Horst Evers")
    sync.add_to_sync(music_path / "Marc-Uwe Kling", f"{humor}/Marc-Uwe Kling")

    sync.add_to_sync(music_new_path / "Christian Humberg", "Eifel/Christian Humberg")

    kinder_lernen = "kinder lernen"
    sync.add_to_sync(music_new_path / "paletti", f"{kinder_lernen}/paletti")
    sync.add_to_sync(
        music_new_path / "Christoph Waltz", f"{kinder_lernen}/Christoph Waltz"
    )

    sync.add_to_sync(music_path / "Die Drei ___", "Die Drei Fragezeichen")
    sync.add_to_sync(music_path / "Die Drei Fragezeichen", "Die Drei Fragezeichen")

    sync.add_to_sync(music_path / "Jürgen Von Der Lippe"/"Ja Uff Erstmal - Winnetou Unter Comedy-G", f"{humor}/Jürgen Von Der Lippe")
    sync.add_to_sync(music_new_path / "In Vino Veritas", f"{krimis}/In Vino Veritas")

    sync.add_to_sync(music_new_path / 'Ben Aaronovitch', f'{krimis}Ben Aaronovitch')
    


   


if __name__ == "__main__":
    sync: SyncMusic = SyncMusic(stick)
    add_stuff(sync)
    sync.sync()


#rsync -avhP   --size-only --delete  stick/   /Volumes/AUTO/
