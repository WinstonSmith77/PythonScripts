import pathlib
import shutil

stick  = pathlib.Path ("/Volumes/Matze/matze/Desktop/usb stick")


def copy_files_to_usb(source_folder: str, dest_folder: str | pathlib.Path):
    """Copy all files from the source folder to the USB stick folder."""
    source = pathlib.Path(source_folder)
    dest = pathlib.Path(dest_folder)

    for item in source.rglob("*"):
        if item.is_file():
            relative_path = item.relative_to(source)
            #folder_name = item.parts[-2]
            destination = dest / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(item.read_bytes())
            print(f"Copied {item} to {destination}")
        else:
            print(f"Skipping directory {item}")

def remove_all_files_in_folder(folder: str | pathlib.Path):
    shutil.rmtree(folder, ignore_errors=True)
        


remove_all_files_in_folder(stick)

stick.mkdir(parents=True, exist_ok=True)

trashes_path = stick / ".trashes"
pathlib.Path(trashes_path).touch()

copy_files_to_usb('/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal/iTunes Music/Music/Arthur Conan Doyle', stick / 'Krimis')
copy_files_to_usb('/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal/iTunes Music/neue musik/In Vino Veritas', stick / 'Krimis' / 'In Vino Veritas')

copy_files_to_usb('/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal/iTunes Music/Music/Dirk Bach', stick / 'Dirk Bach')
copy_files_to_usb('/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal/iTunes Music/neue musik/Horst Evers', stick / 'Horst Evers')
copy_files_to_usb('/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal/iTunes Music/Music/Die Drei ___', stick / 'Die Drei Fragezeichen')

