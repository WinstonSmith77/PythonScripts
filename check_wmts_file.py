import xml.etree.ElementTree as ET

xml_file = 'WMTSList.xml'
providers = 'wmts_providers'
url = 'provider_url'
url_hint = 'usage_hint_url'

all_urls : list[str] = []
all_hint_providers : list[str] = []


def add_to_list(entry,  urls: list[str], url: str):
    provider_url = entry.attrib.get(url)
    if provider_url:
        urls.append(provider_url)

try:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    print(f"Root tag: {root.tag}")

    wmts_providers = root.find(providers)
    if wmts_providers is not None:
        for entry in wmts_providers:
           add_to_list(entry, all_urls, url)
           add_to_list(entry, all_hint_providers, url_hint)
    else:
        print("'wmts_providers' not found in the XML.")
except Exception as e:
    print(f"Error opening XML file: {e}")

print(all_urls)    
print(all_hint_providers)    