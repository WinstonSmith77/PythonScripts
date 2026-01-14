import json
from pathlib import Path


LAYERS_KEY = "layers"
LAYER_ID_KEY = "id"
LAYER_TYPE_KEY = "type"
PAINT_KEY = "paint"
FILL_COLOR_KEY = "fill-color"
LINE_WIDTH_KEY = "line-width"
LINE_DASH_ARRAY = "line-dasharray"



def load_style(path):
    text = Path(path).read_text()
    js = json.loads(text)
    return js


style_folder = Path(__file__).parent

first = load_style(Path(style_folder, "1.json"))

print(first)
