import itertools
import string

length = 3
valid_key_elements = list(string.digits)


print(list(map(lambda x : ''.join(x), )))

all_numbers = set(range(0 , 10 ** length))
all_numbers_list = list(all_numbers)

print(all_numbers_list[0])
print(all_numbers_list[-1])





# for pw in map(lambda c : ''.join(c), itertools.combinations_with_replacement(valid_key_elements, length)):
#     all_numbers.remove(int(pw))

# print(all_numbers)    

