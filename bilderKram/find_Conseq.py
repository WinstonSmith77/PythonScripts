from pathlib import Path
from pprint import pprint
from xmltodict import parse
from datetime import datetime
from itertools import chain, groupby

import PIL.Image
import PIL.ExifTags
import PIL.TiffImagePlugin
import base64

from double_finder.cache import CacheGroup
from double_finder.find_double_files import get_all_files, dump_it

root = Path('/Volumes/Matze/matze/Library/CloudStorage/OneDrive-Personal')

working_dirs = (Path(root, "bilder", "_lightroom")
                #, Path(root, "#emmaTaufe")
                )
minLength = 1
XMP = ".xmp"
JPG = ".jpg"
DATETIME = "DateTime"

DIR = "conseq_files"
FILES_WITH_TIME_XMP = "files_with_time_xmp"
FILES_WITH_TIME_JPG = "files_with_time_jpg"

def filter_date(date: datetime):
    return True


def get_time_from_xmp_file(file):
    doc = parse(Path(file).read_text(encoding="utf8"))
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


def xmp_files_with_time_and_image(fs):
    stem_with_suffix = {}

    for file, _ in fs:
        path = Path(file)
        stem = str(Path(path.parent, path.stem))
        suffix = path.suffix.lower()

        list_suffixes = stem_with_suffix.setdefault(stem, [])
        list_suffixes.append(suffix)

        if len(list_suffixes) > 1 and XMP in list_suffixes:
            del stem_with_suffix[stem]
            file = stem + XMP
            time = get_time_from_xmp_file(file)
            if time:
                yield (file, time)


def parse_time(time_str: str):
    DATE_TIME_FORMATS = (
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y:%m:%d %H:%M:%S",
    )

    time_str = time_str.split("+")[0]
    for format in DATE_TIME_FORMATS:
        try:
            return datetime.strptime(time_str, format)
        except ValueError:
            pass

    return None


def extract_exif_from_file(file):
    image = PIL.Image.open(file)
    exif_data = image.getexif()

    result = {}
    for k, v in exif_data.items():
        if isinstance(v, PIL.TiffImagePlugin.IFDRational):
            v = str(v)

        if isinstance(v, bytes):
            v = base64.standard_b64encode(v).decode()

        k = PIL.ExifTags.TAGS.get(k, None)
        if k is not None:
            result[k] = v
    return result


def jpg_files_with_time_and_image(fs):
    files = (file[0] for file in fs if Path(file[0]).suffix.lower() == JPG)

    for file in files:
        exif = extract_exif_from_file(file)
        yield (file, exif)

def group_by_time(files_time, max_diff_seconds=10, min_length=3):
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
                    yield (len_group, group, str(start))
                group_and_start = ([file], time)

with CacheGroup(DIR, FILES_WITH_TIME_XMP, FILES_WITH_TIME_JPG) as caches:
    cache_entry = str(working_dirs)
    fs_in_cache = caches[DIR].is_in_cache(cache_entry)
    if not fs_in_cache:
        caches[FILES_WITH_TIME_XMP].purge()
        caches[FILES_WITH_TIME_JPG].purge()

    fs = caches[DIR].lookup(
        cache_entry,
        callIfMissing=lambda: list(get_all_files(working_dirs, "*.*", minLength)),
    )

    files_time_xmp = caches[FILES_WITH_TIME_XMP].lookup(
        cache_entry, callIfMissing=lambda: list(xmp_files_with_time_and_image(fs))
    )

    files_time_jpg = caches[FILES_WITH_TIME_JPG].lookup(
        cache_entry, callIfMissing=lambda: list(jpg_files_with_time_and_image(fs))
    )

files_time_jpg = (
    (file, parse_time(exif[DATETIME]))
    for file, exif in files_time_jpg
    if DATETIME in exif
)

files_time_jpg = ((file, time) for file, time in files_time_jpg if time)

files_time_xmp = (
    (file, parse_time(time).replace(tzinfo=None)) for file, time in files_time_xmp
)


files_time = sorted(filter(lambda x: filter_date(x[1]),  chain(files_time_xmp, files_time_jpg)), key=lambda x: x[1])


#pprint(files_time[5])

groups = sorted(list(group_by_time(files_time)), key=lambda x: x[0], reverse=True)
#pprint(groups[0])

groups = groupby(groups, key=lambda x: x[0])
groups = list(
    (key, list(((entry[1], entry[2]) for entry in entries))) for key, entries in groups
)


dump_it("bursts", groups)

#pprint(groups)
