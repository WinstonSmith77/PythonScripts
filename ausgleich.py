from pprint import pprint

bezahlt = (("Sven", 0), ("Gunnar", 10),  ("Kevin", 70),  ("Danny", 25), ("Matze", 20), ("Torsten", 0))
average = average = sum([x[1] for x in bezahlt]) / len(bezahlt)

print("Hat bezahlt", bezahlt)
print("Schnitt", average)
print("")

def ausgleich(bezahlt, average):
    bezahlt_korrigiert = dict((x[0], x[1] - average) for x in bezahlt)

    ausgleiche = []

   # pprint(bezahlt_korrigiert)
    while(True):
        bezahlt_korrigiert = {k: v for k, v in bezahlt_korrigiert.items() if abs(v) >=  0.001}

        if not bezahlt_korrigiert:
            break

        max_bezahlt = max(bezahlt_korrigiert.items(), key=lambda x: x[1])
        min_bezahlt = min(bezahlt_korrigiert.items(), key=lambda x: x[1])

        betrag_ausgleich = min(max_bezahlt[1], abs(min_bezahlt[1]))

        ausgleiche.append((min_bezahlt[0], max_bezahlt[0], betrag_ausgleich))
        bezahlt_korrigiert[max_bezahlt[0]] -= betrag_ausgleich
        bezahlt_korrigiert[min_bezahlt[0]] += betrag_ausgleich

   
    return ausgleiche

result =(ausgleich(bezahlt, average))   

for x in result:
    print(x[0], "soll an", x[1], x[2], "Euro zahlen")   