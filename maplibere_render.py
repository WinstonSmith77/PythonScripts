import json
import pathlib
from itertools import groupby
from typing import Any, Tuple

import urllib.request

from pathlib import Path 
from pprint import pprint
import mapbox_vector_tile

def dump_to_file_json(path, jsonData):
    with open(path, mode="w", encoding="utf8") as file:
        json.dump(jsonData, file, indent=4)

def read_tile():
    parent = Path(__file__).parent
    path = Path(parent, "##tiles_render.json")

    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    
    else:
        url = "https://sgx.geodatenzentrum.de/gdz_basemapde_vektor/tiles/v1/bm_web_de_3857/13/4297/2667.pbf"
        read_data = urllib.request.urlopen(url).read()
        data = mapbox_vector_tile.decode(read_data)
        dump_to_file_json(path, data)

    return data
LAYERS = "layers"
FILTER = "filter"
TYPE = "type"
SYMBOL = "symbol"
LAYOUT = "layout"
TEXT_FONT = "text-font"
ID = "id"
SOURCE_LAYER = "source-layer"
PAINT = "paint"
FILL_COLOR = "fill-color"
LINE_COLOR = "line-color"
LINE_WIDTH = "line-width"
LINE_OPACITY = "line-opacity"

MINZOOM = "minzoom"
MAXZOOM = "maxzoom"

def get_styles():
    path = r"bm_web_col.json"

    def get_rgb(color: str) :
        if color.startswith('rgb'):
            return tuple(map(int, color[4:-1].split(',')))
        else:
            return color

    def is_very_blue(color: tuple[int, int, int]) :
        if not isinstance(color, tuple):
            return False
        return color[2] > (color[0] + 20)  and color[2] > (color[1] + 20)

    content : dict[str, Any] = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))

    def  filter_styles_content(style: dict[str, Any], to_filter : list[str]) -> dict[str, Any]:
        return {key : value for key, value in style.items() if key in to_filter}
    

    styles = [style for style in content[LAYERS]]
    #styles = (style for style in styles if PAINT in style and FILL_COLOR not in style[PAINT]  )
    # styles = ((style, get_rgb(str(style[PAINT][FILL_COLOR]))) for style in styles if PAINT in style and FILL_COLOR in style[PAINT])
    # styles = ((style, color) for (style, color) in styles if is_very_blue(color))
    #
    stylesDisplay = [filter_styles_content(style, [SOURCE_LAYER, ID, TYPE, FILTER]) for style in content[LAYERS]]

    types = set(style[TYPE] for style in list(styles))

    stylesForType = {type : [style[ID] for style in stylesDisplay if style[TYPE] == type] for type in types}

    return stylesDisplay

    #
    # pprint(stylesForType)

styles = get_styles()
tile_data = read_tile()

#pprint(styles)
#print(tile_data)



for style in styles:
    id = style[ID]
    source_layer = style[SOURCE_LAYER]
    filter = style[FILTER] if FILTER in style else []

    if source_layer in tile_data:
        pprint(f'Styles: "{id}" matches SourceLayer "{source_layer}" Filter "{filter}"')
        layer_data = tile_data[source_layer]
        features = layer_data["features"]

        pprint(len(features))
        # for feature in features:
        #     properties = feature["properties"]
        #     pprint(properties)
     