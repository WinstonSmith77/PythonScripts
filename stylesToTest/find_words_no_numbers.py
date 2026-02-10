from pathlib import Path
from collections import Counter
from pprint import pprint
import itertools 



def count_words(text : str):
    
    splits = text.split()
    return [word for word in splits if not any(ch.isdigit() for ch in word)]

parent = Path(__file__).parent
files = list(parent.rglob('*.json'))


words = list(itertools.chain.from_iterable(count_words(file.read_text(encoding='UTF8')) for file in files))


counter = {item: count for item, count in Counter(words).items() if count > 1}


pprint(counter)

