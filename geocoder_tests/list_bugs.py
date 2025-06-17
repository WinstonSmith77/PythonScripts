import os
from pathlib import Path
import xml.etree.ElementTree as ET


script_path = Path(os.path.abspath(__file__))


fails = ["failed_geocode.xml"]

for fail in fails:

    path_xml = script_path.parent / fail


    print(f"Current script path: {script_path}")

    def read_xml(path):
        tree = ET.parse(path)
        root = tree.getroot()
        return root
    

    children = list(read_xml(path_xml))
    

    for child in children:
        print(child.attrib["name"])

