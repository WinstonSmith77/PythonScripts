hat_bezahlt = [
    ("Matthias", 168.11),
    ("Roberto", 59),
    ("Jens M.", 65),
    ("Jens G.", 0),
    ("Stefan", 12 + 12),
]


def do_ausgleich(bezahlt: list[tuple[str, float]]) -> list[tuple[str, str, float]]:
    summe : float = sum([x[1] for x in bezahlt])
    
    #print(summe)

    schnitt : float = summe / len(bezahlt)

    #print(schnitt)
    bezahlt_korrigiert: dict[str, float] = {x[0]: (x[1] - schnitt) for x in bezahlt}

    ausgleiche = []

    while True:
        bezahlt_korrigiert = {
            k: v for k, v in bezahlt_korrigiert.items() if abs(v) >= 0.01
        }

        #bezahlt_korrigiert  = dict(sorted(bezahlt_korrigiert.items(), key=lambda x: x[1], reverse=True))

        if not bezahlt_korrigiert:
            break

        #print(bezahlt_korrigiert)    

        max_bezahlt = max(bezahlt_korrigiert.items(), key=lambda x: x[1])
        min_bezahlt = min(bezahlt_korrigiert.items(), key=lambda x: x[1])

        betrag_ausgleich = min(abs(max_bezahlt[1]), abs(min_bezahlt[1]))

        ausgleiche.append((min_bezahlt[0], max_bezahlt[0], betrag_ausgleich))
        bezahlt_korrigiert[max_bezahlt[0]] -= betrag_ausgleich
        bezahlt_korrigiert[min_bezahlt[0]] += betrag_ausgleich

        

    return ausgleiche


ausgleiche: list[tuple[str, str, float]] = do_ausgleich(hat_bezahlt)

for bezahlt in hat_bezahlt:
    print(bezahlt[0], "hat", round(bezahlt[1], 2), "Euro bezahlt")

print("")

print("Ausgleich:")
print("")

ausgleich: tuple[str, str, float]
for ausgleich in ausgleiche:
    print(ausgleich[0], "muss an", ausgleich[1], round(ausgleich[2], 2), "Euro zahlen")
