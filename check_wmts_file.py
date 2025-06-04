import xml.etree.ElementTree as ET

# Replace 'your_file.xml' with the path to your XML file
xml_file = 'WMTSList.xml'

try:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    print(f"Root tag: {root.tag}")
except Exception as e:
    print(f"Error opening XML file: {e}")