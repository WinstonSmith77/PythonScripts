import json
import pathlib
from itertools import groupby
from typing import Any

path = r"bm_web_col.json"

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
    content: dict[str, Any] = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))

    return content[LAYERS]


styles = get_styles()

def filter_texts_and_add_to(items_of_interest: dict[str, Any], add_to: dict[str, Any]):
    for key, value in items_of_interest.items():
        if  key.startswith("text-"):
            if key not in add_to:
                add_to[key] = []
            add_to[key].append((style[ID], value))


groups_text_attribs: dict[str, Any] = {}
groups = (LAYOUT, PAINT)
for group in groups:
    groups_text_attribs[group] = {}

    for style in styles:
        if group in style:
            filter_texts_and_add_to(style[group], groups_text_attribs[group])

for group in groups:
    for key, value in groups_text_attribs[group].items():
     groups_text_attribs[group][key] =  [(group_key, list(map(lambda x: x[0], group_items))) for group_key, group_items in groupby(value, key=lambda x: x[1])]

info_text = pathlib.Path("info_text.json")

json.dump(groups_text_attribs, info_text.open("w", encoding="utf-8"), indent=4)
