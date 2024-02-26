import json
import pathlib
from pprint import pprint


path = r"bm_web_col.json"


LAYERS = 'layers'
TYPE = 'type'
SYMBOL = 'symbol'
LAYOUT = 'layout'
TEXT_FONT = 'text-font'
ID = 'id'

content = json.loads(pathlib.Path(path).read_text())

styles = content[LAYERS]

def get_id_set(items):
    return set(item[ID] for item in items)

symbols = (style for style in styles if style[TYPE] == SYMBOL)
hasFont = (style for style in styles if LAYOUT in style and TEXT_FONT in style[LAYOUT] and 'weg'.lower() in style[ID].lower())
aubahn = (style for style in styles if 'Nummer_Autobahn' == style[ID])


pprint(list(hasFont))
pprint(list(aubahn))


