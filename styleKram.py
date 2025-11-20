import json
import pathlib
from itertools import groupby
from pprint import pprint

path = r"stylesToTest\basemap.de.new.json"

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


to_show = [(style[ID], style[FILTER]) for style in styles if FILTER in style] 


pprint(to_show)

