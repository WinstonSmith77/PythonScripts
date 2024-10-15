import json
import pathlib
from itertools import groupby
from typing import Any, Tuple


from pprint import pprint

def get_styles():
    path = r"bm_web_col.json"

    LAYERS = "layers"
    FILTER = "filter"
    TYPE = "type"
    SYMBOL = "symbol"
    LAYOUT = "layout"
    TEXT_FONT = "text-font"
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

    def is_very_blue(color: tuple[int, int, int]) :
        if not isinstance(color, tuple):
            return False
        return color[2] > (color[0] + 20)  and color[2] > (color[1] + 20)

    content : dict[str, Any] = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))

    def  filter_styles_content(style: dict[str, Any], to_filter : list[str]) -> dict[str, Any]:
        return {key : value for key, value in style.items() if key in to_filter}
    

    styles = [style for style in content[LAYERS]]
    #styles = (style for style in styles if PAINT in style and FILL_COLOR not in style[PAINT]  )
    # styles = ((style, get_rgb(str(style[PAINT][FILL_COLOR]))) for style in styles if PAINT in style and FILL_COLOR in style[PAINT])
    # styles = ((style, color) for (style, color) in styles if is_very_blue(color))
    #
    stylesDisplay = [filter_styles_content(style, [SOURCE_LAYER, ID, TYPE, FILTER]) for style in content[LAYERS]]

    types = set(style[TYPE] for style in list(styles))

    stylesForType = {type : [style[ID] for style in stylesDisplay if style[TYPE] == type] for type in types}

    return stylesDisplay

    #
    # pprint(stylesForType)
pprint(get_styles())