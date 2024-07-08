import datetime
from pprint import pprint

first_day_gregorian = datetime.datetime(1582, 10, 15)
end = datetime.datetime(2025, 1, 1)

count_weekdays = {}
for year in range(first_day_gregorian.year, end.year + 1):
    for month in range(1, 13):
        
        date = datetime.datetime(year, month, 13)

        if date < first_day_gregorian or date > end:
            continue

        pprint(date)    

        weekday = date.weekday()
        count_weekdays[weekday] = count_weekdays.get(weekday, 0) + 1

count_weekdays = sorted(count_weekdays.items(), key=lambda x: x[1], reverse=True)        

pprint(count_weekdays)
