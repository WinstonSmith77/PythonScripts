import urllib
import urllib.request
from pprint import pprint
import json
import pathlib

import mapbox_vector_tile

def dump_to_file_json(path, jsonData):
   
    with open(path, mode="w", encoding='utf8') as file:
        json.dump(jsonData, file, indent=4)


url_basemap = 'https://sgx.geodatenzentrum.de/gdz_basemapde_vektor/tiles/v1/bm_web_de_3857/6/33/20.pbf'
url_flur = 'https://maps.infas-lt.de/maps/05CA1656-C77F-4F11-AD88-724AEFBE79ED/prerelease/tiles/collections/grp_ags23_2024/tiles/WebMercatorQuad/12/1374/2173?f=application/vnd.mapbox-vector-tile'

url_add_file =  [(url_basemap, 'basemap'), (url_flur, 'flur')]       

pathFile = pathlib.Path(__file__)
parent = pathFile.parent

for url, file in url_add_file:
    tile = urllib.request.urlopen(url).read()
    data = mapbox_vector_tile.decode(tile)
    path = pathlib.Path(parent, f'{file}.json')

    dump_to_file_json(path, data)



