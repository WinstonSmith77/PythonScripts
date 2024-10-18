from random import randint

MINNUMBER = 1
MAXNUMBER = 100

random_number = randint(MINNUMBER, MAXNUMBER)

def enter_number(info_text) -> int:
    valid_input = False
    while not valid_input:
        try:
            number = int(input(f"Guess number beween {MINNUMBER} and  {MAXNUMBER} {info_text}: "))
            valid_input = True
        except ValueError:  # if not a number
            print("Please enter a number!")

    return number        



class GameState:
    NEW = 1
    FOUND = 0
    TOO_LOW = 2
    TOO_LOW = 3
    OUT_OF_RANGE = 4 
    
    def __init__(self, random_number):
        self.number_of_tries = 0
        self.random_number = random_number
        self.state = GameState.NEW

    def enter_try(self, number):
        if number == random_number:
            self.found_solution = True
            self.state = GameState.FOUND
        elif number > random_number:
            self.state = GameState.TOO_HIGH	
            self.number_of_tries += 1
        elif number < random_number:
            self.state = GameState.TOO_LOW
            self.number_of_tries += 1

    def get_state(self):
        return self.state

    def get_number_of_tries(self):
        return self.number_of_tries           

found_solution = False
number_of_tries = 0


while not found_solution:
    number = enter_number(f'(try number {number_of_tries + 1})')
    number_of_tries += 1
    if number == random_number:
        found_solution = True
    if number > random_number:
        print("You guessed too high!")
    elif number < random_number:
        print("You guessed too low!")


print(f"Congratulations! You guessed the number {random_number} correctly! You took {number_of_tries} tries.")
