from pathlib import Path
import json
import pprint
from timeit import default_timer as timer 

from double_finder import do_it
import send2trash


def dump_it(name, obj):
    path = Path(Path(__file__).parent, f'result_{name}_.json')
    with path.open(mode='w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)

def move_files(files, replacePath, withPath, dryRun = True):
    for file in files:
        newPath = Path(file.replace(str(replacePath), withPath))
        Path(newPath).parents[0].mkdir(parents=True, exist_ok=True)
        if dryRun:
            print(f'{file} -> {str(newPath)}')
        else:
            Path(file).rename(newPath)
        pass       


working_dir = Path(r"C:\Users\matze\OneDrive\bilder")

start = timer()
all_doubles = do_it(working_dir)
dump_it('all_files', all_doubles)
end = timer()
print(end - start) # Time in seconds, e.g. 5.38091952400282

def contains_icloud(path : str):
    return 'icloud' in path

def any_map(filter, items):
    return any(map(filter, items))

all_double_with_icloud = [i[1] for i in all_doubles if any_map(contains_icloud, i[1]) and any_map(lambda x: not contains_icloud(x), i[1] )]

dump_it('icloud', all_double_with_icloud)

all_double_with_icloud_in_icloud = [j for i in all_double_with_icloud for j in i if contains_icloud(j)]

all_double_with_icloud_in_icloud

pprint.pprint(all_double_with_icloud)
print(len(all_double_with_icloud_in_icloud))



move_files(all_double_with_icloud_in_icloud, working_dir, r"C:\Users\matze\Desktop\##old_files")