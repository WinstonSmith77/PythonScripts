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

def generate_dobble_deck(n):
    if n < 2:
        raise ValueError("Number of symbols per card must be at least 2")
    
    deck = []
    symbols = list(range(n * (n - 1) + 1))

    symbols = [zoo_animals[i] for i in symbols]
    
    for i in range(n):
        card = [symbols[i * (n - 1) + j] for j in range(n - 1)]
        card.append(symbols[-1])
        deck.append(card)
    
    for i in range(n - 1):
        for j in range(n - 1):
            card = [symbols[i * (n - 1) + k] for k in range(n - 1)]
            card.append(symbols[j])
            deck.append(card)
    
    random.shuffle(deck)
    return deck

def print_deck(deck):
    for card in deck:
        print(card)

if __name__ == "__main__":
    n = 2  # Number of symbols per card
    deck = generate_dobble_deck(n)
    print_deck(deck)