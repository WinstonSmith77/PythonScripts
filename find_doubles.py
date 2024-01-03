import pathlib
import json
from timeit import default_timer as timer 

from double_finder import do_it



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


