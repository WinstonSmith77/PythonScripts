hat_bezahlt = (("Sven", 0), ("Gunnar", 10),  ("Kevin", 70),  ("Danny", 25), ("Matze", 20), ("Torsten", 0))



def ausgleich(bezahlt):
    schnitt = sum([x[1] for x in bezahlt]) / len(bezahlt)
    bezahlt_korrigiert = dict((x[0], x[1] - schnitt) for x in bezahlt)

    ausgleiche = []

   # pprint(bezahlt_korrigiert)
    while(True):
        bezahlt_korrigiert = {k: v for k, v in bezahlt_korrigiert.items() if abs(v) >=  0.01}

        if not bezahlt_korrigiert:
            break

        max_bezahlt = max(bezahlt_korrigiert.items(), key=lambda x: x[1])
        min_bezahlt = min(bezahlt_korrigiert.items(), key=lambda x: x[1])

        betrag_ausgleich = min(max_bezahlt[1], abs(min_bezahlt[1]))

        ausgleiche.append((min_bezahlt[0], max_bezahlt[0], betrag_ausgleich))
        bezahlt_korrigiert[max_bezahlt[0]] -= betrag_ausgleich
        bezahlt_korrigiert[min_bezahlt[0]] += betrag_ausgleich

   
    return ausgleiche

ausgleiche =(ausgleich(hat_bezahlt))   

for bezahlt in hat_bezahlt:
    print(bezahlt[0], "hat", round(bezahlt[1], 2), "Euro bezahlt")

print("")   

print("Ausgleich:")
print("")

for ausgleich in ausgleiche:
    print(ausgleich[0], "muss an", ausgleich[1], round(ausgleich[2], 2), "Euro zahlen")   