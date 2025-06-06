import pathlib
import shutil

stick = pathlib.Path("/Volumes/AUTO")


def copy_files_to_usb(
    source_folder: str | pathlib.Path, dest_folder: str | pathlib.Path
):
    """Copy all files from the source folder to the USB stick folder."""
    source = pathlib.Path(source_folder)
    dest = pathlib.Path(dest_folder)

    print(f"Copying files from {source} to {dest}")

    if not source.exists():
        print(f"Source folder {source} does not exist.")
        return

    for item in source.rglob("*"):
        if item.is_file():
            relative_path = item.relative_to(source)
            # folder_name = item.parts[-2]
            destination = dest / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(item.read_bytes())


def empty_folder(folder: str | pathlib.Path):
    """Remove all content in the folder but keep the folder structure."""
    folder_path = pathlib.Path(folder)
    if folder_path.exists():
        for item in folder_path.iterdir():
            try:
                item = pathlib.Path(item)
                if item.is_file():
                    item.unlink()
                    print(f"Removed file {item}")
                elif item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                    print(f"Removed directory {item}")
            except Exception as e:
                print(f"Error removing {item}: {e}")


def prepare_stick():
    empty_folder(stick)
    stick.mkdir(parents=True, exist_ok=True)

    # trashes_path = stick / ".trashes"
    # pathlib.Path(trashes_path).touch()


def copy():
    """Copy music files to the USB stick."""
    itunes_path = pathlib.Path(
        "/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal/iTunes Music"
    )
    music_path = itunes_path / "Music"
    music_new_path = itunes_path / "neue musik"

    copy_files_to_usb(music_new_path / "Christoph Waltz", stick / "Christoph Waltz")

    copy_files_to_usb(music_path / "Arthur Conan Doyle", stick / "Krimis")
    copy_files_to_usb(
        music_new_path / "In Vino Veritas", stick / "Krimis" / "In Vino Veritas"
    )
    copy_files_to_usb(music_new_path / "stelter", stick / "Krimis" / "Stelter")
    copy_files_to_usb(
        music_new_path / "Agatha Christie", stick / "Krimis" / "Agatha Christie"
    )

    copy_files_to_usb(music_path / "Dirk Bach", stick / "Walter Moers")
    copy_files_to_usb(music_path / "Walter Moers", stick / "Walter Moers")
    copy_files_to_usb(
        music_new_path / "Moers_EInhörnchen", stick / "Walter Moers" / "Einhörnchen"
    )

    copy_files_to_usb(music_new_path / "Horst Evers", stick / "Horst Evers")

    copy_files_to_usb(music_path / "Marc-Uwe Kling", stick / "Marc-Uwe Kling")

    copy_files_to_usb(music_path / "Die Drei ___", stick / "Die Drei Fragezeichen")
    copy_files_to_usb(music_new_path / "paletti", stick / "paletti")

    copy_files_to_usb(music_new_path / "Christian Humberg", stick / "Christian Humberg")


if __name__ == "__main__":
    prepare_stick()
    copy()
    print("Finished copying files to USB stick.")
