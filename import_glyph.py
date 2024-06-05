import json
from  pathlib import Path
from collections import namedtuple
from PIL import Image




def parse(data):
    bitmap = 'bitmap'
    pixels = tuple(data[bitmap]['data'].values())
    width = data[bitmap]['width']
    height = data[bitmap]['height']

    return namedtuple('Glyph', [bitmap, 'width', 'height'])(pixels, width, height)

def create_grayscale_image(bitmap, filename):
    image = Image.new('L', (bitmap.width, bitmap.height))
    image.putdata(bitmap.bitmap)
    image.save(filename)
    return image


class Pipeline:
    count = 0
    folder = Path('glyphs')
    folder.mkdir(exist_ok=True)
    @classmethod
    def process(cls, glyphPath):
        read = json.loads(Path(glyphPath).read_text(encoding='utf-8'))
        bitmap = parse(read)
        # print(bitmap)
        create_grayscale_image(bitmap, Path(cls.folder, f'{cls.count}.png'))
        cls.count += 1



pipeline = Pipeline()
pipeline.process('glyph.json')








