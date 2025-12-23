# FLOOD GAME

# This file is very inefficient in terms of cell recreation. This will be updated soon, but I'll push this into github as of now so that
# you can see the basic structure of the game and the GUI, and start working on the flood fill algorithm and the automation using greedy algorithm.

# Ritesh and Rupesh look at the TODOs and complete the functions as per the docstrings. There should be NO CHANGES to the function signatures or docstrings.
# The parameters and return types should remain the same. They are mentioned clearly in the docstrings.

# If nothing works out after completing your part, don't worry lol. I'll fix it. Just be sure that your part is implemented perfectly.

import tkinter as tk
import random
from collections import deque
import copy

colors = {
    1: "#FF5555",  # RED
    2: "#8BE9FD",  # CYAN
    3: "#50FA7B",  # GREEN
    4: "#BD93F9",  # PURPLE
    5: "#FF79C6",  # PINK
    6: "#F1FA8C"   # YELLOW
}
def grid_generator(n):
    return [[random.randint(1, 6) for p in range(n)] for _ in range(n)]

# TODO
def grid_update(color: int):
    """
    Docstring for grid_update

    :param color: The next color selected by the player or computer.

    This function should update the grid based on the selected color. It should change the color of the connected region starting from the top-left corner
    to the new color and expand the connected region accordingly. It should return the updated grid. An example is shown below to illustrate the expected behavior:

    [[1, 1, 2, 3],                                              [4, 4, 2, 3],
     [1, 2, 2, 3],    ------> After selecting color 4  ---->    [4, 2, 2, 3],
     [1, 4, 2, 3],                                              [4, 4, 2, 3],
     [5, 4, 5, 5]]                                              [5, 4, 5, 5]]

     - In this example, when 4 is selected, it changes the top-left cell to 1. Then every cell connected either horizontally or vertically
     with the same color (1) is changed to 4, and also the cells connected to the newly changed cells again. So,
     - (1, 1) is changed. connected to it, and having the same color are (1, 2) and (2, 1). They are changed.
     - Now connected to (1, 2) and having same color is nothing. So the recursion(??) for that stops here
     - Connected to (2, 1) and having same color is (3, 1). So it is changed too.
     - Now connected to (3, 1) and having same color is nothing. So the recursion(??) for that stops here.
     - After all changes, the final grid is returned.

    :return: The updated grid after applying the flood fill algorithm.


    DO NOT DELETE THIS DOC STRING EVEN AFTER COMPLETING THIS FUNCTION  !!!
    """

    global x  
    
    start_color = x[0][0]
    new_color = color
    n = len(x)
    
    if start_color == new_color:
        return x

    def fill(r, c):
        if r < 0 or r >= n or c < 0 or c >= n:
            return
        
        if x[r][c] != start_color:
            return
        
        x[r][c] = new_color

        fill(r + 1, c)
        fill(r - 1, c)
        fill(r, c + 1)
        fill(r, c - 1)

    fill(0, 0)
    
    return x

def greedy_color_selector(grid):
    """
    This function should implement a greedy algorithm to select the next color to maximize the size of the connected region
    starting from the top-left corner. It should analyze the current grid and return the color that would result in the largest
    expansion of the connected region.

    Common mistake to avoid: Do NOT just return the color which is most frequent in the grid. The goal is to maximize the connected region size,
    not just to pick the most common color. You need to consider how each color choice would affect the connected region starting from the top-left corner.
    Also, don't just look at the immediate neighbors; consider the potential chain reactions that could occur by selecting a particular color.

    :param grid: The current grid state.
    :return: The color that maximizes the connected region size when selected.

    The colors are represented as numbers. The grid is a nested list of numbers. THE RETURN TYPE WILL ALSO BE A NUMBER.
    """
    
def greedy_next_color(grid):
    """
    Selects the color that maximizes the size of the connected region
    starting from the top-left corner (0,0) after one flood move.
    """

    rows = len(grid)
    cols = len(grid[0])

    # -------- helper: find flooded region --------
    def flooded_region(g):
        start_color = g[0][0]
        visited = set()
        q = deque([(0, 0)])
        visited.add((0, 0))

        while q:
            x, y = q.popleft()
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < rows and
                    0 <= ny < cols and
                    (nx, ny) not in visited and
                    g[nx][ny] == start_color):
                    visited.add((nx, ny))
                    q.append((nx, ny))
        return visited

    # -------- helper: apply flood fill --------
    def apply_flood(g, new_color):
        region = flooded_region(g)
        for x, y in region:
            g[x][y] = new_color

    # ------------------------------------------

    current_color = grid[0][0]
    all_colors = set(cell for row in grid for cell in row)

    best_color = current_color
    max_region_size = -1

    # Try each possible color (except current)
    for color in all_colors:
        if color == current_color:
            continue

        # Simulate the move
        temp_grid = copy.deepcopy(grid)
        apply_flood(temp_grid, color)

        # Measure resulting region size
        region_size = len(flooded_region(temp_grid))

        if region_size > max_region_size:
            max_region_size = region_size
            best_color = color

    return best_color


size = 15
x = grid_generator(size)

root = tk.Tk()
root.geometry("1300x600")

game_frame = tk.Frame(root, bd=1, relief="solid")
game_frame.place(relx=0.1, rely=0, width=550, height=550)

def grid_rebuild(e, color):
    global x
    x = grid_update(color)
    draw_grid(x)

def draw_grid(grid):
    # Delete everything in game_frame
    for widget in game_frame.winfo_children():
        widget.destroy()

    # Rebuild the grid
    for i in range(len(grid)):
        for j in range(len(grid)):
            cell_color = colors[grid[i][j]]
            cell = tk.Label(game_frame, bg=cell_color, width=4, height=2, borderwidth=0, relief="solid")
            cell.place(relheight=1/size, relwidth=1/size, anchor="nw", relx=j*(1/size), rely=i*(1/size))
            # cell.bind("<B1-Release>", lambda: grid_rebuild(color=grid[i][j]))
            cell.bind("<ButtonRelease-1>", lambda e, color=grid[i][j]: grid_rebuild(e, color))

draw_grid(x)
root.mainloop()
