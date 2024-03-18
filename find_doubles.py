import pathlib
import json
import pprint
from timeit import default_timer as timer 

from double_finder import do_it
import send2trash



def dump_it(name, obj):
    path = pathlib.Path(pathlib.Path(__file__).parent, f'result_{name}_.json')
    with path.open(mode='w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)


working_dir = pathlib.Path(r"C:\Users\matze\OneDrive\bilder")

start = timer()
all_doubles = do_it(working_dir)
dump_it('all_files', all_doubles)
end = timer()
print(end - start) # Time in seconds, e.g. 5.38091952400282

def contains_icloud(path : str):
    return 'icloud' in path

def any_map(filter, items):
    return any(map(filter, items))

all_double_jpgs = [i[1] for i in all_doubles if any_map(contains_icloud, i[1]) and any_map(lambda x: not contains_icloud(x), i[1] ) and all(map(lambda f : f.lower().endswith('.jpg'), i[1]))]
all_double_jpgs_in_icloud = [[j for j in i if contains_icloud(j)] for i in all_double_jpgs]

pprint.pprint(all_double_jpgs_in_icloud)
print(len(all_double_jpgs_in_icloud))

for i in all_double_jpgs_in_icloud:
    for j in i:
       print(j)