import itertools

texts = ['mac', 'pc']
wrapper = 'a {} is not '

for text in itertools.cycle(texts):
    print(wrapper.format(text), end = '')
    