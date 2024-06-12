import json
from pathlib import Path
from collections import namedtuple
import shutil
from PIL import Image


def parse(data, invert=False):
    bitmap = "bitmap"
    pixels = tuple(data[bitmap]["data"].values())
    if invert:
        pixels = tuple(255 - p for p in pixels)
    width = data[bitmap]["width"]
    height = data[bitmap]["height"]

    return namedtuple("Glyph", [bitmap, "width", "height"])(pixels, width, height)


def create_grayscale_image(bitmap, filename):
    image = Image.new("L", (bitmap.width, bitmap.height))
    image.putdata(bitmap.bitmap)
    image.save(filename)
    return image


def split_jsons(content: str):
    for line in content.splitlines():
        start = -1
        end = -1
        count = 0
        for i, c in enumerate(line):
            if c == "{":
                count += 1
                if count == 1:
                    start = i
            elif c == "}":
                count -= 1
                if count == 0:
                    end = i
            if count == 0 and start != -1 and end != -1:
                yield line[start : end + 1]
                start = -1
                end = -1


class Pipeline:
    count = -1
    folder = Path("glyphs")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(exist_ok=True)

    def __init__(self, name):
        self.name = name
        (Pipeline.folder / name).mkdir(exist_ok=True)

    def process(self, glyphPath):
        read = Path(glyphPath).read_text(encoding="utf-8")

        texts = {}
        for split in split_jsons(read):
           
            try:
                parsed = json.loads(split)
            except json.JSONDecodeError:
                continue    

            match parsed['type']:    
                case 'glyph':   
                    parsed = parsed["glyph"]
                    bitmap = parse(parsed, True)
                    Pipeline.count += 1
                    create_grayscale_image(bitmap, Pipeline.folder / self.name  / f"{Pipeline.count}.png")  
                case 'geometry':    
                    parsed = parsed["data"]
                    keyInner = dict(parsed['tile'].items())
                    keyInner['text'] = parsed['text']
                    key= tuple(keyInner.items())
                    toAdd = parsed['geometry']
                    texts.setdefault(key, []).append(toAdd)

        print(texts)    
                


if __name__ == "__main__":
    pipeline = Pipeline('basemap')
    pipeline.process("basemap_glyphs.json")

    #pipeline2 = Pipeline('swiss')
    #pipeline2.process("swiss_glyphs.json")
