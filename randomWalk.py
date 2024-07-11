from collections import namedtuple
from random import Random

State = namedtuple("State", ["account","history"], defaults=[0, []])
rand = Random()


def isSuccess():
    return rand.randint(0, 1) == 1


state = State(account= 100)

def newState(state, delta):
    return State(state.account + delta, state.history + [state.account])

while True:
   
    if state.account <= 0:
        break

    if(len(state.history) > 100):
        break

    stake = max(state.account * .5, 0)
    if isSuccess():
        state = newState(state, stake)
    else:
        state = newState(state, -stake)

import matplotlib.pyplot as plt

plt.plot(state.history)
plt.xlabel('Step')
plt.ylabel('Account Balance')
plt.title('Random Walk')
plt.show()
