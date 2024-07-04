from pathlib import Path
from pprint import pprint
from xmltodict import parse
from datetime import datetime
from dateutil import parser

from double_finder.cache import CacheGroup
from double_finder.find_double_files import get_all_files, dump_it


working_dir = Path(r"C:\Users\matze\OneDrive\bilder")
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
    return get_time_from_xmp(parse(Path(file).read_text(encoding="utf8")))


def files_with_time(fs):
    def are_there_other_files(path):
        stem = Path(path).stem
        for file, _ in fs:
            if stem in file and Path(file[0]).suffix.lower() != XMP:
                return True

    files = [path[0] for path in fs if Path(path[0]).suffix.lower() == XMP]

    files = [file for file in files if are_there_other_files(file)]

    files_with_time = ((file, get_time(file)) for file in files)
    files_with_time = [(file, time) for file, time in files_with_time if time]
    return files_with_time


def parse_time(time_str):
    try:
        return parser.parse(time_str)
    except ValueError:
        return None


def group(files_time, max_diff_seconds=10, min_length=3):
    group_and_start = None
    for file, time in files_time:
        if not group_and_start:
            group_and_start = ([file], time)
        else:
           group, start = group_and_start
           if (time - start).total_seconds() < max_diff_seconds:
                group.append(file)
                group_and_start = (group, time)
           else:
               len_group = len(group)
               if len_group >= min_length:
                   yield (len_group, group)
               group_and_start = ([file], time)         


        


DIR = "conseq_dir"
FILES_WITH_TIME = "files_with_time"

with CacheGroup(DIR, FILES_WITH_TIME) as caches:

    def get_fs():
        return caches[DIR].lookup(
            str(working_dir),
            callIfMissing=lambda: get_all_files(working_dir, "*.*", minLength),
        )

    files_time = caches[FILES_WITH_TIME].lookup(
        str(working_dir), callIfMissing=lambda: files_with_time(get_fs())
    )

    files_time = [
        (file, parse_time(time).replace(tzinfo=None)) for file, time in files_time
    ]
    files_time = sorted(files_time, key=lambda x: x[1])

    groups = list(group(files_time))

    dump_it("bursts", groups)

    pprint(groups)
