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
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(exist_ok=True)

    def __init__(self, name):
        self.name = name
        (Pipeline.folder / name).mkdir(exist_ok=True)

    def process(self, glyphPath):
        read = Path(glyphPath).read_text(encoding="utf-8")

        for split in split_jsons(read):
            parsed = json.loads(split)
            bitmap = parse(parsed, True)
            Pipeline.count += 1
            create_grayscale_image(bitmap, Pipeline.folder / self.name  / f"{Pipeline.count}.png")


if __name__ == "__main__":
    pipeline = Pipeline('basemap')
    pipeline.process("glyph.json")
