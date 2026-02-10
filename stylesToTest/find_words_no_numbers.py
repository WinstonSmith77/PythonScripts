from pathlib import Path
from collections import Counter
from pprint import pprint
import itertools


TRANSLATION_TABLE = str.maketrans({
    '"': None,
    "'": None,
    " ": None,
    ",": " ",
    ":": " ",
    "[": " [ ",
    "]": " ] ",
    "{": " { ",
    "}": " } ",
})


def count_words(text: str):
    text = text.translate(TRANSLATION_TABLE)

    splits = text.split()
    return (word for word in splits if not any(ch.isdigit() for ch in word))

parent = Path(__file__).parent
files = list(parent.rglob('*.json'))


words = itertools.chain.from_iterable(count_words(file.read_text(encoding='UTF8')) for file in files)


counter = sorted(  {item: count for item, count in Counter(words).items() if count > 250}.items(), key= lambda x : x[1] )


print(counter)

