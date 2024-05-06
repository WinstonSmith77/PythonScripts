xrange = range(5)

adders = [lambda y, x = x : x + y  for x in xrange]


for i in xrange:
    print(adders[i](10))