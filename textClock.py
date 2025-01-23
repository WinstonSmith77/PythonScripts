

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

def toWords(value):
    if isinstance(value, int):
        result =  i.number_to_words(value)
        return result    
    elif isinstance(value, datetime):
        minute = value.minute
        hour = value.hour
        result = f"{toWords(hour)}    {toWords(minute)}"
        return result

while(True):
    cls()
    now = datetime.now()
   
  
    bigOut(toWords(now))  
    sleep(5)
