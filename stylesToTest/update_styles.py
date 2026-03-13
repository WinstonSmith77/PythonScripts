import requests
import json
import os
from urllib.parse import urlsplit
from pathlib import Path



HREF = "href"
REL = "rel"
LINKS = "links"
COLLECTIONS = "collections"
STYLES = "styles"
ID = "id"


def read_base_url():
    default_url = "https://maps.infas-lt.de/default"
    desktop_file = Path(os.environ.get("USERPROFILE", "")) / "OneDrive - Ipsos" /"Desktop" / "url_geoserver.txt"

    if desktop_file.is_file():
        value = desktop_file.read_text(encoding="utf-8").strip()
        if value:
            return value

    return default_url


base_url = read_base_url()

def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()
    return json.loads(response.content.decode("utf-8"))


def extract_last_url_path_part(url):
    path = urlsplit(url).path
    if not path:
        return ""
    return path


def print_json(data):
    print(json.dumps(data, indent=2))


def save_pretty_json(url, output_path):
    data = fetch_json(url)
    output_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


pretty_json = fetch_json(base_url)

# print_json(pretty_json)

# Find all links that end with "styles"
tilesets_url = [link for link in pretty_json[LINKS]
                if link[REL].endswith("tilesets-vector")][0][HREF]

collections_tiles = [link for link in fetch_json(
    tilesets_url)[LINKS] if link[REL] == 'data']


# print_json(collections)

collections_tiles = fetch_json(collections_tiles[0][HREF])[COLLECTIONS]

# print_json(collections_tiles)

names_to_styles = [(c[ID], [links[HREF] for links in c[LINKS] if links[HREF].endswith(
    "styles")][0]) for c in collections_tiles if collections_tiles]

names_to_styles = [(name, [link[HREF] for link in fetch_json(url)[
                    LINKS] if link[HREF].endswith("styles")][0]) for name, url in names_to_styles]

names_to_styles = [(name, [(styles[ID], [links for links in styles[LINKS] if links[REL].endswith(
    "stylesheet")][0]) for styles in fetch_json(url)[STYLES]]) for name, url in names_to_styles]
names_to_styles = [(name,   [(file[0], file[1][HREF])
                    for file in files]) for name, files in names_to_styles]

names_to_styles.append(("ch.swisstopo.basemap_world.vt", [("ch.swisstopo.basemap_world.vt.style", "https://vectortiles.geo.admin.ch/styles/ch.swisstopo.basemap_world.vt/style.json?key=xmETqTBaiAH9bbZXXiFm")]))

print(names_to_styles)

for name, files in names_to_styles:
    print(f"Name: {name}")

    for file_name, file_url in files:
        output_path = (Path(__file__).parent /"read_from_geoserver"/ name /
                       (file_name+".json")).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_pretty_json(file_url, output_path)
        print(f"Downloaded {file_name} to {output_path}")
