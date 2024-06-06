import json
from pathlib import Path
from collections import namedtuple
import shutil
from PIL import Image
from multiprocessing.pool import Pool
from pprint import pprint


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
    # image.remap_palette(range(255, 0, -1))
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


def do_it(input):
    parsed = json.loads(input[0])
    bitmap = parse(parsed, True)
    create_grayscale_image(bitmap, Path("glyphs", f"{input[1]}.png"))


class Pipeline:
    count = -1
    folder = Path("glyphs")

    @classmethod
    def process(cls, glyphPath):
        read = Path(glyphPath).read_text(encoding="utf-8")
        count = cls.count
        splits = tuple((split, count := count + 1) for split in split_jsons(read))
        cls.count = count

        # for split in splits:
        #     do_it(split)

        with Pool() as pool:
            pool.map(do_it, splits)

if __name__ == "__main__":
    shutil.rmtree(Pipeline.folder)
    Pipeline.folder.mkdir(exist_ok=True)

    pipeline = Pipeline()
    pipeline.process("glyph.json")
