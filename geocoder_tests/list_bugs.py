import os
from pathlib import Path
import xml.etree.ElementTree as ET


script_path = Path(os.path.abspath(__file__))
path_xml = script_path.parent / "tests.xml"
print(f"Current script path: {script_path}")


tree = ET.parse(path_xml)
root = tree.getroot()
children = list(root)

for child in children:
    print({child.attrib["name"]})

