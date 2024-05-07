from pprint import pprint

xrange = range(5)

def make_adder_freeze_x(x):
    pprint(locals())
    def adder(y):
        return x + y
    return adder

adders = [make_adder_freeze_x(x)  for x in xrange]


for i in xrange:
    print(adders[i](10))