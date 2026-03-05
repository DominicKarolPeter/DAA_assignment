from constants import SEARCH_DEPTH
def get_flooded_size_sim(graph, current_colors):
    start_node = 0
    target_color = current_colors[start_node]

    queue = [start_node]
    visited = {start_node}

    while queue:
        node = queue.pop(0)

        for neighbour in graph[node]:
            if neighbour not in visited and current_colors[neighbour] == target_color:
                visited.add(neighbour)
                queue.append(neighbour)

    return len(visited)
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
    
    # BFS
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

def boundary_options(graph,current_colors):
    start_color=current_colors[0]
    boundaries=set()
    queue=[0]
    visited={0}

    while queue:
        node=queue.pop(0)
        for neighbour in graph[node]:
            if neighbour not in visited:
                if current_colors[neighbour]==start_color:
                    visited.add(neighbour)
                    queue.append(neighbour)
                else:
                    boundaries.add(current_colors[neighbour])
    return boundaries

def backtracking_color_selector(graph,current_colors):
    best_move=None
    max_overall_score=-1
    options=boundary_options(graph,current_colors)

    if len(options)==1:
        return list(options)[0]
    
    for color_choice in options:
        next_state=simulate_move(graph,current_colors,color_choice)
        path_score=backtracking_solve(next_state,SEARCH_DEPTH-1,graph)
        if path_score>max_overall_score:
            max_overall_score=path_score
            best_move=color_choice
        
        if best_move is None:
            return 1
        return best_move
    