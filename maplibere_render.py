import json
import pathlib
from itertools import groupby
from typing import Any, Tuple

import urllib.request

from pathlib import Path
from pprint import pprint
import mapbox_vector_tile

parent = Path(__file__).parent
path = Path(parent, "##tiles_render.json")
pathOutput = Path(parent, "##output.txt")


def dump_to_file_json(path, jsonData):
    with open(path, mode="w", encoding="utf-8") as file:
        json.dump(jsonData, file, indent=4)


def read_tile():
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

    def get_rgb(color: str):
        if color.startswith("rgb"):
            return tuple(map(int, color[4:-1].split(",")))
        else:
            return color

    def is_very_blue(color: tuple[int, int, int]):
        if not isinstance(color, tuple):
            return False
        return color[2] > (color[0] + 20) and color[2] > (color[1] + 20)

    content: dict[str, Any] = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))

    def filter_styles_content(
        style: dict[str, Any], to_filter: list[str]
    ) -> dict[str, Any]:
        return {key: value for key, value in style.items() if key in to_filter}

    # styles = [style for style in content[LAYERS]]
    # styles = (style for style in styles if PAINT in style and FILL_COLOR not in style[PAINT]  )
    # styles = ((style, get_rgb(str(style[PAINT][FILL_COLOR]))) for style in styles if PAINT in style and FILL_COLOR in style[PAINT])
    # styles = ((style, color) for (style, color) in styles if is_very_blue(color))
    #
    stylesDisplay = [
        filter_styles_content(style, [SOURCE_LAYER, ID, TYPE, FILTER])
        for style in content[LAYERS]
    ]

    # types = set(style[TYPE] for style in list(styles))

    # stylesForType = {type : [style[ID] for style in stylesDisplay if style[TYPE] == type] for type in types}

    return stylesDisplay

    #
    # pprint(stylesForType)


styles = get_styles()
tile_data = read_tile()

# pprint(styles)
# print(tile_data)


def pass_filter(filter: list, properties: dict[str, Any]) -> bool:
    if not filter:
        return True

    operation, args = filter[0], filter[1:]

    class Operator:
        ALL = "all"
        ANY = "any"
        EQ = "=="
        IN = "in"
        NIN = "!in"
        NEQ = "!="
        NHAS = "!has"
        HAS = "has"
        LESSOREQ = "<="
        GREATER = ">"
        GREATEROREQ = ">="

        @staticmethod
        def invert_or_not(operation: str, x: bool) -> bool:
            if operation in [Operator.NEQ, Operator.NHAS, Operator.NIN]:
                return not (x)
            return x

    match operation:
        case Operator.EQ | Operator.IN | Operator.NIN:
            assert len(args) >= 1
            name_prop = args[0]

            if name_prop not in properties:
                return Operator.invert_or_not(operation, False)

            value_prop = properties[name_prop]

            compare_to_values = args[1:]
            must_be_in = [compare_to_value for compare_to_value in compare_to_values]

            return Operator.invert_or_not(operation, value_prop in must_be_in)
        
        case Operator.ALL | Operator.ANY:
            assert len(args) >= 1
            if operation == Operator.ANY:
                func = any
            else:
                func = all
            return func(pass_filter(cond, properties) for cond in args)

        case Operator.NEQ:
            assert len(args) >= 2
            name_prop = args[0]

            if name_prop not in properties:
                return True

            value_prop = properties[name_prop]

            must_be = args[1]
            return must_be == value_prop
       
        case Operator.NHAS | Operator.HAS:
            assert len(args) == 1
            return Operator.invert_or_not(operation, args[0] in properties)
        
        case Operator.LESSOREQ:
            assert len(args) == 2
            name_prop, value = args
            return properties.get(name_prop, 0) <= value
        
        case Operator.GREATER:
            assert len(args) == 2
            name_prop, value = args
            return properties.get(name_prop, 0) > value
        
        case Operator.GREATEROREQ:
            assert len(args) == 2
            name_prop, value = args
            return properties.get(name_prop, 0) >= value

        case _:
            assert False, f"Unknown filter: {operation}"

    return False


with open(pathOutput, mode="w", encoding="utf-8") as file:
    for style in styles:
        id = style[ID]
        source_layer = style[SOURCE_LAYER]
        filter = style[FILTER] if FILTER in style else []
        print(f'Styles: "{id}" Filter: "{filter}"', file=file)

        tab = " " * 4

        if source_layer in tile_data:
            print(f'{tab}matches SourceLayer "{source_layer}" ', file=file)
            layer_data = tile_data[source_layer]
            features = layer_data["features"]

            for feature in features:
                if pass_filter(filter, feature["properties"]):
                    properties = feature["properties"]
                    print(f"{tab * 2}{properties}", file=file)
