import pathlib
import json

from cache import *

FS = '.fs'

def dump_it(name, obj):
    path = pathlib.Path(pathlib.Path(__file__).parent, f'result_{name}_.json')
    with path.open(mode='w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)

working_dir = pathlib.Path("C:/Users/matze/OneDrive/bilder/_lightroom/2004-01-20")
def do_it(working_dir, caches : CacheGroup):
     def get_all_files(path : pathlib.Path, pattern):
        result = path.rglob(pattern, case_sensitive=False)
        result = list(map(str, result))

        return result
     
     return caches[FS].lookup(str(working_dir), toCall = lambda: get_all_files(working_dir, '*.*'))
     
with CacheGroup(FS) as caches:

    fs = dump_it('all_files', do_it(working_dir, caches))




