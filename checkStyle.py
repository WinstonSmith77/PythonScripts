import json
import pathlib
import pprint


path = r"C:\Users\henning\source\easymapGit\dev\src\Test\LutumTappert.Test.VektorKachel\UnitTestFiles\style.json"


LAYERS = 'layers'
TYPE = 'type'
SYMBOL = 'symbol'
LAYOUT = 'layout'
TEXT_FONT = 'text-font'

content = json.loads(pathlib.Path(path).read_text())

styles = content[LAYERS]

symbols = (style for style in styles if style[TYPE] == SYMBOL)
hasFont = (style for style in styles if LAYOUT in style and TEXT_FONT in style[LAYOUT])

for style in hasFont:
    pprint.pprint(style[TYPE])


