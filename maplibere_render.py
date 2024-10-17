import json
import pathlib
from itertools import groupby
from typing import Any, Tuple
import functools
import time

import urllib.request

from pathlib import Path
from pprint import pprint
import mapbox_vector_tile

parent = Path(__file__).parent
path = Path(parent, "##tiles_render.json")
pathOutput = Path(parent, "##output.json")
pathOfI = Path(parent, "##poi.json")

lines_oi: set | None = set()
show_skipped = False

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
        # data = None
        dump_to_file_json(path, data)

    return data

LAYERS = "layers"
FILTER = "filter"
TYPE = "type"
SYMBOL = "symbol"
LAYOUT = "layout"
TEXT_FONT = "text-font"
TEXT_FIELD = "text-field"
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

    styles = [style for style in content[LAYERS]]
    # styles = (style for style in styles if PAINT in style and FILL_COLOR not in style[PAINT]  )
    # styles = ((style, get_rgb(str(style[PAINT][FILL_COLOR]))) for style in styles if PAINT in style and FILL_COLOR in style[PAINT])
    # styles = ((style, color) for (style, color) in styles if is_very_blue(color))
    #
    stylesDisplay = [
        filter_styles_content(style, [SOURCE_LAYER, ID, TYPE, FILTER, LAYOUT])
        for style in styles
    ]

    # types = set(style[TYPE] for style in list(styles))

    # stylesForType = {type : [style[ID] for style in stylesDisplay if style[TYPE] == type] for type in types}

    return styles

    #
    # pprint(stylesForType)

def passes_filter(filter: list, properties: dict[str, Any]) -> bool:
    if not filter:
        return True

    class Operators:
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
        LESS = "<"

        @staticmethod
        def invert_or_not(operation: str, x: bool) -> bool:
            if operation in [Operators.NEQ, Operators.NHAS, Operators.NIN]:
                return not (x)
            return x

    operation = filter[0]

    def expand_item(item):
        if isinstance(item, str) and "," in item:
            return map(lambda x: x.strip(), item.split(","))
        return [item]

    def expand_items(set_to_test):
        return set(
            to_test for to_test in set_to_test for to_test in expand_item(to_test)
        )

    def tuple_to_str_seperated_by_semikolon(t):
        t = map(str, t)
        return f"({';;'.join(t)})"

    match filter:
        case [
            Operators.EQ
            | Operators.NEQ
            | Operators.IN
            | Operators.NIN,
            name_prop,
            *set_to_test,
        ]:
            value = properties.get(name_prop, None)

            result = Operators.invert_or_not(operation, value in set_to_test)

            if lines_oi is not None and any(
                map(lambda x: isinstance(x, str) and "," in x, set_to_test)
            ):
                if value and "," in value:
                    expanded_set = expand_items(set_to_test)
                    expanded_value = expand_item(value)
                    result2 = Operators.invert_or_not(
                        operation, any(map(lambda x: x in expanded_set, expanded_value))
                    )
                    to_add = "!!!!!" if result != result2 else ""
                    line_to_print = f"{to_add}{value} <> {tuple_to_str_seperated_by_semikolon(tuple(set_to_test))}{to_add}"
                    lines_oi.add(line_to_print)

            return result

        case [Operators.ALL | Operators.ANY, *sub_filters]:
            if operation == Operators.ANY:
                any_or_all = any
            else:
                any_or_all = all
            return any_or_all(
                passes_filter(sub_filter, properties) for sub_filter in sub_filters
            )

        case [Operators.NHAS | Operators.HAS, name_prop]:
            return Operators.invert_or_not(operation, name_prop in properties)

        case [
            Operators.LESSOREQ
            | Operators.LESS
            | Operators.GREATER
            | Operators.GREATEROREQ,
            name_prop,
            value,
        ]:
            if name_prop not in properties:
                return False

            stored_value = properties[name_prop]

            match operation:
                case Operators.LESSOREQ:
                    return stored_value <= value
                case Operators.LESS:
                    return stored_value < value
                case Operators.GREATER:
                    return stored_value > value
                case Operators.GREATEROREQ:
                    return stored_value >= value
        case _:
            assert False, f"Unknown filter: {operation}"

    return False

def benchmark(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        stop_time = time.time()
        delta = stop_time - start_time
        print(f"{f.__name__} Delta {delta}")
        return result

    return wrapper

@benchmark
def main():
    styles = get_styles()
    tile_data = read_tile()
   
    output = []
    for style in styles:
        id = style[ID]
        source_layer = style[SOURCE_LAYER]
        if MINZOOM in style:
            min_zoom = style[MINZOOM]
        else:
            min_zoom = ""

        if MAXZOOM in style:
            max_zoom = style[MAXZOOM]
        else:
            max_zoom = ""

        if min_zoom != "" and max_zoom != "":
            zoom_text = f" Zoom: {(min_zoom, max_zoom)}"
        else:
            zoom_text = None

        filter = style[FILTER] if FILTER in style else []

        if LAYOUT in style and TEXT_FIELD in style[LAYOUT]:
            text_name = style[LAYOUT][TEXT_FIELD]
        else:
            text_name = None

        style_outputs = []
        if source_layer in tile_data:
           
            layer_data = tile_data[source_layer]
            features = layer_data["features"]

            features_output = []
            for feature in features:
                feature_output = []
                properties = feature["properties"]
                passed = passes_filter(filter, properties)
                if passed or show_skipped:
                    feature_output.append(
                        f"{"NOT" if not passed else ""}{properties}"
                    )
                    feature_output.append(f"{feature['geometry']}")
                    if text_name:
                        if "{" not in text_name:
                            text = text_name
                        else:
                            text_name_stripped = text_name.strip("{}")
                            if text_name_stripped in properties:
                                text = properties[text_name_stripped]
                            else:
                                text = None
                        if text:
                            feature_output.append(
                                f"Text: '{text_name}' {text}"
                            )
                    features_output.append(feature_output)        

            if features_output:
                style_outputs.append(f'matches SourceLayer "{source_layer}" ')
                style_outputs.append(features_output)

        if style_outputs:
            style_outputs.insert(
                0,
                f'Styles: "{id}" Filter: "{filter}" {zoom_text if zoom_text else ""}',
            )

        if style_outputs:
            output.append(style_outputs)  

    dump_to_file_json(pathOutput, output)    

main()


if lines_oi is not None:
    dump_to_file_json(pathOfI, list(lines_oi))
    