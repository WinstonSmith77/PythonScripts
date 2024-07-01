from pathlib import Path
from pprint import pprint
from xmltodict import parse

from double_finder.cache import CacheGroup
from double_finder.find_double_files import get_all_files



working_dir = Path(r"C:\Users\matze\OneDrive\bilder")
minLength = 1    
XMP = '.xmp'


DIR = 'conseq_dir'
with CacheGroup(DIR) as caches:
    fs = caches[DIR].lookup(str(working_dir), callIfMissing = lambda: get_all_files(working_dir, '*.*', minLength))
    files = [path[0] for path in fs if Path(path[0]).suffix.lower() == XMP]
    #pprint(fs)

    

    xmp = parse(Path(files[5689]).read_text())

    pprint(xmp['x:xmpmeta']['rdf:RDF']['rdf:Description']['@exif:DateTimeOriginal'])