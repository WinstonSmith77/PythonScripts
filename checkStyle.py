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

grouped_styles = {}
for style in styles:
    source_layer = style['source-layer']
    list_for_styles = grouped_styles.setdefault(source_layer, [])
    list_for_styles.append(style['id'])


grouped_styles = dict(sorted(grouped_styles.items(), key=lambda x: x[0]))


source_layers = [i for i in grouped_styles]

#pprint((grouped_styles))
pprint((source_layers))
#pprint(list(aubahn))


