from random import randint

MINNUMBER = 1
MAXNUMBER = 100


random_number = randint(MINNUMBER, MAXNUMBER)


number = int(input(f"Guess number beween {MINNUMBER} and  {MAXNUMBER}: "))

while number != random_number:
    if number > random_number:
        print("You guessed too high!")
    elif number < random_number:
        print("You guessed too low!")
    number = int(input(f"Guess number beween {MINNUMBER} and  {MAXNUMBER}: "))

print(f"Congratulations! You guessed the number {random_number} correctly!")

