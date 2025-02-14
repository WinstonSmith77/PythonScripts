import itertools

crs = tuple(i for i in range(10))


def all_combinations():
    return itertools.product(crs, repeat=4)


def filter(combinations, min_number_of_different_digits):
    return (c for c in combinations if len(set(c)) >= min_number_of_different_digits)

def to_int(c):
    return c[0] * 1000 + c[1] * 100 + c[2] * 10 + c[3]

all = tuple(all_combinations())

filtered = tuple(filter(all, 4))

print(len(all), len(filtered)) 

map_daten = map(to_int, filtered) 

print(*map_daten)  # 5040 715
