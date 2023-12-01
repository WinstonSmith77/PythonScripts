import pathlib
import os
import pprint
import PIL.Image
import PIL.ExifTags

JPG = '.jpg'
PANA = '.rw2'

working_dir = "C:/Users/matze/OneDrive/bilder"

path = pathlib.Path(working_dir)

def get_all_files(path, pattern):
    return  list(path.rglob(pattern, case_sensitive= False))

images = [get_all_files(path, f"*{ext}") for ext in [JPG, PANA]]

def extract_from_exif(exifdata, *only):
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
                    image = PIL.Image.open(file)
                    exifdata = image.getexif()
                    file_meta = (*file_meta, extract_from_exif(exifdata, 'Make', 'Model'))
                except PIL.UnidentifiedImageError:
                    pass

            list_for_ext.append(file_meta)
            

    return result

all = merge(*images)
doubles = {key: value for key, value in all.items() if len(value) > 1}

pprint.pprint(doubles)





   
