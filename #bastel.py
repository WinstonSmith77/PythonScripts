import difflib

a = 'image_5656'
b = 'image_5656(2)'

r = difflib.SequenceMatcher(None, a,b).ratio()
print(r)

