import os
from pathlib import Path
import xml.etree.ElementTree as ET


script_path = Path(os.path.abspath(__file__))
path_xml = script_path.parent / "tests.xml"
print(f"Current script path: {script_path}")

def read_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root


file = read_xml_file(path_xml)

print(file)


# Example usage:
# xml_root = read_xml_file('your_file.xml')
# for child in xml_root:
#     print(child.tag, child.attrib)