import pathlib, pprint


working_dir = "C:/Users/matze/OneDrive/bilder"

path = pathlib.Path(working_dir)

def get_all_files(path, pattern):
    return  list(path.rglob(pattern, case_sensitive= False))

all_jpgs = get_all_files(path, "*.jpg")
all_raws = get_all_files(path, "*.rw2")

print(all_jpgs[0].parts[-1])

print(all_raws[0].parts[-1])

print(len(all_jpgs), len(all_raws))



def merge(*args):
    result = {}

    for image_list in args:
        for file in image_list:
            key = file.parts[-1]
            *_, ext = key.split('.')
            ext = ext.lower()
            list_for_name = result.setdefault(key, {})
            list_for_ext = list_for_name.setdefault(ext, [])
            list_for_ext.append(file)
            

    return result

a = merge(all_jpgs, all_raws)

b = {key: value for key, value in a.items() if len(value) > 1}
pprint.pprint(b)





   
