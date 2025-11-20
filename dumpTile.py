import urllib
import urllib.request
from pprint import pprint
import json
from pathlib import Path

import mapbox_vector_tile


def dump_to_file_json(path, jsonData):
    with open(path, mode="w", encoding="utf8") as file:
        json.dump(jsonData, file, indent=4)


url_basemap = "https://vectortiles2.geo.admin.ch/tiles/ch.swisstopo.relief.vt/v1.0.0/9/266/181.pbf"
#url_flur = 'https://maps.infas-lt.de/maps/05CA1656-C77F-4F11-AD88-724AEFBE79ED/prerelease/tiles/collections/grp_ags23_2024/tiles/WebMercatorQuad/12/1374/2173?f=application/vnd.mapbox-vector-tile'

#url_nl = "https://api.pdok.nl/kadaster/brt-achtergrondkaart/ogc/v1/tiles/NetherlandsRDNewQuad/3/2/2"

urls = [url_basemap]

pathFile = Path(__file__)
parent = pathFile.parent

for url in urls:
    read_data = urllib.request.urlopen(url).read()
    data = mapbox_vector_tile.decode(read_data)

   # pprint(list(data.keys()))

    data = {k: v for k, v in data.items()}
    #features_str = "features"

    # for v in data.values():
    #     features = v[features_str]
    #     features = [
    #         f
    #         for f in features
    #         if "properties" in f.keys() and "name" in f["properties"].keys() and 'Arsten' in f['properties']['name']
    #     ]
    #     v[features_str] = features
    #     # del v[features_str]

    ulr_ = url.replace("?", "")
    file = Path(ulr_).parts[-4:]
    file = "_".join(file)
    path = Path(parent, f"{file}.json")
    path_bin = Path(parent, f"{file}.pbf")

    # print(path, path_bin)

    Path(path_bin).write_bytes(read_data)

    dump_to_file_json(path, data)
