import json
import pathlib
from itertools import groupby
from typing import Any, Tuple


from pprint import pprint


path = r"bm_web_col.json"

LAYERS = "layers"
TYPE = "type"
SYMBOL = "symbol"
LAYOUT = "layout"
TEXT_FONT = "text-font"
ID = "id"
SOURCE_LAYER = "source-layer"
PAINT = "paint"
FILL_COLOR = "fill-color"

MINZOOM = "minzoom"
MAXZOOM = "maxzoom"

def get_rgb(color: str) :
    if color.startswith('rgb'):
        return tuple(map(int, color[4:-1].split(',')))
    else:
        return color

def is_blue(color: tuple[int, int, int]) :
    if not isinstance(color, tuple):
        return False
    return color[2] > (color[0] + 20)  and color[2] > (color[1] + 20)

content : dict[str, Any] = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))

styles = (style for style in content[LAYERS])
styles = ((style, get_rgb(str(style[PAINT][FILL_COLOR]))) for style in styles if PAINT in style and FILL_COLOR in style[PAINT])
styles = ((style, color) for (style, color) in styles if is_blue(color))


pprint(list(styles))