import pathlib, pprint


working_dir = "C:/Users/matze/OneDrive/bilder"

path = pathlib.Path(working_dir)

all_jpgs =list(path.rglob("*.jpg", case_sensitive= False))

print(len(all_jpgs))
   
