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

def split_file(file:str):
    start = -1
    end = -1
    count = 0   
    for i, c in enumerate(file):
       if c == '{':
           count += 1
           if count == 1:
               start = i
       elif c == '}': 
           count -= 1
           if count == 0:
               end = i
       if count == 0 and start != -1 and end != -1:
           yield file[start:end+1]
           start = -1
           end = -1        
    


class Pipeline:
    count = 0
    folder = Path('glyphs')
    folder.mkdir(exist_ok=True)
    @classmethod
    def process(cls, glyphPath):
        read = Path(glyphPath).read_text(encoding='utf-8')
        for item in split_file(read):
           # print(item)
            bitmap = parse(json.loads(item))
        # print(bitmap)
            create_grayscale_image(bitmap, Path(cls.folder, f'{cls.count}.png'))
            cls.count += 1



pipeline = Pipeline()
pipeline.process('glyph.json')








