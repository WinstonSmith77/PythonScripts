import pathlib
import os
import pprint

import PIL.Image
import PIL.ExifTags
import PIL.TiffImagePlugin
import json
import base64
import xmltodict
import dateparser
import datetime
from cache import *

JPG = '.jpg'
PANA = '.rw2'
XMP = '.xmp'
ERROR = 'error'
FS = '.fs'

FILE = 'file'
LEN = 'length'
DATETIME = 'datetime'
EXIF = 'exif'
XML = 'XML'

def do_it(working_dir, caches: list[Cache]):
    def get_all_files(path, pattern):
        result = path.rglob(pattern, case_sensitive=False)
        result = list(map(str, result))

        return result

    def extract_exif_from_file(file):
        image = PIL.Image.open(file)
        exif_data = image.getexif()

        result = {}
        for k, v in exif_data.items():

            if isinstance(v, PIL.TiffImagePlugin.IFDRational):
                v = str(v)

            if isinstance(v, bytes):
                v = base64.standard_b64encode(v).decode()

            k = PIL.ExifTags.TAGS.get(k, None)
            if k is not None:
                result[k] = v
        return result

    def filter_exif(exif, *only):
        return {k: v for k, v in exif.items() if k in only or not only}

    def parse_exif_date(date : str):
        splits = date.split(' ')
        all_splits = splits[0].split(':') + splits[1].split(':')
        date = f'{all_splits[0]}-{all_splits[1]}-{all_splits[2]}T{all_splits[3]}:{all_splits[4]}:{all_splits[5]}'

        try:
            date_time = datetime.datetime.fromisoformat(date).isoformat()
        except ValueError:
            date_time = None

        return date_time       

    def handle_jpg(file, file_meta):
        filter = ['Make', 'Model', 'DateTime']
        # filter = []
        try:
            key = [extract_exif_from_file.__name__, file]
            exif = caches[JPG].lookup(*key, toCall=lambda: extract_exif_from_file(file))
            exif = filter_exif(exif, *filter)
        except PIL.UnidentifiedImageError:
            exif = caches[JPG].add_result(*key, value={ERROR: ERROR})

        key_time = 'DateTime'

        if key_time in exif:
            time_str :str = exif[key_time]
            file_meta[DATETIME]  = parse_exif_date(time_str)

        file_meta[DATETIME]  = exif
        return file_meta
    

    def find_in_xmp(xmp, path):
        item_pos = xmp
        for path_item in path[:-1]:
            if path_item in item_pos:
                item_pos = item_pos[path_item]
            else:
                item_pos = None
                break
                
        if  item_pos is not None:
            name = path[-1]  
            if name in item_pos:
                return item_pos[name]        


    def handle_xmp(file, file_meta):
        def parse_xmp(file):
            with pathlib.Path(file).open(mode='r', encoding='utf-8') as f:
                return xmltodict.parse(f.read())

        json = caches[XMP].lookup(parse_xmp.__name__, file, toCall=lambda: parse_xmp(file))

        path_to_date = ["x:xmpmeta", "rdf:RDF", "rdf:Description", '@exif:DateTimeOriginal']

        date_time_str =  find_in_xmp(json, path_to_date)       
        if  date_time_str is not None:    
            time = datetime.datetime.fromisoformat(date_time_str).isoformat()
            file_meta[DATETIME]  = time
        else:
            file_meta[XML]  = json


        return file_meta

    def merge_image_lists(*args):
        result = {}

        for image_list in args:
            for file in image_list:
                file_path = pathlib.Path(file)
                key = str(pathlib.Path(file_path.parent, file_path.stem.lower()))
                ext = file_path.suffix.lower()
                list_for_name = result.setdefault(key, {})
               
                stat = os.stat(file)

                file_meta = {LEN : stat.st_size}
                if ext == JPG:
                    file_meta = handle_jpg(file, file_meta)

                elif ext == XMP:
                    file_meta = handle_xmp(file, file_meta)

                list_for_name[ext] =  file_meta

        return result

    images = [caches[FS].lookup(get_all_files.__name__, ext, str(working_dir),
                                toCall=lambda: get_all_files(working_dir, f'*{ext}'))
              for ext in
              [JPG, PANA, XMP]]

    all_images = merge_image_lists(*images)
    return all_images

def find_triples(all_images):
      doubles = {key: value for key, value in all_images.items() if len(value) == 3}
      return doubles

def copy_time_from_xmp_to_rw2(all_images):

    result = {}

    for name, images in all_images.items():
        pana = images[PANA]
        xmp = images[XMP]

        if DATETIME in xmp:
            pana = dict(pana)
            pana[DATETIME] = xmp[DATETIME]
            images[PANA] = pana
        
        result[name] = images

    return result


working_dir = pathlib.Path("C:/Users/matze/OneDrive/bilder")
with  CacheGroup(JPG, XMP, FS) as caches:
    all_images = do_it(working_dir, caches)

triples = find_triples(all_images)
fixed_time_rw2 = copy_time_from_xmp_to_rw2(triples)

with  pathlib.Path(pathlib.Path(__file__).parent, 'result.json').open(mode='w', encoding='utf-8') as f:
    json.dump(fixed_time_rw2, f, indent=2)

# pprint.pprint(result)
