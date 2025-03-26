import json
import pathlib
from itertools import groupby
from pprint import pprint

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


styles = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))[LAYERS]

styles = [(style[ID], style[SOURCE_LAYER], style[TYPE]) for style in styles if SOURCE_LAYER  in style ]

styles_to_type = [item for item in sorted(styles, key=lambda x: x[2])]

styles_to_type = [(key, len(list(group))) for key, group in groupby(styles_to_type, key=lambda x: x[2])]

pprint(styles_to_type)

