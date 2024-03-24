from datetime import datetime

now = datetime.now()
delta = datetime.now() - now

print(delta.seconds)