
a = 1

b = [[2,3], []]


def merge(l, lofl):
        result = [l] + [j for alist in lofl for j in alist]
        return result

print(merge(a, b))

