import json
import pathlib
from collections import namedtuple
from PIL import Image, _imaging


read = json.loads(pathlib.Path('glyph.json').read_text(encoding='utf-8'))

def parse(data):
    bitmap = 'bitmap'
    pixels = tuple(data[bitmap]['data'].values())
    width = data[bitmap]['width']
    height = data[bitmap]['height']

    return namedtuple('Glyph', [bitmap, 'width', 'height'])(pixels, width, height)

def create_grayscale_image(pixels, width, height, filename):
    image = Image.new('L', (width, height))
    image.putdata(pixels)
    image.save(filename)
    return image


bitmap = parse(read)

print(bitmap)


create_grayscale_image(bitmap.bitmap, bitmap.width, bitmap.height, 'grayscale.png')