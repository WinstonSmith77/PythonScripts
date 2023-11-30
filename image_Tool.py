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

hash_jpgs = {file.parts[-1]:file for file in all_jpgs}
hash_raws = {file.parts[-1]:file for file in all_raws}




print(hash_jpgs, hash_raws)
   
