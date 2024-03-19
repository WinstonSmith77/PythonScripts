from datetime import datetime, timedelta

now = datetime.now()
later = datetime.now()

diff:timedelta = (later - now)

print(type(diff))

print(diff.seconds)