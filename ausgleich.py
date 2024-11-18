from pprint import pprint

bezahlt = (("M", 0), ("G", 10),  ("K", 70),  ("D", 25), ("MH", 20), ("T", 0))
average = average = sum([x[1] for x in bezahlt]) / len(bezahlt)

pprint(bezahlt)
pprint(average)

def ausgleich(bezahlt, average):
    bezahlt_korrigiert = dict((x[0], x[1] - average) for x in bezahlt)

   # pprint(bezahlt_korrigiert)
    
    max_bezahlt = max(bezahlt_korrigiert.values())
    min_bezahlt = min(bezahlt_korrigiert.values())
    
    pprint(max_bezahlt)
    pprint(min_bezahlt)
   
    return bezahlt_korrigiert

pprint(ausgleich(bezahlt, average))