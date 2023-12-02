import pathlib
import os
import pprint
import PIL.Image
import PIL.ExifTags
import json


class Cache:
    def __init__(self, name,*, ignore = False) -> None:
        self._ignore = ignore
        self._path = pathlib.Path(pathlib.Path(__file__).parent, f'{name}.cache.json')

        if ignore:
            return

        if self._path.exists():
            try:
                with self._path.open(mode='r', encoding='utf-8') as f:
                 self._innerCache = json.load(f)
                return 
            except:
                pass

        self._innerCache = {}
       

    def Lookup(self, params, toCall):
        if self._ignore:
            return toCall()
        
        if params in self._innerCache:
            return self._innerCache[params]
        else:
            new_entry = toCall()
            self._innerCache[params] = new_entry
            return new_entry

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        if not self._ignore:
            with self._path.open(mode='w', encoding='utf-8') as f:
                json.dump(self._innerCache, f, indent=2)
         
def do_it(working_dir, cache: Cache):
    JPG = '.jpg'
    PANA = '.rw2'

    def get_all_files(path, pattern):
        result = path.rglob(pattern, case_sensitive=False)
        result = list(map(str, result))

        return result

    def extract_exif_from_file(file, *only):
        image = PIL.Image.open(file)
        exif_data = image.getexif()

        result = {}
        for k, v in exif_data.items():
            k = PIL.ExifTags.TAGS.get(k, None)
            if k is not None and k in only:
                result[k] = v
        return result

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

                    try:
                        file_meta = (
                        *file_meta, cache.Lookup(file, lambda: extract_exif_from_file(file, 'Make', 'Model')))
                    except PIL.UnidentifiedImageError:
                        pass

                list_for_ext.append(file_meta)

        return result

    images = [cache.Lookup(ext, lambda: get_all_files(working_dir, f'*{ext}')) for ext in [JPG, PANA]]

    all_images = merge(*images)
    doubles = {key: value for key, value in all_images.items() if len(value) > 1}

    return doubles


working_dir = pathlib.Path("C:/Users/matze/OneDrive/bilder")
with  Cache('first', ignore=False) as cache:
    result = do_it(working_dir, cache)
pprint.pprint(result)
