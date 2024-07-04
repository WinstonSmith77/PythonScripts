from pathlib import Path
from pprint import pprint
from xmltodict import parse
from datetime import datetime
from dateutil import parser

from double_finder.cache import CacheGroup
from double_finder.find_double_files import get_all_files, dump_it


working_dir = Path(r"C:\Users\henning\OneDrive\bilder\_lightroom")
minLength = 1
XMP = ".xmp"


def get_time_from_xmp(doc):
    paths_to_time = (
        "x:xmpmeta",
        "rdf:RDF",
        "rdf:Description",
        "@exif:DateTimeOriginal",
    )
    for path in paths_to_time:
        doc = doc.get(path, None)
        if not doc:
            return None
    return doc


def get_time(file):
    return get_time_from_xmp(parse(Path(file).read_text()))


def files_with_time(fs):
    files = [path[0] for path in fs if Path(path[0]).suffix.lower() == XMP]

    files_with_time = ((file, get_time(file)) for file in files)
    files_with_time = [(file, time) for file, time in files_with_time if time]
    return files_with_time


def parse_time(time_str):
    try:
        return parser.parse(time_str)
    except ValueError:
        return None


DIR = "conseq_dir"
FILES_WITH_TIME = "files_with_time"

def group(files_time, max_diff_seconds=10, min_length=2):
    group = []
    last = None
    for file, time in files_time:
        if last is None:
            last = time
            group.append((file, str(time)))
        elif (time - last).total_seconds() < max_diff_seconds:
            group.append((file, str(time)))
            last = time
        else:
            if len(group) >= min_length:
                yield group
            group = []
            last = None   
           
           

with CacheGroup(DIR, FILES_WITH_TIME) as caches:

    def get_fs():
        return caches[DIR].lookup(
            str(working_dir),
            callIfMissing=lambda: get_all_files(working_dir, "*.*", minLength),
        )

    files_time = caches[FILES_WITH_TIME].lookup(
        str(working_dir), callIfMissing=lambda: files_with_time(get_fs())
    )

    files_time = [(file, parse_time(time).replace(tzinfo=None)) for file, time in files_time]
    files_time = sorted(files_time, key=lambda x: x[1])

    groups = list(group(files_time))

    dump_it('bursts', groups)
   
    
    
    pprint(groups)
