import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

ON = 255
OFF = 0


def generate_grid(N):
    """Returns a random NxN grid of values"""
    return np.random.choice([ON, OFF], N*N, p=[0.2, 0.8]).reshape(N, N)


# Update grid with Conway's rules
def update(frameNum, img, grid, N):
    # Copy grid to calculate
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # Calculate number of squares which are ON
            # Modulo operator ensures the grid "wraps around" on itself
            total = int((grid[i, (j-1) % N] + grid[i, (j+1) % N] +
                         grid[(i-1) % N, j] + grid[(i+1) % N, j] +
                         grid[(i-1) % N, (j-1) % N] + grid[(i-1) % N, (j+1) % N] +
                         grid[(i+1) % N, (j-1) % N] + grid[(i+1) % N, (j+1) % N])/255)
            # Apply Conway's rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img


# Main() function
def main():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Runs Conway's Game of Life simulation.")

    # Add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    args = parser.parse_args()

    # Set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # Set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # Populate grid with random on/off - more off than on
    grid = generate_grid(N)

    # Set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames=10,
                                  interval=updateInterval,
                                  save_count=50)

    # Set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


# Call main() function if file is run
if __name__ == '__main__':
    main()
