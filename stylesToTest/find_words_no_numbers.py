from pathlib import Path
from collections import Counter
from pprint import pprint

parent = Path(__file__).parent
files = list(parent.rglob('*.json'))

first = files[0]

print(first)



