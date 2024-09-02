import itertools
import os
from pathlib import Path
from pprint import pprint
from itertools import groupby


def get_length(file):
    stat = os.stat(file)
    return stat.st_size


def get_all_files(paths: Path | list[Path], pattern, minLength=5 * 1024):
    if not isinstance(paths, (list, tuple)):
        paths = (paths,)
    results_sources = (
        Path(path).rglob(pattern, case_sensitive=False) for path in paths
    )
    results = (result for result in itertools.chain(*results_sources))
    results = filter(os.path.isfile, results)
    results = filter(
        lambda item: item[1] >= minLength,
        map(lambda x: (str(x), get_length(x)), results),
    )

    return results


path = r"C:\Users\henning\OneDrive\bilder"


round_to = 5 * 2 * 512 * 1024

all_length = list(
    length // round_to * round_to for _, length in get_all_files(path, "*.rw2")
)
# pprint(all_length)


all_length = sorted(all_length)
all_length = groupby(all_length)
all_length = {key: len(list(group)) for key, group in all_length}

import matplotlib.pyplot as plt

plt.bar([str(key) for key in all_length.keys()], all_length.values())
plt.xlabel('File Size')
plt.ylabel('Count')
plt.title('File Size Distribution')
plt.show()