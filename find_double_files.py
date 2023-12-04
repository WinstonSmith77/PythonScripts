import pathlib
import json
import os

from cache import *

FS = '.fs'

def dump_it(name, obj):
    path = pathlib.Path(pathlib.Path(__file__).parent, f'result_{name}_.json')
    with path.open(mode='w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)

working_dir = pathlib.Path("C:/Users/matze/OneDrive/bilder/_lightroom/masters")
def get_length(file):
    stat = os.stat(file)
    return stat.st_size


def do_it(working_dir, caches : CacheGroup):
     def get_all_files(path : pathlib.Path, pattern):
        result = path.rglob(pattern, case_sensitive=False)
        result = filter(os.path.isfile, result)
        result = list(map(lambda x : (str(x), get_length(x)), result))

        return result
     
     return caches[FS].lookup(str(working_dir), toCall = lambda: get_all_files(working_dir, '*.*'))
     
with CacheGroup(FS) as caches:

    fs = dump_it('all_files', do_it(working_dir, caches))




