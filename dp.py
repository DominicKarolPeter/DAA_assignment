def simulate_move(graph, current_color, move_color):
    """
    State Transition Function (S → S′)
    Creates a new hypothetical board after applying a move.
    Does NOT modify the original board.
    """

    new_colors = list(current_color)

    start_node = 0
    old_color = new_colors[start_node]

    if old_color == move_color:
        return new_colors
    
    #BFS
    queue = [start_node]
    visited = {start_node}
    new_colors[start_node] = move_color

    while queue:
        u = queue.pop(0)
        for v in graph[u]:
            if v not in visited and new_colors[v] == old_color:
                visited.add(v)
                new_colors[v] = move_color
                queue.append(v)
    return new_colors

def get_flooded_size(graph, colors):

    """
    Utility Function
    Returns size of flooded region starting from node 0.
    """
    start_node = 0
    target_color = colors[start_node]

    queue = deque([start_node])
    visited = set([start_node])

    while queue:
        node = queue.popleft()

        for neighbour in graph[node]:
            if neighbour not in visited and colors[neighbour] == target_color:
                visited.add(neighbour)
                queue.append(neighbour)
    return len(visited)

def boundary_colors(graph,colors):
    start_node = 0
    base_color = colors[start_node]

    queue = deque([start_node])
    visited = set([start_node])

    while queue:
        node = queue.popleft()
        for neighbour in graph[node]:
            if neighbour not in visited and colors[neighbour] == base_color:
                visited.add(neighbour)
                queue.append(neighbour)
    
    boundary = set()

    for node in visited:
        for neighbour in graph[node]:
            if neighbour not in visited:
                boundary.add(colors[neighbour])
    
    return boundary
