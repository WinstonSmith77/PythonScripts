from pathlib import Path
from pprint import pprint

from double_finder.cache import CacheGroup
from double_finder.find_double_files import get_all_files



working_dir = Path(r"C:\Users\matze\OneDrive\bilder")
minLength = 1    
XMP = '.xmp'


DIR = 'conseq_dir'
with CacheGroup(DIR) as caches:
    fs = caches[DIR].lookup(str(working_dir), callIfMissing = lambda: get_all_files(working_dir, '*.*', minLength))
    fs = [path[0] for path in fs if Path(path[0]).suffix.lower() == XMP]
    pprint(fs)