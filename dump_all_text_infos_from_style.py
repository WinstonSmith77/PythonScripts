import json
from pathlib import Path
from itertools import groupby
from typing import Any
import time
import argparse

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

def parse_args():
    parser = argparse.ArgumentParser(description="Process a JSON style file.")
    parser.add_argument("path", type=str, help="Path to the JSON style file")
    parser.add_argument(
        "--contains", type=str, default="", help='Filter keys that contain this string (default: "text-")'
    )
    parser.add_argument(
        "--valuecontains", type=str, default="", help='Filter values that contain this string (default: "")'
    )
    parser.add_argument(
        "--valuesonly", action="store_true", help="Only include styles where the value contains the specified string"
    )

    args = parser.parse_args()

    return args.path, args.contains, args.valuecontains, args.valuesonly

def get_styles(path):
    content: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))

    return content[LAYERS]

values_str_to_value : dict[str, Any] = {}

def filter_texts_and_add_to(
    items_of_interest: dict[str, Any], add_to: dict[str, Any], style: dict[str, Any], must_contain: str, value_must_contain: str, values_str_to_value : dict[str, Any]
):
    for key, value in items_of_interest.items():
        if key.startswith(must_contain):
            value_str = str(value)
            values_str_to_value[value_str] = value
            if value_must_contain in value_str:
                if key not in add_to:
                    add_to[key] = []
               
                add_to[key].append((style[ID], value_str))


def take_second(x):
    return x[1]


def order_and_groupBy(items, key):
    return groupby(sorted(items, key=key), key=key)

def format_with_(text: str):
    return f'_{text}' if text else ""

def make_path(folder :str, path: str, must_contain: str, value_must_contain: str, values_only: bool, group : str = ""):
    return Path(folder, f"info_text_{Path(path).stem}{format_with_(must_contain)}{format_with_(value_must_contain)}{format_with_("values_only" if values_only else "")}{format_with_(group)}.json")


groups = (LAYOUT, PAINT)

def do_it(styles, path, must_contain: str,  value_must_contain: str, values_only: bool):
    groups_text_attribs: dict[str, Any] = {}
    groups_text_attribs["style"] = path

    values_str_to_value : dict[str, Any] = {}

    for group in groups:
        groups_text_attribs[group] = {}

        for style in styles:
            if group in style:
                filter_texts_and_add_to(style[group], groups_text_attribs[group], style, must_contain, value_must_contain, values_str_to_value)

    for group in groups:
        for key, value in groups_text_attribs[group].items():
            items = [
                (group_key, list(map(lambda x: x[0], list(group_items))))
                for group_key, group_items in order_and_groupBy(value, key=take_second)
            ]

            items = sorted(items, key=lambda x: len(x[1]), reverse=True)

            
            items = [(values_str_to_value[ item[0]], item[1]) for item in items]

            if values_only:
                items = [item[0] for item in items]

            groups_text_attribs[group][key] = items

    folder = "info"

    Path(folder).mkdir(exist_ok=True)

    info_text_path = make_path(folder, path, must_contain, value_must_contain, values_only)
    json.dump(groups_text_attribs, info_text_path.open("w", encoding="utf-8"), indent=4)

    for group in groups:
        for key, value in groups_text_attribs[group].items():
            info_text_path = make_path(folder, path, must_contain, value_must_contain, values_only, key)

            to_write = [{'content' : item} for item in value ]    

            json.dump(to_write, info_text_path.open("w", encoding="utf-8"), indent=4)

if __name__ == "__main__":
    start_time = time.time()
    path, must_contain, value_must_contain, values_only = parse_args()
    styles = get_styles(path)
    do_it(styles, path, must_contain, value_must_contain, values_only)
    end_time = time.time()

    print(f"Execution time: {(end_time - start_time) * 1000} milliseconds")
