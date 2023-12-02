import pathlib
import os
import pprint
import PIL.Image
import PIL.ExifTags


class Cache:
    def __init__(self) -> None:
        pass
    
    def Lookup(self, params, toCall):
        return toCall()    

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.stream.close()

def do_it(working_dir, cache: Cache):

    JPG = '.jpg'
    PANA = '.rw2'
    
    def get_all_files(path, pattern):
        return  list(path.rglob(pattern, case_sensitive= False))

    def extract_exif_from_file(file, *only):
        image = PIL.Image.open(file)
        exifdata = image.getexif()

        result = {}
        for k,v in exifdata.items():
            k = PIL.ExifTags.TAGS.get(k, None)
            if k is not None and k in only:
                result[k] = v
        return result

    def merge(*args):
        result = {}

        for image_list in args:
            for file in image_list:
                name = file.stem.lower()
                ext = file.suffix.lower()
                list_for_name = result.setdefault(name, {})
                list_for_ext = list_for_name.setdefault(ext, [])
                stat = os.stat(file)

                file_meta =  (file, stat.st_size)
                if ext == JPG:
                    
                    try:
                        file_meta = (*file_meta, cache.Lookup(None, lambda : extract_exif_from_file(file, 'Make', 'Model')))
                    except PIL.UnidentifiedImageError:
                        pass

                list_for_ext.append(file_meta)

        return result


    images = [cache.Lookup(None, lambda : get_all_files(working_dir, f"*{ext}")) for ext in [JPG, PANA]]

    all = merge(*images)
    doubles = {key: value for key, value in all.items() if len(value) > 1}

    return doubles

working_dir = pathlib.Path("C:/Users/matze/OneDrive/bilder")
cache = Cache()
result = do_it(working_dir, cache)

pprint.pprint(result)





   
