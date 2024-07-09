import datetime
from pprint import pprint

first_day_gregorian = datetime.datetime(1582, 10, 15)
end = datetime.datetime(2025, 1, 1)

WEEKDAY_NAMES_GERMAN = (
    "Montag",
    "Dienstag",
    "Mittwoch",
    "Donnerstag",
    "Freitag",
    "Samstag",
    "Sonntag",
)

count_weekdays = {}
for year in range(first_day_gregorian.year, end.year + 1):
    for month in range(1, 13):
        date = datetime.datetime(year, month, 13)

        if date < first_day_gregorian or date > end:
            continue

        weekday = WEEKDAY_NAMES_GERMAN[date.weekday()]
        count_weekdays[weekday] = count_weekdays.get(weekday, 0) + 1

count_weekdays = sorted(count_weekdays.items(), key=lambda x: x[1], reverse=True)

min_count = min(count_weekdays, key=lambda x: x[1])[1]

count_weekdays = [
    (name, f"{count} = {min_count} + {count - min_count}")
    for name, count in count_weekdays
]

pprint(f'Start : {first_day_gregorian}')
pprint(f'End : {end}')
pprint(count_weekdays, underscore_numbers=True)
