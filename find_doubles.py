from pathlib import Path

from timeit import default_timer as timer 
from double_finder import do_it
import json

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
all_doubles, group_length_without_doubles = do_it(working_dir)
dump_it('all_files', all_doubles)
dump_it('group_length_without_doubles', group_length_without_doubles)
end = timer()
print(end - start) # Time in seconds, e.g. 5.38091952400282

def contains_icloud(path : str):
    return 'icloud' in path

def any_map(filter, items):
    return any(map(filter, items))

def tail(items):
    _, *tail = items
    return tail 

# all_doubles_parts_to_remove = [k 
#                                for i in all_doubles 
                             
#                                 for k in tail(i[1])
#                                  ]

# pprint.pprint(all_doubles)

#pprint.pprint(all_doubles_parts_to_remove)


#move_files(all_doubles_parts_to_remove, working_dir, r"C:\Users\matze\Desktop\###old_files")