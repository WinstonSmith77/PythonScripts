import hashlib
import itertools
import pathlib
import json
import os


from double_finder.cache import *

def do_it(working_dir, minLength, caches : CacheGroup = None):
    def get_length(file):
        stat = os.stat(file)
        return stat.st_size


    def get_all_files(path : pathlib.Path, pattern, minLength = 5 * 1024):
        result = path.rglob(pattern, case_sensitive=False)
        result = filter(os.path.isfile, result)
        result = list(filter(lambda item : item[1] >= minLength, map(lambda x : (str(x), get_length(x)), result)))

        return result
    
    def get_hash_file(file):
        try:
            bytes = pathlib.Path(file).read_bytes()
            md5_returned = hashlib.sha256(bytes).hexdigest()
            return md5_returned
        except FileNotFoundError:
            return None

    def find_doubles(all):

        results = {}

        for file, length in all:

            items_for_length = results.setdefault(length, [])
            items_for_length.append(file)

        results = {key: items for key, items in results.items() if len(items) > 1}       

        new_result = {}
        for size, files in results.items():
            inner_dict_size ={}
            new_result[size] = inner_dict_size
            combinations = itertools.combinations(files, 2)
            for comb in combinations:
                a_file = comb[0]
                b_file = comb[1]
                         
                a_hash = caches[HASH].lookup(a_file, toCall= lambda: get_hash_file(a_file)) 
                b_hash = caches[HASH].lookup(b_file, toCall= lambda: get_hash_file(b_file))   

                if a_hash is not None and b_hash is not None and a_hash == b_hash:
                    inner_set = inner_dict_size.setdefault(a_hash, set())
                    
                    inner_set.add(a_file)
                    inner_set.add(b_file)   

        new_result2 = {}

        for size, dict_hashes in new_result.items():
            list_for_hashes = []
            for items in dict_hashes.values():
                if items:
                    list_for_hashes.append(list(items))
            if list_for_hashes:
                new_result2[size] =  list_for_hashes   


        return sorted(new_result2.items(), key= lambda item : int(item[0]), reverse=True)

    needsToDispose = False
    if caches is None:
        caches = CacheGroup(FS, HASH)
        needsToDispose = True

    try: 
        fs = caches[FS].lookup(str(working_dir), str(minLength), toCall = lambda: get_all_files(working_dir, '*.*', minLength))
        caches.close_and_remove(FS)
        doubles = find_doubles(fs)

        return doubles
    finally:
        if needsToDispose:
            caches.__exit__(None, None, None)
     


