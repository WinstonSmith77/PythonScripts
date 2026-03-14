import os
from pathlib import Path
import json
import xml.etree.ElementTree as ET


script_path = Path(os.path.abspath(__file__))


fails = ["failed_geocode.xml", "failed_singleline.xml"]

output = script_path.parent / "output.text"

fail_text = []

for fail in fails:
    path_xml = script_path.parent / fail

    def read_xml(path):
        tree = ET.parse(path)
        root = tree.getroot()
        return root

    children = list(read_xml(path_xml))

    for child in children:
        fail_text.append(child.attrib["name"] + "\n" + child.attrib["status"] + "\n\n")

with open(output, "w", encoding="utf-8") as f:
    f.writelines(fail_text)
