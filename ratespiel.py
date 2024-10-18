from random import randint
from argparse import ArgumentParser

MINNUMBER = 1
MAXNUMBER = 100

def get_hint():
    args = ArgumentParser()
    args.add_argument('--hint', action='store_true', help='Provide hints if the guess is too high or too low')
    args = args.parse_args()

    return args.hint

use_hint = get_hint()
print(use_hint)

def enter_number(info_text) -> int:
    valid_input = False
    while not valid_input:
        try:
            number = int(input(f"Guess number beween {MINNUMBER} and  {MAXNUMBER} {info_text}: "))
            valid_input = True
        except ValueError:  # if not a number
            print("Please enter a number!")

    return number        

class Game:
    NEW = 1
    FOUND = 0
    TOO_LOW = 2
    TOO_HIGH = 3
    OUT_OF_RANGE = 4 
    
    def __init__(self, random_number):
        self.__number_of_tries = 0
        self.__random_number = random_number
        self.__state = Game.NEW

    def enter_try(self, number):
        self.__number_of_tries += 1
        if number == self.__random_number:
            self.__state = Game.FOUND
        elif number < MINNUMBER or number > MAXNUMBER:
            self.__state = Game.OUT_OF_RANGE
        elif number > self.__random_number:
            self.__state = Game.TOO_HIGH	
        elif number < self.__random_number:
            self.__state = Game.TOO_LOW

    def get_state(self):
        return self.__state

    def get_number_of_tries(self):
        return self.__number_of_tries

    def get_random_number(self):
        return self.__random_number           

game = Game(randint(MINNUMBER, MAXNUMBER))

while not game.get_state() == Game.FOUND:
    number = enter_number(f'(try number {game.get_number_of_tries() + 1})')
    game.enter_try(number)
    if game.get_state() == Game.FOUND:
        found_solution = True
    elif game.get_state() == Game.OUT_OF_RANGE:
        print(f"Input out of range! Please enter a number between {MINNUMBER} and {MAXNUMBER}!")
    elif game.get_state() == Game.TOO_HIGH:
        print("You guessed too high!")
    elif game.get_state() == Game.TOO_LOW:
        print("You guessed too low!")

print(f"Congratulations! You guessed the number {game.get_random_number()} correctly! You took {game.get_random_number()} tries.")
