from pprint import pprint

zoo_animals = [
    "Lion",
    "Tiger",
    "Elephant",
    "Giraffe",
    "Zebra",
    "Panda",
    "Kangaroo",
    "Koala",
    "Penguin",
    "Flamingo",
    "Hippopotamus",
    "Rhinoceros",
    "Cheetah",
    "Leopard",
    "Gorilla",
    "Chimpanzee",
    "Orangutan",
    "Baboon",
    "Meerkat",
    "Lemur",
    "Sloth",
    "Armadillo",
    "Anteater",
    "Otter",
    "Beaver",
    "Wolf",
    "Fox",
    "Bear",
    "Polar Bear",
    "Grizzly Bear",
    "Moose",
    "Deer",
    "Bison",
    "Buffalo",
    "Camel",
    "Llama",
    "Alpaca",
    "Yak",
    "Reindeer",
    "Elk",
    "Ostrich",
    "Emu",
    "Peacock",
    "Parrot",
    "Macaw",
    "Toucan",
    "Eagle",
    "Hawk",
    "Falcon",
    "Owl",
    "Crocodile",
    "Alligator",
    "Turtle",
    "Tortoise",
    "Iguana",
    "Komodo Dragon",
    "Snake",
    "Python",
    "Boa Constrictor",
    "Chameleon",
    "Frog",
    "Toad",
    "Salamander",
    "Newt",
    "Fish",
    "Shark",
    "Dolphin",
    "Whale",
    "Seal",
    "Sea Lion",
    "Walrus",
    "Octopus",
    "Squid",
    "Jellyfish",
    "Starfish",
    "Crab",
    "Lobster",
    "Shrimp",
    "Clam",
    "Oyster",
    "Snail",
    "Slug",
    "Butterfly",
    "Moth",
    "Bee",
    "Wasp",
    "Ant",
    "Grasshopper",
    "Cricket",
    "Beetle",
    "Spider",
    "Scorpion",
    "Centipede",
    "Millipede",
    "Bat",
    "Hedgehog",
    "Porcupine",
    "Skunk",
    "Raccoon",
    "Possum",
]

zoo_animals = [i for i in range(len(zoo_animals))]

zoo_animals_reverse = zoo_animals[::-1]


class PointMod:
    def __init__(self, x, y, q):
        self.x = x % q
        self.y = y % q
        self.q = q

    def __add__(self, other):
        if self.q != other.q:
            raise ValueError("Modulus must be the same")
        return PointMod(
            (self.x + other.x) % self.q, (self.y + other.y) % self.q, self.q
        )

    def __mul__(self, other):
        return PointMod((self.x * other) % self.q, (self.y * other) % self.q, self.q)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __hash__(self):
        return self.y * self.q + self.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.q == other.q

    def __str__(self):
        return f"(x={self.x}, y={self.y})"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def makePoint(q):
        def makePoint(x, y):
            return PointMod(x, y, q)

        return makePoint


def generate_dobble_deck(n):
    if n < 2:
        raise ValueError("Number of symbols per card must be at least 2")

    q = n - 1
    makePoint = PointMod.makePoint(q)

    matrix = {}
    qrange = tuple(range(q))
    for x in qrange:
        for y in qrange:
            p = makePoint(x, y)
            matrix[p] = zoo_animals[hash(p) % len(zoo_animals)]

    # print(matrix)

    directions = {
        makePoint(0, 1),
        makePoint(1, 0),
        
        makePoint(1, 1),
        makePoint(1, -1),
        
        makePoint(2, 1),
        makePoint(2, -1),

        makePoint(1, 2),
        makePoint(1, -2),
    }

    directions_to_symbols = {
        d: zoo_animals_reverse[hash(d) % len(zoo_animals)] for d in directions
    }
    #pprint(directions_to_symbols)

    vertical = [makePoint(i, 0) for i in range(q)]
    horizontal = [makePoint(0, i) for i in range(q)]
    all = tuple(
        set(
            vertical
             + horizontal
        )
    )
    # pprint(all)

    deck = []

    for start in all:
        for d in directions:
            line = []
            pprint("newLine")
            for i in qrange:
                p = start + d * i
                print(p, matrix[p])
                line.append(matrix[p])
            line.append(directions_to_symbols[d])
            line = tuple(line)
            deck.append(line)

    deck.append(tuple(directions_to_symbols.values()))

    deck = sorted(set(sorted([tuple(sorted(line)) for line in deck])))

    return deck


def print_deck(deck):
    pprint(deck)
    pprint(len(deck))


if __name__ == "__main__":
    n = 8  # Number of symbols per card
    deck = generate_dobble_deck(n)
    print_deck(deck)
