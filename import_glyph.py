import functools
import json
from pathlib import Path
from collections import namedtuple
import shutil
import time
from PIL import Image

from pprint import pprint


def benchmark(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        stop_time = time.time()
        delta = stop_time - start_time
        pprint(f"{f.__name__} Delta {delta}")
        return result

    return wrapper


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


class Pipeline:
    count = -1
    folder = Path("glyphs")

    @classmethod
    @benchmark
    def process(cls, glyphPath):
        read = Path(glyphPath).read_text(encoding="utf-8")

        for split in split_jsons(read):
            parsed = json.loads(split)
            bitmap = parse(parsed, True)
            cls.count += 1
            create_grayscale_image(bitmap, cls.folder / f"{cls.count}.png")


if __name__ == "__main__":
    shutil.rmtree(Pipeline.folder)
    Pipeline.folder.mkdir(exist_ok=True)

    pipeline = Pipeline()
    pipeline.process("glyph.json")
