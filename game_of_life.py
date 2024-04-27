import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

def random_grid(size):
    """Returns a grid of given size filled with random 0s or 1s."""
    return np.random.choice([0, 1], size*size, p=[0.8, 0.2]).reshape(size, size)

def update(frameNum, img, grid, size, pause):
    """Update the grid and the image for the next frame, respecting the pause state."""
    if not pause[0]:  # Only update if not paused
        newGrid = grid.copy()
        for i in range(size):
            for j in range(size):
                total = int((grid[i, (j-1)%size] + grid[i, (j+1)%size] +
                             grid[(i-1)%size, j] + grid[(i+1)%size, j] +
                             grid[(i-1)%size, (j-1)%size] + grid[(i-1)%size, (j+1)%size] +
                             grid[(i+1)%size, (j-1)%size] + grid[(i+1)%size, (j+1)%size]))
                if grid[i, j] == 1:
                    if (total < 2) or (total > 3):
                        newGrid[i, j] = 0
                else:
                    if total == 3:
                        newGrid[i, j] = 1
        img.set_data(newGrid)
        grid[:] = newGrid[:]
    return img,

def onClick(event, img, grid, size):
    """Handle click events to toggle cells."""
    if event.xdata and event.ydata:  # Check if click is inside the axes
        ix, iy = int(event.xdata), int(event.ydata)
        grid[iy, ix] = 1 - grid[iy, ix]  # Toggle the cell state
        img.set_data(grid)

def onKeyPress(event, fig, pause):
    """Handle key press events to exit fullscreen or toggle pause."""
    if event.key == 'escape':
        plt.close(fig)  # Close the plot window
    elif event.key == 'p':
        pause[0] = not pause[0]  # Toggle pause state

def show_instructions():
    """Show instructions in a message box before starting the game."""
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Instructions",
                        "Use ESC button to exit.\nClick on a cell to create or destroy life.\nPress 'P' to pause or resume the game.")
    root.destroy()

def main():
    size = 32  # Suitable size for the display
    updateInterval = 50
    pause = [False]  # Pause state control, using a list to maintain reference in callback

    show_instructions()  # Show the initial instructions

    grid = random_grid(size)

    fig, ax = plt.subplots(figsize=(10, 10))  # 10x10 inch window
    img = ax.imshow(grid, interpolation='nearest', aspect='auto')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, size, pause),
                                  frames=10,
                                  interval=updateInterval,
                                  save_count=50)

    fig.canvas.mpl_connect('button_press_event', lambda event: onClick(event, img, grid, size))
    fig.canvas.mpl_connect('key_press_event', lambda event: onKeyPress(event, fig, pause))

    plt.get_current_fig_manager().resize(800, 800)  # Resize the window to 800x800 pixels
    plt.show()

if __name__ == '__main__':
    main()
