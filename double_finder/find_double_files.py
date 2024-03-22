import hashlib
import itertools
from pathlib import Path
import json
import os
import difflib

from double_finder.cache import CacheGroup

DIR = '.directory'
HASH = '.hash'
FILEDIFF =  '.fileDiff'

def dump_it(name, obj):
    path = Path(Path(__file__).parent, f'result_{name}_.json')
    with path.open(mode='w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)

def get_hash_file(file):
     try:
        bytes = Path(file).read_bytes()
        md5_returned = hashlib.sha256(bytes).hexdigest()
        return md5_returned
     except FileNotFoundError:
        return None

def get_length(file):
    stat = os.stat(file)
    return stat.st_size

def get_all_files(path : Path, pattern, minLength = 5 * 1024):
    result = path.rglob(pattern, case_sensitive=False)
    result = filter(os.path.isfile, result)
    result = list(filter(lambda item : item[1] >= minLength, map(lambda x : (str(x), get_length(x)), result)))

    return result

def do_it(working_dir, minLength = 10 * 1024, caches : CacheGroup = None):
    
    def possible_doubles_from_groups(groups):
         result = {}
         for size, files in groups.items():
            group_result = []
            combinations = itertools.combinations(files, 2)
            for comb in combinations:
                a_file = Path(comb[0])
                b_file = Path(comb[1])

                ratio_name = caches[FILEDIFF].lookup(comb[0], comb[1], 'FileName' , callIfMissing= lambda : difflib.SequenceMatcher(None, a_file.name, b_file.name).ratio())
                quick_ratio_content = caches[FILEDIFF].lookup(comb[0], comb[1], 'Content' , callIfMissing= lambda : difflib.SequenceMatcher(None, a_file.read_bytes(), b_file.read_bytes()).real_quick_ratio())

                group_result.append((comb[0], comb[1], ratio_name, quick_ratio_content))
            result[size] = group_result
         return result       


    def doubles_from_groups(groups):
        new_result = {}
        for size, files in groups.items():
            inner_dict_size ={}
            new_result[size] = inner_dict_size
            combinations = itertools.combinations(files, 2)
            for comb in combinations:
                a_file = comb[0]
                b_file = comb[1]
                         
                a_hash = caches[HASH].lookup(a_file, callIfMissing= lambda: get_hash_file(a_file)) 
                b_hash = caches[HASH].lookup(b_file, callIfMissing= lambda: get_hash_file(b_file))   

                if a_hash is not None and b_hash is not None and a_hash == b_hash:
                    inner_set = inner_dict_size.setdefault(a_hash, set())
                    
                    inner_set.add(a_file)
                    inner_set.add(b_file)   

        new_result2 = {}

        for size, dict_hashes in new_result.items():
            list_for_hashes = []
            for items in dict_hashes.values():
                for item in items:
                    list_for_hashes.append(item)
            if list_for_hashes:
                new_result2[size] =  list_for_hashes   

        doubles = dict(sorted(new_result2.items(), key= lambda item : int(item[0]), reverse=True))

        return doubles
    
    def make_groups(all):
        groups = {}

        for file, length in all:

            items_for_length = groups.setdefault(length, [])
            items_for_length.append(file)

        groups = {key: items for key, items in groups.items() if len(items) > 1}   
        return groups 

    def find_doubles(all):

        groups = make_groups(all)

        doubles = doubles_from_groups(groups)

        for length, files in doubles.items():
            for double in files:
                groups[length].remove(double) 


        return (doubles, groups, possible_doubles_from_groups(groups))

    needsToDispose = False
    if caches is None:
        caches = CacheGroup(DIR, HASH, FILEDIFF)
        needsToDispose = True

    try: 
        fs = caches[DIR].lookup(str(working_dir), str(minLength), callIfMissing = lambda: get_all_files(working_dir, '*.*', minLength))
        caches.close_and_remove(DIR)
        doubles = find_doubles(fs)

        return doubles
    finally:
        if needsToDispose:
            caches.__exit__(None, None, None)
     


