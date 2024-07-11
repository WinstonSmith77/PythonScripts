from collections import namedtuple
from random import Random
import matplotlib.pyplot as plt

State = namedtuple("State", ["balance", "history"], defaults=[0, [0]])
rand = Random()


def isSuccess():
    return rand.randint(0, 1) == 1


startBalance = 100
state = State(balance=startBalance, history=[startBalance])


def newState(oldState, deltaBalance):
    newBalance = oldState.balance + deltaBalance
    return State(newBalance, oldState.history + [newBalance])


while True:
    if state.balance <= 0:
        break

    stake = max(round(max(state.balance * 0.5, 1)), 0)
    if isSuccess():
        state = newState(state, stake)
    else:
        state = newState(state, -stake)

print(state)

plt.plot(state.history)
plt.xlabel("Step")
plt.ylabel("Account Balance")
plt.title("Random Walk")
plt.show()
