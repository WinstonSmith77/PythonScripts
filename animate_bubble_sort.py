import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import shuffle

def bubble_sort(arr):
    yield tuple(arr)
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
        yield tuple(arr)

def get_colors():
    cmap = plt.get_cmap('')
    colors = [cmap(i) for i in range(cmap.N)]   
    return colors

length = 50
all_colors = get_colors()

def plot():
    # Generate random data
    data = list(range(0, length))
    shuffle(data)
    # Create a figure and axis
    fig, ax = plt.subplots()

    # Initialize the bar plot
    bar_rects = ax.bar(range(len(data)), data, align='edge')

    all_states = tuple(bubble_sort(data))
    # Define the update function for the animation
    def update_fig(frame_num, rects):
        # Get the current state to display
        state = all_states[frame_num]
        for rect, val in zip(rects, state):
            rect.set_height(val)  # Update the heights of the bars
            rect.set_color(all_colors[val % len(all_colors)])  # Update the colors of the bars

    # Create the animation
    anim = animation.FuncAnimation(fig, update_fig, frames=range(len(data)), fargs=(bar_rects,), interval=100, repeat=True)

    # Show the plot
    plt.show()

plot()