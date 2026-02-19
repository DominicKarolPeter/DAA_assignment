#   DP Logic:
memo = {}
SEARCH_DEPTH = 4 # DP Lookahead depth

def get_flooded_size_sim(graph, current_colors):
    """Helper: Counts size of flooded region for a simulation state."""
    target_c = current_colors[0]
    count = 0
    visited = {0}
    q = [0]
    while q:
        u = q.pop(0)
        count += 1
        for v in graph[u]:
            if v not in visited and current_colors[v] == target_c:
                visited.add(v)
                q.append(v)
    return count

def simulate_move(graph, current_colors, move_color):
    """
    Returns a NEW list of colors after applying a hypothetical move.
    Does NOT change the global 'color' list.
    """
    new_colors = list(current_colors)
    start_node = 0
    old_c = new_colors[start_node]
    
    if old_c == move_color:
        return new_colors

    # BFS to change color
    q = [start_node]
    visited = {start_node}
    new_colors[start_node] = move_color
    
    while q:
        u = q.pop(0)
        for v in graph[u]:
            if v not in visited and new_colors[v] == old_c:
                visited.add(v)
                new_colors[v] = move_color
                q.append(v)
    return new_colors

def dp_solve(current_colors, depth, graph):
    """
    Recursive DP Function with Memoization.
    Returns: (Best Score, Best First Move)
    """
    # check whether already present
    state_key = (tuple(current_colors), depth)
    if state_key in memo:
        return memo[state_key]
    
    # 1.Base case
    if depth == 0:
        return (get_flooded_size_sim(graph, current_colors), None)
    
    # valid moves
    start_c = current_colors[0]
    boundary_colors = set()
    visited = {0}
    q = [0]
    
    # Traverse current flood to find neighbors
    while q:
        u = q.pop(0)
        for v in graph[u]:
            if v not in visited:
                if current_colors[v] == start_c:
                    visited.add(v)
                    q.append(v)
                else:
                    boundary_colors.add(current_colors[v])
    
    if not boundary_colors: # Already solved or no moves- edge case
        return (9999, None)

    # 2.Recursive step
    best_score = -1
    best_move = list(boundary_colors)[0]

    for move in boundary_colors:
        next_state_colors = simulate_move(graph, current_colors, move)
        
        score, _ = dp_solve(next_state_colors, depth - 1, graph)
        
        if score > best_score:
            best_score = score
            best_move = move
            
    # updating memo
    memo[state_key] = (best_score, best_move)
    return (best_score, best_move)

def dp_color_selector(graph, color) -> int:
    """
    Main entry point for the computer player.
    """
    global memo
    memo = {} # Clear memory for new turn to save RAM
    
    # Run DP
    # Note: graph is global or passed, but dp_solve needs it. 
    # Since graph is constant structure, we access it globally or pass it.
    score, move = dp_solve(color, SEARCH_DEPTH, graph)
    
    # Fallback if None returned (rare edge case if solved)
    if move is None:
        return 1 
        
    return move
