import itertools
import os
from pathlib import Path
from pprint import pprint

def get_length(file):
    stat = os.stat(file)
    return stat.st_size


def get_all_files(paths : Path | list[Path], pattern, minLength = 5 * 1024):
    if not isinstance(paths, (list, tuple)):
        paths = (paths,)
    results_sources = (Path(path).rglob(pattern, case_sensitive=False) for path in paths)
    results = (result for result in itertools.chain(*results_sources))
    results = filter(os.path.isfile, results)
    results = filter(lambda item : item[1] >= minLength, map(lambda x : (str(x), get_length(x)), results))

    return results


path = (r'C:\Users\matze\OneDrive\bilder')


all_length =  list(length for _, length in get_all_files(path, '*.rw2'))

min  = min(all_length)
max = max(all_length)

