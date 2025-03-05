import random

zoo_animals = [
    "Lion", "Tiger", "Elephant", "Giraffe", "Zebra", "Panda", "Kangaroo", "Koala", "Penguin", "Flamingo",
    "Hippopotamus", "Rhinoceros", "Cheetah", "Leopard", "Gorilla", "Chimpanzee", "Orangutan", "Baboon", "Meerkat", "Lemur",
    "Sloth", "Armadillo", "Anteater", "Otter", "Beaver", "Wolf", "Fox", "Bear", "Polar Bear", "Grizzly Bear",
    "Moose", "Deer", "Bison", "Buffalo", "Camel", "Llama", "Alpaca", "Yak", "Reindeer", "Elk",
    "Ostrich", "Emu", "Peacock", "Parrot", "Macaw", "Toucan", "Eagle", "Hawk", "Falcon", "Owl",
    "Crocodile", "Alligator", "Turtle", "Tortoise", "Iguana", "Komodo Dragon", "Snake", "Python", "Boa Constrictor", "Chameleon",
    "Frog", "Toad", "Salamander", "Newt", "Fish", "Shark", "Dolphin", "Whale", "Seal", "Sea Lion",
    "Walrus", "Octopus", "Squid", "Jellyfish", "Starfish", "Crab", "Lobster", "Shrimp", "Clam", "Oyster",
    "Snail", "Slug", "Butterfly", "Moth", "Bee", "Wasp", "Ant", "Grasshopper", "Cricket", "Beetle",
    "Spider", "Scorpion", "Centipede", "Millipede", "Bat", "Hedgehog", "Porcupine", "Skunk", "Raccoon", "Possum"
]


class PointMod:
    def __init__(self, x, y, q):
        self.x = x
        self.y = y
        self.q = q

    def __add__(self, other):
        if self.q != other.q:
            raise ValueError("Modulus must be the same")
        return PointMod((self.x + other.x) % self.q, (self.y + other.y) % self.q, self.q)

    def __mul__(self, other):
        if self.q != other.q:
            raise ValueError("Modulus must be the same")
        return PointMod((self.x * other) % self.q, (self.y * other)% self.q, self.q)

    def __rmul__(self, other):
        return self.__mul__(other)
    

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.q == other.q

    def __str__ (self):
        return f"(x={self.x}, y={self.y}, q={self.q})"
    
    @staticmethod
    def makePoint(q):
        def makePoint(x, y):
            return PointMod(x, y, q)
        return makePoint

def generate_dobble_deck(n):
    if n < 2:
        raise ValueError("Number of symbols per card must be at least 2")
    
    makePoint = PointMod.makePoint(7)
   
    a = makePoint(1,2)
    b = makePoint(13,14)
   

    print(a + b)
    #print(a * 10)
    #print(10 * a)
    
    
    deck = []
    return deck

def print_deck(deck):
    for card in deck:
        print(card)

if __name__ == "__main__":
    n = 2  # Number of symbols per card
    deck = generate_dobble_deck(n)
    print_deck(deck)