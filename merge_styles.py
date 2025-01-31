from pathlib import Path
from pprint import pprint
import json


ID = 'id'
STYLE = 'style'


def append_id(style, with_text):
    style[ID] = (with_text, style[ID]) 
    return style

pathStyles = Path(r'stylesToTest')

paths_styles = (list(pathStyles.glob("*.json")))

jsons = [(Path(style).stem, json.loads(style.read_text(encoding="utf-8"))) for style in paths_styles]
layers = [append_id(style, content[0])  for content in jsons for style in content[1]['layers']]


layers = sorted(layers, key=lambda x: x[ID])

layers_dict = {}


for layer in layers:
    id = layer[ID]
    while id in layers_dict:
        id = id + "_"
        layer[ID] = id
       
    layers_dict[id] = layer

layers = list(layers_dict.values())

to_save  = {"layers" : layers}
path = Path("merged_styles.json")

json.dump(to_save, path.open("w", encoding="utf-8"), indent=4)





