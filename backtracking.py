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