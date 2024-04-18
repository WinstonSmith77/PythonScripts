import urllib
import urllib.request
from pprint import pprint
import json
import pathlib

import mapbox_vector_tile

def dump_to_file_json(path, jsonData):
   
    with open(path, mode="w", encoding='utf8') as file:
        json.dump(jsonData, file, indent=4)


url = 'https://sgx.geodatenzentrum.de/gdz_basemapde_vektor/tiles/v1/bm_web_de_3857/6/33/20.pbf'
tile = urllib.request.urlopen(url).read()

data = mapbox_vector_tile.decode(tile)

path = pathlib.Path(__file__)
parent = path.parent
file = pathlib.Path(parent, 'dump.json')

dump_to_file_json(file, data)




