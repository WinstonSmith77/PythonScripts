import pathlib
import os
import pprint
import itertools
import hashlib

import PIL.Image
import PIL.ExifTags
import PIL.TiffImagePlugin
import json
import base64
import xmltodict
import datetime
from cache import *

JPG = '.jpg'
PANA = '.rw2'
XMP = '.xmp'
ERROR = 'error'
FS = '.fs'

FILE = 'file'
LEN = 'length'
DATETIME = 'DateTime'
EXIF = 'exif'
XML = 'XML'
MAKE = 'Make'
MODEL= 'Model'
HASH = 'hash'

def do_it(working_dir, caches: CacheGroup):
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
        filter = [MAKE, MODEL, DATETIME]
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
            parsed_time = parse_exif_date(time_str)
            if parsed_time is not None:
                file_meta[DATETIME] = parsed_time

        file_meta[EXIF]  = exif
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

        path_to =  ["x:xmpmeta", "rdf:RDF", "rdf:Description"]
      
        path_to_date = [*path_to, '@exif:DateTimeOriginal']
        path_to_make = [*path_to, f"@tiff:{MAKE}"]
        path_to_model = [*path_to, f"@tiff:{MODEL}"]

        date_time_str =  find_in_xmp(json, path_to_date)       
        if  date_time_str is not None:    
            time = datetime.datetime.fromisoformat(date_time_str).isoformat()
            file_meta[DATETIME]  = time
        else:
            file_meta[XML]  = json

        paths_to_add = [(MAKE, path_to_make), (MODEL, path_to_model)]

        for path_to_add in paths_to_add:
            data = find_in_xmp(json, path_to_add[1])
            if data is not None:
                file_meta[path_to_add[0]] = data

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

def find_triples(all):
      doubles = {key: value for key, value in all.items() if len(value) == 3}
      return doubles

def copy_time_from_xmp_to_rw2(all):
    result = {}

    for name, images in all.items():
        if{XMP, PANA} <= images.keys():
            pana = images[PANA]
            xmp = images[XMP]
            del images[XMP]

            fields_to_copy = [DATETIME, MAKE, MODEL]
            for field_to_copy in fields_to_copy: 
                if field_to_copy in xmp:
                    pana[field_to_copy] = xmp[field_to_copy]
            
        result[name] = images

    return result


def find_doubles_raw_jpeg_by_time(all):
    result = {}

    for name, images in all.items():
        if {PANA, JPG} <= images.keys():
            pana = images[PANA]
            jpg = images[JPG]

            pana_time = datetime.datetime.fromisoformat(pana[DATETIME])
            jpg_time = datetime.datetime.fromisoformat(jpg[DATETIME])

            diff = pana_time - jpg_time
            if abs(diff.total_seconds()) > 1:
                continue

            result[name] = images

    return result

def find_files_to_delete(all):
    result = []

    for name in all:
        result.append(name + JPG)

    return result

def find_files_to_delete2(all):
    result = []

    path_for_old_files = pathlib.Path(pathlib.Path(__file__).parent, '#old_files').parts

    for value in all.values():
       for item in value:
           file = item[0]
           if 'icloud' in file:
               path_to_move_to = pathlib.Path(file)
               parts = list(path_to_move_to.parts)
               parts[0:1] = path_for_old_files 
               result.append((file, str(pathlib.Path(*parts))))

    return result

def get_group_by_size(all, caches : CacheGroup):
    
    def get_md5_file(file):
        bytes = pathlib.Path(file).read_bytes()
        md5_returned = hashlib.sha256(bytes).hexdigest()
        return md5_returned
    
    result = {}

    for name, images in all.items():
       for ext, file in images.items():
           if ext == XMP:
               continue
           size = file[LEN]
           list_len = result.setdefault(size, [])
           list_len.append((name + ext, file))

    result = {size : images for size, images in result.items() if len(images) > 1}      

    new_result = {}
    for size, images in result.items():
       
        combinations = itertools.combinations(images, 2)
        for comb in combinations:

            meta = comb[0][1]
            meta2 =  comb[1][1]

            if DATETIME in meta and DATETIME in meta2:

                diff = abs(datetime.datetime.fromisoformat(meta[DATETIME]) -  datetime.datetime.fromisoformat(meta2[DATETIME]))
                if diff.total_seconds() < 1:

                    a_file = comb[0][0]
                    b_file = comb[1][0]
                    a_hash = caches[HASH].lookup(a_file, toCall= lambda: get_md5_file(a_file)) 
                    b_hash = caches[HASH].lookup(b_file, toCall= lambda: get_md5_file(b_file))   

                    if a_hash == b_hash:
                        inner_dict = new_result.setdefault(size, {})
                        inner_dict[comb[0][0]] = comb[0][1]
                        inner_dict[comb[1][0]] = comb[1][1]

    return new_result

def dump_it(name, obj):
    path = pathlib.Path(pathlib.Path(__file__).parent, f'result_{name}_.json')
    with path.open(mode='w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)

working_dir = pathlib.Path("C:/Users/matze/OneDrive/bilder")
with  CacheGroup(JPG, XMP, FS, HASH) as caches:
    all_images = do_it(working_dir, caches)

    #triples = find_triples(all_images)
    fixed_time_rw2 = copy_time_from_xmp_to_rw2(all_images)
    #doubles_by_time = find_doubles_raw_jpeg_by_time(fixed_time_rw2)
    #files_to_delete = find_files_to_delete(doubles_by_time)
    group_by_size = get_group_by_size(fixed_time_rw2, caches)
    #files_to_delete2 = find_files_to_delete2(group_by_size)

dump_it('all_images', all_images)
#dump_it("doubles", doubles_by_time)
#dump_it("to delete", files_to_delete2)
dump_it("fixed_time_rw2", fixed_time_rw2)
dump_it("group_by_size", group_by_size)

# for file in files_to_delete2:
#     source = pathlib.Path(file[0])
#     dest =  pathlib.Path(file[1])
    
#     dest.parent.mkdir(parents=True, exist_ok=True)
    
#     source.rename(dest)

# pprint.pprint(result)
