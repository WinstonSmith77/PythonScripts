import pathlib
import os
import pprint
import PIL


JPG = '.jpg'

working_dir = "C:/Users/matze/OneDrive/bilder"

path = pathlib.Path(working_dir)

def get_all_files(path, pattern):
    return  list(path.rglob(pattern, case_sensitive= False))

all_jpgs = get_all_files(path, f"*{JPG}")
all_raws = get_all_files(path, "*.rw2")


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
                    file_meta = (*file_meta,  exifdata)
                except PIL.UnidentifiedImageError:
                    pass

            list_for_ext.append(file_meta)
            

    return result

a = merge(all_jpgs, all_raws)

b = {key: value for key, value in a.items() if len(value) > 1}
pprint.pprint(b)





   
