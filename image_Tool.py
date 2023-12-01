import pathlib
import os
import pprint


working_dir = "C:/Users/matze/OneDrive/bilder"

path = pathlib.Path(working_dir)

def get_all_files(path, pattern):
    return  list(path.rglob(pattern, case_sensitive= False))

all_jpgs = get_all_files(path, "*.jpg")
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
            list_for_ext.append((file, stat.st_size))
            

    return result

a = merge(all_jpgs, all_raws)

b = {key: value for key, value in a.items() if len(value) > 1}
pprint.pprint(b)





   
