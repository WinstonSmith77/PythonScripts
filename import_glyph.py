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
    #image.remap_palette(range(255, 0, -1))
    image.putdata(bitmap.bitmap)
    image.save(filename)
    return image


def split_jsons(content: str):
    start = -1
    end = -1
    count = 0
    for i, c in enumerate(content):
        if c == "{":
            count += 1
            if count == 1:
                start = i
        elif c == "}":
            count -= 1
            if count == 0:
                end = i
        if count == 0 and start != -1 and end != -1:
            yield content[start : end + 1]
            start = -1
            end = -1


def do_it(index, jsonData):
    parsed = json.loads(jsonData)
    bitmap = parse(parsed, True)
    create_grayscale_image(bitmap, Path("glyphs", f"{index}.png"))


class Pipeline:
    count = 0
    folder = Path("glyphs")
    shutil.rmtree(folder) 
    folder.mkdir(exist_ok=True)

    @classmethod
    def process(cls, glyphPath):
        read = Path(glyphPath).read_text(encoding="utf-8")
        count = cls.count
        splits = tuple((split, count := count + 1) for split in  split_jsons(read))
        cls.count = count

        for jsonData, index in splits:
            do_it(count, jsonData)
           


pipeline = Pipeline()
pipeline.process("glyph.json")
