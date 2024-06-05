import json
import pathlib
from collections import namedtuple


read = json.loads(pathlib.Path('glyph.json').read_text(encoding='utf-8'))

def parse(data):
  
    pixels = tuple(read['bitmap']['data'].values())
    width = read['bitmap']['width']
    height = read['bitmap']['height']

    return namedtuple( ['pixels', 'width', 'height'])(pixels, width, height)

print(parse(read))