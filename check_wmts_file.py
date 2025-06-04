import xml.etree.ElementTree as ET

# Replace 'your_file.xml' with the path to your XML file
xml_file = 'WMTSList.xml'
try:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    print(f"Root tag: {root.tag}")

    # Find all entries under 'wmts_providers'
    wmts_providers = root.find('wmts_providers')
    if wmts_providers is not None:
        for entry in wmts_providers:
            print(ET.tostring(entry, encoding='unicode'))
    else:
        print("'wmts_providers' not found in the XML.")
except Exception as e:
    print(f"Error opening XML file: {e}")