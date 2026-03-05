"""backtracking_color_selector()
        │
        ▼
Find boundary colors
        │
        ▼
Simulate each move
        │
        ▼
Call backtracking_solve()
        │
        ▼
Explore future states recursively
        │
        ▼
Evaluate flood size
        │
        ▼
Return best move
"""
"""
implements a Flood-It game solver using a combination of Breadth-First Search (BFS)
 and depth-limited backtracking. The algorithm simulates possible color moves from the starting tile
   and recursively explores future states up to a predefined search depth. Each simulated state is evaluated based 
   on the size of the flooded region, with a small heuristic bonus for states that create more expansion opportunities 
   along the boundary. By comparing the scores of different move sequences, the algorithm selects the color that maximizes 
   the flooded area and leads to the most promising board configuration.
"""


from collections import deque
from constants import SEARCH_DEPTH


def get_flooded_size_sim(graph, colors):
    start = 0
    flood_color = colors[start]

    queue = deque([start])
    visited = {start}

    while queue:
        node = queue.popleft()

        for neighbour in graph[node]:
            if neighbour not in visited and colors[neighbour] == flood_color:
                visited.add(neighbour)
                queue.append(neighbour)

    return len(visited)
def simulate_move(graph, colors, new_color):
    """
    Creates a simulated board after applying a color move.
    Does NOT modify the original board.
    """

    new_colors = colors.copy()
    start = 0
    old_color = new_colors[start]

    if old_color == new_color:
        return new_colors

    queue = deque([start])
    visited = {start}

    new_colors[start] = new_color

    while queue:
        node = queue.popleft()

        for neighbour in graph[node]:
            if neighbour not in visited and new_colors[neighbour] == old_color:
                visited.add(neighbour)
                new_colors[neighbour] = new_color
                queue.append(neighbour)

    return new_colors



def boundary_options(graph, colors):
    start = 0
    start_color = colors[start]

    queue = deque([start])
    visited = {start}
    boundary_colors = set()

    while queue:
        node = queue.popleft()

        for neighbour in graph[node]:
            if neighbour not in visited:

                if colors[neighbour] == start_color:
                    visited.add(neighbour)
                    queue.append(neighbour)
                else:
                    boundary_colors.add(colors[neighbour])

    return boundary_colors


def backtracking_solve(colors, depth, graph):

    if depth == 0:
        return get_flooded_size_sim(graph, colors)

    options = boundary_options(graph, colors)

    if not options:
        return 9999

    best_score = -1

    for color in options:

        next_state = simulate_move(graph, colors, color)

        score = backtracking_solve(next_state, depth - 1, graph)

        bonus = len(boundary_options(graph, next_state)) * 0.1

        total_score = score + bonus

        if total_score > best_score:
            best_score = total_score

    return best_score


def backtracking_color_selector(graph, colors):

    options = boundary_options(graph, colors)

    if len(options) == 1:
        return next(iter(options))

    best_move = None
    best_score = -1

    for color in options:

        next_state = simulate_move(graph, colors, color)

        score = backtracking_solve(next_state, SEARCH_DEPTH - 1, graph)

        if score > best_score:
            best_score = score
            best_move = color

    return best_move if best_move is not None else 1