import hashlib
import itertools
import pathlib
import json
import os

from cache import *

FS = '.fs'
HASH = '.hash'

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
    
    def get_sha_file(file):
        bytes = pathlib.Path(file).read_bytes()
        md5_returned = hashlib.sha256(bytes).hexdigest()
        return md5_returned

    def find_doubles(all):

        results = {}

        for file, length in all:

            items_for_length = results.setdefault(length, [])
            items_for_length.append(file)

        results = {key: items for key, items in results.items() if len(items) > 1}       

        new_result = {}
        for size, files in results.items():
       
            combinations = itertools.combinations(files, 2)
            for comb in combinations:
                a_file = comb[0]
                b_file = comb[1]
                         
                a_hash = caches[HASH].lookup(a_file, toCall= lambda: get_sha_file(a_file)) 
                b_hash = caches[HASH].lookup(b_file, toCall= lambda: get_sha_file(b_file))   

                if a_hash == b_hash:
                    inner_set = new_result.setdefault(size, set())
                    inner_set.add(a_file)
                    inner_set.add(b_file)   

        new_result = {key: list(items) for key, items in new_result.items()}               

        return new_result 

     
    fs = caches[FS].lookup(str(working_dir), toCall = lambda: get_all_files(working_dir, '*.*'))
    doubles = find_doubles(fs)

    return doubles
     
with CacheGroup(FS, HASH) as caches:
    all_doubles = do_it(working_dir, caches)
dump_it('all_files', all_doubles)



