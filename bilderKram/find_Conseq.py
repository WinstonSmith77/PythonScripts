from pathlib import Path
from double_finder.cache import CacheGroup


DIR = 'dir'
caches = CacheGroup(DIR)

working_dir = Path(r"C:\Users\matze\OneDrive\bilder")



fs = caches[DIR].lookup(str(working_dir), callIfMissing = lambda: get_all_files(working_dir, '*.*', minLength))