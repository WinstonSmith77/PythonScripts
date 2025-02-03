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
    args = parser.parse_args()

    return args.path

def get_styles(path):
    content: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))

    return content[LAYERS]


def filter_texts_and_add_to(
    items_of_interest: dict[str, Any], add_to: dict[str, Any], style: dict[str, Any]
):
    for key, value in items_of_interest.items():
        if key.startswith("text-"):
            if key not in add_to:
                add_to[key] = []
            add_to[key].append((style[ID], str(value)))


def take_second(x):
    return x[1]


def order_and_groupBy(items, key):
    return groupby(sorted(items, key=key), key=key)


def do_it(styles, path):
    groups_text_attribs: dict[str, Any] = {}
    groups_text_attribs["style"] = path
    groups = (LAYOUT, PAINT)
    for group in groups:
        groups_text_attribs[group] = {}

        for style in styles:
            if group in style:
                filter_texts_and_add_to(style[group], groups_text_attribs[group], style)

    for group in groups:
        for key, value in groups_text_attribs[group].items():
            items = [
                (group_key, list(map(lambda x: x[0], list(group_items))))
                for group_key, group_items in order_and_groupBy(value, key=take_second)
            ]

            items = sorted(items, key=lambda x: len(x[1]), reverse=True)

            groups_text_attribs[group][key] = items

    info_text = Path(f"info_text_{Path(path).stem}.json")

    json.dump(groups_text_attribs, info_text.open("w", encoding="utf-8"), indent=4)


if __name__ == "__main__":
    start_time = time.time()
    path = parse_args()
    styles = get_styles(path)
    do_it(styles, path)
    end_time = time.time()

    print(f"Execution time: {(end_time - start_time) * 1000} milliseconds")
