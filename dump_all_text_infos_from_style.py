import json
import pathlib
from itertools import groupby
from typing import Any



# path = r"merged_styles.json"
path = r"bm_web_col_.json"

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

def filter_texts_and_add_to(items_of_interest: dict[str, Any], add_to: dict[str, Any], style: dict[str, Any]):
    for key, value in items_of_interest.items():
        if  key.startswith("text-"):
            if key not in add_to:
                add_to[key] = []
            add_to[key].append((style[ID], str(value)))


groups_text_attribs: dict[str, Any] = {}
groups_text_attribs['style'] = path
groups = (LAYOUT, PAINT)
for group in groups:
    groups_text_attribs[group] = {}

    for style in styles:
        if group in style:
            filter_texts_and_add_to(style[group], groups_text_attribs[group], style)

def take_second(x):
    return x[1]

def order_and_groupBy(items, key):
    return groupby(sorted(items, key=key), key=key)   

for group in groups:
    for key, value in groups_text_attribs[group].items():
        groups_text_attribs[group][key] =  [(group_key, list(map(lambda x : x[0], list(group_items)))) for group_key, group_items in order_and_groupBy(value, key=take_second)]

# for group in groups:
#     for key in groups_text_attribs[group]:
#         groups_text_attribs[group][key] =   sorted(groups_text_attribs[group][key], key=lambda x: len(x[1]), reverse=True) 




info_text = pathlib.Path(f"info_text_{pathlib.Path(path).stem}.json")

json.dump(groups_text_attribs, info_text.open("w", encoding="utf-8"), indent=4)
