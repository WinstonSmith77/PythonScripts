import difflib
from pathlib import Path

a = 'C:\\Users\\matze\\OneDrive\\bilder\\icloud\\IMG_3439.HEIC'
b = 'C:\\Users\\matze\\OneDrive\\bilder\\_lightroom\\2020-06-29\\IMG_3439.HEIC'

n = difflib.SequenceMatcher(None, a,b).ratio()
print(n)


c = difflib.SequenceMatcher(None, Path(a).read_bytes(), Path(b).read_bytes()).get_matching_blocks()
print(c)


