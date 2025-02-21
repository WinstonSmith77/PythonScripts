import random
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

faktor = range(10)
lern_faktoren = [1, 3, 5, 10]

all_aufgaben = list(set((a + 1, b) for a in faktor for b in lern_faktoren))
random.shuffle(all_aufgaben)

anzahl = 10

all_aufgaben = all_aufgaben[0:anzahl]

for index, aufgabe in enumerate(all_aufgaben):        
    richtig = False
    while not richtig:
        cls()
        print(f"{index + 1} von {anzahl}") 
        try:
            eingabe =   input(f"{aufgabe[0]} * {aufgabe[1]} = ?")
            ergebnis = int(eingabe)
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")
            continue
        if ergebnis == aufgabe[0] * aufgabe[1]:
            print("Richtig!")
            richtig = True
        else:
            print("Falsch! Nochmal probieren.")
