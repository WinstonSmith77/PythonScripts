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

content = json.loads(pathlib.Path(path).read_text())

styles = [style for style in content[LAYERS]]
styles = sorted(styles, key=lambda x: x[SOURCE_LAYER])
styles = groupby(styles, key=lambda x: x[SOURCE_LAYER])
styles = {key: list([item[ID] for item in group]) for key, group in styles}

pprint((styles))


