from random import randint

MINNUMBER = 1
MAXNUMBER = 100


random_number = randint(MINNUMBER, MAXNUMBER)


def enter_number():
    valid_input = False
    while not valid_input:
        try:
            number = int(input(f"Guess number beween {MINNUMBER} and  {MAXNUMBER}: "))
            valid_input = True
        except ValueError:  # if not a number
            print("Please enter a number!")

    return number        


found_solution = False
while not found_solution:
    number = enter_number()
    if number == random_number:
        found_solution = True
    if number > random_number:
        print("You guessed too high!")
    elif number < random_number:
        print("You guessed too low!")


print(f"Congratulations! You guessed the number {random_number} correctly!")
