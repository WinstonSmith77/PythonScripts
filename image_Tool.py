import pathlib
import os
import pprint

import PIL.Image
import PIL.ExifTags
import PIL.TiffImagePlugin
import json
import base64
import xmltodict


class PassThroughCache:
    def __init__(self, name) -> None:
        pass

    def Lookup(self, key, toCall):
        return toCall()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass


class Cache:
    def __init__(self, name) -> None:
        self._path = pathlib.Path(pathlib.Path(__file__).parent, f'{name}.cache.json')

        if self._path.exists():
            try:
                with self._path.open(mode='r', encoding='utf-8') as f:
                    self._innerCache = json.load(f)
                return
            except:
                pass

        self._innerCache = {}

    def AddResult(self, *key_parts, value):
        key = self._make_key(*key_parts)
        self._innerCache[key] = value
        self._isDirty = True
        return value

    def _make_key(self, *key_parts):
        return  ",".join(key_parts)   

    def Lookup(self, *key_parts, toCall):
        key = self._make_key(*key_parts)

        if key in self._innerCache:
            return self._innerCache[key]
        else:
            new_entry = toCall()
            self._innerCache[key] = new_entry
            self._isDirty = True  
            return new_entry

    def __enter__(self):
        self._isDirty = False
        return self

    def __exit__(self, type, value, tb):
        if self._isDirty:
            with self._path.open(mode='w', encoding='utf-8') as f:
                json.dump(self._innerCache, f, indent=2)

JPG = '.jpg'
PANA = '.rw2'
XMP = '.xmp'
ERROR = 'error'
FS = '.fs'


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

    def handle_jpg(file, file_meta):
        filter = ['Make', 'Model', 'DateTime']
        # filter = []
        try:
            key = [extract_exif_from_file.__name__, file]
            exif = caches[JPG].Lookup(*key, toCall=lambda: extract_exif_from_file(file))
            exif = filter_exif(exif, *filter)
        except PIL.UnidentifiedImageError:
            exif = caches[JPG].AddResult(*key, value= {ERROR: ERROR})

        return (*file_meta, exif)

    def handle_xmp(file, file_meta):
        def parse_xmp(file):
            with pathlib.Path(file).open(mode='r', encoding='utf-8') as f:
                return xmltodict.parse(f.read())
            
        json =  caches[XMP].Lookup(parse_xmp.__name__, file, toCall=lambda: parse_xmp(file)) 
        return (*file_meta, json)

    def merge(*args):
        result = {}

        for image_list in args:
            for file in image_list:
                file_path = pathlib.Path(file)
                name = file_path.stem.lower()
                ext = file_path.suffix.lower()
                list_for_name = result.setdefault(name, {})
                list_for_ext = list_for_name.setdefault(ext, [])
                stat = os.stat(file)

                file_meta = (file, stat.st_size)
                if ext == JPG:
                    file_meta = handle_jpg(file, file_meta)

                elif ext == XMP:
                    file_meta = handle_xmp(file, file_meta)

                list_for_ext.append(file_meta)

        return result

    images = [caches[FS].Lookup(get_all_files.__name__, ext, str(working_dir), toCall=lambda: get_all_files(working_dir, f'*{ext}'))
              for ext in
              [JPG, PANA, XMP]]

    all_images = merge(*images)
    doubles = {key: value for key, value in all_images.items() if len(value) > 2}

    return doubles




working_dir = pathlib.Path("C:/Users/matze/OneDrive/bilder")
with  Cache(JPG) as jpg_cache:
    with  Cache(FS) as fs_cache:
        with  Cache(XMP) as xmp_cache:
            caches = {
                JPG : jpg_cache,
                FS : fs_cache,
                XMP : xmp_cache 
                }
            result = do_it(working_dir,caches)

with  pathlib.Path(pathlib.Path(__file__).parent, 'result.json').open(mode='w', encoding='utf-8') as f:
    json.dump(result, f, indent=2)

# pprint.pprint(result)
