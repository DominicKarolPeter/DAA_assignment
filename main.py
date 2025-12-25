# FLOOD GAME

# Ritesh and Rupesh look at the TODOs and complete the functions as per the docstrings. There should be NO CHANGES to the function signatures or docstrings.
# The parameters and return types should remain the same. They are mentioned clearly in the docstrings.

import tkinter as tk
import random

# CONSTANTS
COLORS = {
    1: "#FF5555",  # RED
    2: "#8BE9FD",  # CYAN
    3: "#50FA7B",  # GREEN
    4: "#BD93F9",  # PURPLE
    5: "#FF79C6",  # PINK
    6: "#F1FA8C"   # YELLOW
}
SIZE = 15

# Generates a random graph represented by numbers 1 to 6
def grid_generator(n: int) -> tuple[dict, list]:
    """
    Docstring for grid_generator

    Time complexity: O(n^2)
    :param n: Size of the grid
    :return: A graph represented as adjacency list and a list of colors for each node.
    :rtype: A tuple (graph, color)
    """
    color = [random.randint(1, 6) for _ in range(n*n)]

    graph = {}
    for i in range(n*n):
        graph[i] = []
        if (i + 1) < n**2 and (i + 1) % n != 0:
            graph[i].append(i + 1)
        if (i - 1) >= 0 and i % n != 0:
            graph[i].append(i - 1)
        if (i + n) < n**2:
            graph[i].append(i + n)
        if (i - n) >= 0:
            graph[i].append(i - n)
    return graph, color

graph, color = grid_generator(SIZE)


# TODO
def grid_update(selected_color: int) -> None:
    """
    Docstring for grid_update

    :param selected_color: The next color selected by the player or computer.
    This function should update the grid based on the selected color. It should change the color of the connected region starting from the top-left corner
    to the new color and expand the connected region accordingly. It should return the updated grid. An example is shown below to illustrate the expected behavior:
    :return: No return value is expected from this function.

    Description of expected behavior:
        Start from the top-left cell of the grid. That is, node 0. 
        Change its color to the selected_color. That is color[0] = selected_color.
        Go to each neighbor (bfs). that is, graph[0]. 
        IFF neighbor color is same as graph's original color, do the same 3 steps for that neighbor.
        Continue this process until all connected nodes with the original color have been changed to the selected_color

    DO NOT DELETE THIS DOC STRING EVEN AFTER COMPLETING THIS FUNCTION  !!!
    """

    pass

def greedy_color_selector(graph, color) -> int:
    """
    Docstring for greedy_color_selector

    :param graph: The current graph state. It is a dictionary representing the adjacency list.
    :param color: The current color of each node. It is a list
    :return: The color that maximizes the connected region size when selected. TYPE IS INTEGER. ISTG IF YOU RETURN ANYTHING ELSE...
    
    This function should implement a greedy algorithm to select the next color to maximize the size of the connected region
    starting from the top-left corner. It should analyze the current grid and return the color that would result in the largest
    expansion of the connected region.

    Common mistake to avoid: Do NOT just return the color which is most frequent in the grid. The goal is to maximize the connected region size,
    not just to pick the most common color. You need to consider how each color choice would affect the connected region starting from the top-left corner.
    Also, don't just look at the immediate neighbors; consider the potential chain reactions that could occur by selecting a particular color.

    """
    start_color = color[0]
    best_color = start_color
    best_size = -1

    for candidate in range(1, 7):
        if candidate == start_color:
            continue

        temp_color = color[:]
        queue = [0]
        visited = set([0])
        temp_color[0] = candidate

        while queue:
            u = queue.pop(0)
            for v in graph[u]:
                if v not in visited and temp_color[v] == start_color:
                    visited.add(v)
                    temp_color[v] = candidate
                    queue.append(v)

        size = len(visited)

        if size > best_size:
            best_size = size
            best_color = candidate

    return best_color


    

########################################################################################
# ------------------------------       GAME WINDOW       -------------------------------
########################################################################################

root = tk.Tk()
root.geometry("1300x600")

game_frame = tk.Frame(root, bd=1, relief="solid")
game_frame.place(relx=0.1, rely=0, width=550, height=550)

canvas = tk.Canvas(game_frame, highlightthickness=0)
canvas.place(relwidth=1, relheight=1)

cell_size = 550 / SIZE  # pixel size per cell


def grid_rebuild(selected_color: int):
    # grid_update mutates `color` directly
    grid_update(selected_color)
    draw_grid(color)


def on_click(event):
    col = int(event.x // cell_size)
    row = int(event.y // cell_size)

    if 0 <= row < SIZE and 0 <= col < SIZE:  # Ensuring to work only on clicks within the grid
        node = row * SIZE + col  # row 1, column 5 with a size of 6 would be node 11
        selected_color = color[node]
        grid_rebuild(selected_color)


def draw_grid(color):
    canvas.delete("all")

    for node in range(SIZE * SIZE):
        cell_color = COLORS[color[node]]

        row = node // SIZE
        col = node % SIZE

        x0 = col * cell_size
        y0 = row * cell_size
        x1 = x0 + cell_size
        y1 = y0 + cell_size

        canvas.create_rectangle(
            x0, y0, x1, y1,
            fill=cell_color,
            outline=""
        )


canvas.bind("<ButtonRelease-1>", on_click)

draw_grid(color)
root.mainloop()
