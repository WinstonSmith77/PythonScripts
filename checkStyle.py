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

def get_styles():
    def get_rgb(color: str) :
        if color.startswith('rgb'):
            return tuple(map(int, color[4:-1].split(',')))
        else:
            return color

    def is_very_blue(color: tuple[int, int, int]) :
        if not isinstance(color, tuple):
            return False
        return color[2] > (color[0] + 20)  and color[2] > (color[1] + 20)

    content : dict[str, Any] = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))

    def  filter_styles_content(style: dict[str, Any], to_filter : list[str]) -> dict[str, Any]:
        return {key : value for key, value in style.items() if key in to_filter}
    

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
styles = get_styles()

tree = {}
for style in styles:
    source_layer = style['source-layer']
    list_styles = tree.setdefault(source_layer, [])
    list_styles.append(style['id'])


pathlib.Path("export.json").write_text(json.dumps(tree, indent=4), encoding="utf-8")



first_ten_entries = list(styles)[:20]

csharp_list = "var stylesListToShow = new List<string> {\n"
csharp_list += ",\n".join(f'    "{style["id"]}"' for style in first_ten_entries)
csharp_list += "\n};"

print(csharp_list)

content : dict[str, Any] = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))

content[LAYERS] = [style for style in styles if style[SOURCE_LAYER] in ['Hintergrund',
                                                                        'Siedlungsflaeche'
                                                                         ]]

pathlib.Path(path.replace('.', '_.')).write_text(json.dumps(content, indent=4), encoding="utf-8")


