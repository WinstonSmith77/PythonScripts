import datetime
from pprint import pprint
from itertools import groupby

first_day_gregorian = datetime.datetime(1582, 10, 15)
end = datetime.datetime(first_day_gregorian.year + 400, first_day_gregorian.month, first_day_gregorian.day)

WEEKDAY_NAMES_GERMAN = (
    "Montag",
    "Dienstag",
    "Mittwoch",
    "Donnerstag",
    "Freitag",
    "Samstag",
    "Sonntag",
)

def calculate_weekday(date : datetime):
    month = date.month
    year = date.year
    day = date.day
    if month < 3:
        month += 12
        year -= 1
    K = year % 100
    J = year // 100
    h = (day + ((13 * (month + 1)) // 5) + K + (K // 4) + (J // 4) + (5 * J)) % 7
    # Convert Zeller's Congruence to Python's weekday (Monday = 0, Sunday = 6)
    return (h + 2) % 7

count_weekdays = {}
for year in range(first_day_gregorian.year, end.year + 1):
    for month in range(1, 13):
        date = datetime.datetime(year, month, 13)

        if date < first_day_gregorian or date > end:
            continue

        weekday = WEEKDAY_NAMES_GERMAN[calculate_weekday(date)]
        count_weekdays[weekday] = count_weekdays.get(weekday, 0) + 1

count_weekdays = sorted(count_weekdays.items(), key=lambda x: x[1], reverse=True)

min_count = min(count_weekdays, key=lambda x: x[1])[1]

count_weekdays = [
    (name, f"{count:_} = {min_count:_} + {count - min_count:_}")
    for name, count in count_weekdays
]

count_weekdays = [list(lines) for _, lines  in groupby(count_weekdays, key=lambda x: x[1])]

pprint(f'Start : {first_day_gregorian}')
pprint(f'End : {end}')
pprint(count_weekdays, underscore_numbers=True)


