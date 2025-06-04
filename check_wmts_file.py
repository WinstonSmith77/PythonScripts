import xml.etree.ElementTree as ET

xml_file = 'WMTSList.xml'
providers = 'wmts_providers'
url = 'provider_url'

all_urls : list[str] = []

try:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    print(f"Root tag: {root.tag}")

    wmts_providers = root.find(providers)
    if wmts_providers is not None:
        for entry in wmts_providers:
            provider_url = entry.attrib.get(url)
            if provider_url:
                all_urls.append(provider_url)
               
    else:
        print("'wmts_providers' not found in the XML.")
except Exception as e:
    print(f"Error opening XML file: {e}")

print(all_urls)    