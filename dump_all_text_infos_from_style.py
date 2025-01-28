import json
import pathlib
from itertools import groupby
from typing import Any, Tuple


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

MINZOOM = "minzoom"
MAXZOOM = "maxzoom"

def get_rgb(color: str) :
        if color.startswith('rgb'):
            return tuple(map(int, color[4:-1].split(',')))
        else:
            return color


def is_color_check(color, check) -> bool:
    if isinstance(color, str):
       return check(get_rgb(color))
    
    colors = [c[1] for c in color['stops']]
    return any(map(check, map(get_rgb,colors)))

def is_very_given_color(color: tuple[int, int, int], color_to_check: tuple[int, int, int], max_diff) -> bool:
    return is_color_check(color, lambda color : abs(color[0] - color_to_check[0]) < max_diff and abs(color[1] - color_to_check[1]) < max_diff and abs(color[2] - color_to_check[2]) < max_diff)

def is_very_red(color: tuple[int, int, int]) :
    return is_color_check(color, lambda color : color[0] >  230 and color[1] < 150 and color[2] < 150)

def  filter_styles_content(style: dict[str, Any], to_filter : list[str]) -> dict[str, Any]:
        return {key : value for key, value in style.items() if key in to_filter}

def get_styles():
    

    content : dict[str, Any] = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))

    styles = [style for style in content[LAYERS]]
    stylesWithText = [style for style in content[LAYERS] if LAYOUT in style and TEXT_FIELD in style[LAYOUT]]
    #styles = (style for style in styles if PAINT in style and FILL_COLOR not in style[PAINT]  )
    # styles = ((style, get_rgb(str(style[PAINT][FILL_COLOR]))) for style in styles if PAINT in style and FILL_COLOR in style[PAINT])
    # styles = ((style, color) for (style, color) in styles if is_very_blue(color))
    #
    stylesDisplay = [filter_styles_content(style, [SOURCE_LAYER, ID, TYPE]) for style in content[LAYERS]]

    types = set(style[TYPE] for style in list(styles))

    stylesForType = {type : [style[ID] for style in stylesDisplay if style[TYPE] == type] for type in types}

    return styles

    #
    # pprint(stylesForType)



    source_layers = list(style[SOURCE_LAYER] for style in styles)

    i = 0
    while True:
        if i + 1 >= len(source_layers):
            break
        if source_layers[i] == source_layers[i + 1]:
            del source_layers[i + 1]
        else: 
            i+=1    



    tree = {}
    for style in styles:
        source_layer = style['source-layer']
        list_styles = tree.setdefault(source_layer, [])
        list_styles.append(style['id'])


    pathlib.Path("export.json").write_text(json.dumps(tree, indent=4), encoding="utf-8")

styles = get_styles()

styles = [style for style in styles if PAINT in style]
styles = [filter_styles_content(style, [PAINT, LAYOUT, ID]) for style in styles]   

#styles = [filter_styles_content(style, [PAINT, LAYOUT, ID]) for style in styles]   




def filter_texts(items_of_interest : dict[str, Any], add_to :  dict[str, Any] ):
      for key, value in items_of_interest.items():
         if not key.startswith('text-'):
             continue
        
         if key not in add_to:
             add_to[key] = []
         add_to[key].append((style[ID], value))

text_attribs : dict[str, Any] = {}
for group in  (LAYOUT, PAINT):
    text_attribs[group] = {}

    for style in styles:
        if group  in style:
            filter_texts(style[group], text_attribs[group])

#pprint(styles)
#pprint(text_attribs)

info_text = pathlib.Path("info_text.json")

json.dump(text_attribs, info_text.open("w", encoding="utf-8"), indent=4)