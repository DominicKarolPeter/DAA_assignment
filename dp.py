from constants import SEARCH_DEPTH
#   DP Logic:
memo = {}

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

def dp_solve(current_colors, depth, graph):
    state_key = (tuple(current_colors), depth)

    # 1. check memory
    if state_key in memo:
        return memo[state_key]
    
    # 2. Base case
    if depth == 0:
        return (get_flooded_size_sim(graph, current_colors), None)
    
    #3. valid moves
    options=boundary_options(graph,current_colors)
    
    if not options: # Already solved or no moves- edge case
        return (9999, None)

    #4.Recursive step
    best_score = -1
    best_move = None

    for color_choice in options:
        next_state_colors = simulate_move(graph, current_colors, color_choice)
        score, _ = dp_solve(next_state_colors, depth - 1, graph)
        
        if score > best_score:
            best_score = score
            best_move = color_choice
            
    # 5. updating memo
    memo[state_key] = (best_score, best_move)
    return (best_score, best_move)

def dp_color_selector(graph, color) -> int:
    """
    Main entry point for the computer player.
    """
    global memo
    memo = {} 
    score, move = dp_solve(color, SEARCH_DEPTH, graph)
    

    if move is None:
        return 1 
        
    return move