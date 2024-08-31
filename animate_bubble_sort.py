import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import shuffle
from pathlib import Path
from pprint import pprint as pp

def bubble_sort(arr):
    yield tuple(arr)
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
        yield tuple(arr)


def quicksort(arr, states = None):

    if states is None:
        states = []

    states.append(arr)
    if len(arr) <= 1:
        
        return (arr, states)
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    result = quicksort(left)[0] + middle + quicksort(right)[0]
    states.append(result)
    return (result, states)

      


def get_colors():
    cmap = plt.get_cmap('hsv')
    colors = [cmap(i) for i in range(cmap.N)]   
    return colors

length = 10
all_colors = get_colors()

def export(anim, name):
    pathFile = Path(__file__).parent
    pathFile = Path(pathFile, f"{name}.html")
    print(pathFile) 
    anim.save(pathFile, writer='html')


def make_data():
    data = list(range(0, length))
    shuffle(data)
    return data

def plot(sorter, name):
    # Generate random data
    data = make_data()
    # Create a figure and axis
    fig, ax = plt.subplots()

    # Initialize the bar plot
    bar_rects = ax.bar(range(len(data)), data, align='edge')

    all_states = tuple(sorter(data))
    # Define the update function for the animation
    def update_fig(frame_num, rects):
        # Get the current state to display
        state = all_states[frame_num]
        for rect, val in zip(rects, state):
            rect.set_height(val)  # Update the heights of the bars
            rect.set_color(all_colors[val % len(all_colors)])  # Update the colors of the bars

    # Create the animation
    anim = animation.FuncAnimation(fig, update_fig, frames=range(len(data)), fargs=(bar_rects,), interval=100, repeat=True)
    
    export(anim, name)
   

    # Show the plot
    plt.show()


data = make_data()


pp(tuple(quicksort(data)))

#plot(bubble_sort, 'bubble_sort')
#plot(quicksort, 'quicksort')