import itertools
import time

texts = ['mac', 'pc']
wrapper = 'a {} is not '
sleep_time = 0.2

def do_it(texts, wrapper, sleep_time):
    for text in itertools.cycle(texts):
        print(wrapper.format(text), end = '')
        time.sleep(sleep_time)


do_it(texts, wrapper, sleep_time)        


