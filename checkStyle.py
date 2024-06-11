import json
import pathlib
from pprint import pprint
from itertools import groupby


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

styles_sorted = sorted(styles, key=lambda x: x['source-layer'])
styles_by_source_layer = [(g[0], [s['id'] for s in list(g[1])]) for g in groupby(styles_sorted, key=lambda x: x['source-layer'])]
styles_by_source_layer = sorted(styles_by_source_layer, key=lambda x: x[0])

source_layers = [i[0] for i in styles_by_source_layer]

pprint(list(source_layers))
#pprint(list(aubahn))


