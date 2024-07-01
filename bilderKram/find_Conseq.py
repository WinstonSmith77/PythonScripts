from pathlib import Path
from pprint import pprint
from xmltodict import parse

from double_finder.cache import CacheGroup
from double_finder.find_double_files import get_all_files



working_dir = Path(r"C:\Users\matze\OneDrive\bilder")
minLength = 1    
XMP = '.xmp'

def get_time_from_xmp(doc):
    paths_to_time = ('x:xmpmeta','rdf:RDF','rdf:Description','@exif:DateTimeOriginal')
    for path in paths_to_time:
        if path in doc:
            doc = doc[path]
        else:
            return None

    return doc        

def files_with_time(fs):
    files = [path[0] for path in fs if Path(path[0]).suffix.lower() == XMP]
   
    files_with_time = ((file, get_time_from_xmp(parse(Path(file).read_text())) )  for file in files)
    files_with_time = [(file, time) for file, time in files_with_time if time]
    return files_with_time


DIR = 'conseq_dir'
FILES_WITH_TIME = 'files_with_time'
with CacheGroup(DIR, FILES_WITH_TIME) as caches:
    fs = caches[DIR].lookup(str(working_dir), callIfMissing = lambda: get_all_files(working_dir, '*.*', minLength))
    files_with_time =  caches[FILES_WITH_TIME].lookup(str(working_dir), callIfMissing = lambda: files_with_time(fs))

    

  

   