from collections import namedtuple
from random import Random
import matplotlib.pyplot as plt
from pprint import pprint

State = namedtuple("State", ["balance", "history"], defaults=[0, [(0, 0)]])
rand = Random()


def isSuccess():
    return rand.randint(0, 1) == 1


def ppprint(*args, **kwargs):
    pprint(*args, **kwargs, underscore_numbers=True)


startBalance = 10
destBalance = 100
state = State(balance=startBalance, history=[(0, startBalance)])


def newState(oldState, deltaBalance):
    newBalance = oldState.balance + deltaBalance
    return State(newBalance, oldState.history + [(deltaBalance, newBalance)])


stake = startBalance
while state.balance < destBalance:
    if isSuccess():
        state = newState(state, stake)
    else:
        state = newState(state, -stake)

    stake *= 1

pprint(state, underscore_numbers=True)

min_balance = min(x[1] for x in state.history)
max_stake = max(abs(x[0]) for x in state.history)
max_debt = min(x[1] - abs(x[1]) for x in state.history)
ppprint(f"Min balance: {min_balance:_}")
ppprint(f"Max stake: {max_stake:_}")
ppprint(f"Max debt: {max_debt:_}")


plt.plot([(abs(x[0]), x[1]) for x in state.history])
plt.xlabel("Steps")
plt.ylabel("Balance")
plt.title("Random Walk")
plt.show()
