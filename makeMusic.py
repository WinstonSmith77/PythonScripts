import os
import pathlib

stick : str ="/Volumes/Matze/matze/Desktop/usb stick"
trashes_path = pathlib.Path(stick) / ".trashes"

pathlib.Path(trashes_path).touch()
