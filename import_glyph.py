import json
import pathlib
from collections import namedtuple
import struct


read = json.loads(pathlib.Path('glyph.json').read_text(encoding='utf-8'))

def parse(data):
  
    pixels = tuple(data['bitmap']['data'].values())
    width = data['bitmap']['width']
    height = data['bitmap']['height']

    return namedtuple('Glyph', ['pixels', 'width', 'height'])(pixels, width, height)



def create_grayscale_bmp_file(bitmap, width, height, filename):
    # Calculate the size of the image data
    image_size = width * height

    # Create the BMP file header
    file_header = struct.pack('<2sIHHI', b'BM', 54 + image_size, 0, 0, 54)

    # Create the BMP info header
    info_header = struct.pack('<IIIHHIIIIII', 40, width, height, 1, 8, 0, image_size, 0, 0, 0, 0)

    # Create the grayscale pixel data
    pixel_data = bytes(bitmap)

    # Write the BMP file
    with open(filename, 'wb') as file:
        file.write(file_header)
        file.write(info_header)
        file.write(pixel_data)

    print(filename)

bitmap = parse(read)

print(bitmap)
print('a')




# Usage example
create_grayscale_bmp_file(bitmap.pixels, bitmap.width, bitmap.height, 'grayscale.bmp')