import urllib.request
from pathlib import Path

url = "https://vectortiles.geo.admin.ch/styles/ch.swisstopo.lightbasemap_world.vt/style.json?key=xmETqTBaiAH9bbZXXiFm"
output_path = Path("swiss_light_basemap.json").resolve()

print(f"Path: {output_path}")

# Ensure the directory exists
if output_path.parent != Path("."):
    output_path.parent.mkdir(parents=True, exist_ok=True)

print(f"Downloading from {url}...")
try:
    urllib.request.urlretrieve(url, output_path)
    print(f"Successfully saved to {output_path.resolve()}")
except Exception as e:
    print(f"Error downloading file: {e}")
