import json
import pathlib
from itertools import groupby


from pprint import pprint



path = r"bm_web_col.json"


LAYERS = 'layers'
TYPE = 'type'
SYMBOL = 'symbol'
LAYOUT = 'layout'
TEXT_FONT = 'text-font'
ID = 'id'
SOURCE_LAYER = 'source-layer'
PAINT = 'paint'
FILL_COLOR = "fill-color";

content = json.loads(pathlib.Path(path).read_text(encoding='utf-8'))

styles = [style for style in content[LAYERS]]
paints = [{key:value for key, value in style.items() if key in [PAINT, ID]} for style in content[LAYERS] if PAINT in style] 


pprint((paints))


