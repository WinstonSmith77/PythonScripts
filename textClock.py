

import pyfiglet
import inflect
from datetime import datetime
from time import sleep

import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

i = inflect.engine()

def bigOut(text ):
    result = pyfiglet.figlet_format(text)
    print(result)

def toWords(number):
    result =  i.number_to_words (str(number))
    return result    

while(True):
    cls()
    now = datetime.now()
    minute = now.minute
    hour = now.hour
    result = f"{toWords(hour)}    {toWords(minute)}"
    bigOut(result)  
    sleep(5)
