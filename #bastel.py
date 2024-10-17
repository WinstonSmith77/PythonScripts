def tuple_to_str_seperated_by_semikolon(t):
    t = map(str, t)
    return f"{';'.join(t)}"


print(tuple_to_str_seperated_by_semikolon((1, 2, 3)))