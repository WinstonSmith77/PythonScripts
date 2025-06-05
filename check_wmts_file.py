
import xml.etree.ElementTree as ET
import requests
# This script checks the existence of URLs in a WMTS XML file.

xml_file = 'WMTSList.xml'
providers = 'wmts_providers'
url = 'provider_url'
url_hint = 'usage_hint_url'

all_urls : list[str] = []
all_hint_urls : list[str] = []


def add_to_list(entry,  urls: list[str], url: str):
    provider_url = entry.attrib.get(url)
    if provider_url:
        urls.append(provider_url)

def check_url_exists(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        code = response.status_code
        return code == 200 
    except Exception:
        return False

def main():
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    
        wmts_providers = root.find(providers)
        if wmts_providers is not None:
            for entry in wmts_providers:
                add_to_list(entry, all_urls, url)
                add_to_list(entry, all_hint_urls, url_hint)
        else:
            print("'wmts_providers' not found in the XML.")
    except Exception as e:
        print(f"Error opening XML file: {e}")


    # print(all_urls)
    # print(all_hint_providers)

    non_existing_urls = [u for u in all_urls if not check_url_exists(u)]
    print("Non Existing URLs:")
    print(non_existing_urls)
    

    non_existing_hint_urls = [u for u in all_hint_urls if not check_url_exists(u)]
    print("Non Existing Hint URLs:")
    print(non_existing_hint_urls)
        
if __name__ == "__main__":
    main()