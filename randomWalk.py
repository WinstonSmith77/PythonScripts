from collections import namedtuple
from random import Random
import matplotlib.pyplot as plt

State = namedtuple("State", ["balance", "history"], defaults=[0, [0]])
rand = Random()


def isSuccess():
    return rand.randint(0, 1) == 1


startBalance = 100
state = State(balance=startBalance, history=[startBalance])


def newState(state, delta):
    newBalance = state.balance + delta
    return State(newBalance, state.history + [newBalance])


while True:
    if state.balance <= 0:
        break

    stake = max(round(max(state.balance * 0.25, 1)), 0)
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
