import json
import pathlib
from collections import namedtuple


read = json.loads(pathlib.Path('glyph.json').read_text(encoding='utf-8'))

def parse(data):
  
    pixels = tuple(data['bitmap']['data'].values())
    width = data['bitmap']['width']
    height = data['bitmap']['height']

    return namedtuple('Glyph', ['pixels', 'width', 'height'])(pixels, width, height)

print(parse(read))