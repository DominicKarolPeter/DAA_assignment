import random

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


# def grid_update(selected_color: int, color, graph) -> bool:
#     """
#     Docstring for grid_update

#     :param selected_color: The next color selected by the player or computer.
#     This function should update the grid based on the selected color. It should change the color of the connected region starting from the top-left corner
#     to the new color and expand the connected region accordingly. It should return the updated grid. An example is shown below to illustrate the expected behavior:
#     :return: If the grid was updated successfully, return True. Else, return False.

#     Description of expected behavior:
#         Start from the top-left cell of the grid. That is, node 0. 
#         Change its color to the selected_color. That is color[0] = selected_color.
#         Go to each neighbor (bfs). that is, graph[0]. 
#         IFF neighbor color is same as graph's original color, do the same 3 steps for that neighbor.
#         Continue this process until all connected nodes with the original color have been changed to the selected_color
#     """
#     startN = 0
#     oldC = color[startN]
    
#     if oldC == selected_color:
#         return 0
    
#     q = [startN]
#     visited = {startN}
#     color[startN] = selected_color

#     expanded = False

#     while q:
#         u = q.pop(0)
#         for v in graph[u]:
#             if v not in visited and color[v] == oldC:
#                 color[v] = selected_color
#                 visited.add(v)
#                 q.append(v)
#                 expanded = True
#     if expanded:
#         return 1
#     return -1

def grid_update(selected_color: int, color, graph) -> int:
    startN = 0
    oldC = color[startN]

    if oldC == selected_color:
        return 0

    visited = set()
    q = [startN]
    original_region = set()

    # Step 1: find original flooded region
    while q:
        u = q.pop(0)
        if u in visited:
            continue
        if color[u] == oldC:
            visited.add(u)
            original_region.add(u)
            q.extend(graph[u])

    # Change region color
    for node in original_region:
        color[node] = selected_color

    # Step 2: expand into adjacent selected_color nodes
    q = list(original_region)
    new_region = set(original_region)

    while q:
        u = q.pop(0)
        for v in graph[u]:
            if v not in new_region and color[v] == selected_color:
                new_region.add(v)
                q.append(v)

    # If region size increased → expansion happened
    if len(new_region) > len(original_region):
        return 1
    else:
        return -1
