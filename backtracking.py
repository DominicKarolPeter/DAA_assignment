"""
Backtracking Strategy
Backtracking in Flood means looking ahead several moves and undoing/reconsidering choices that don't lead to efficient progress. Here's how to apply it:
1. Go Deep, Not Wide
It's wise to go "deep" — select the colour which takes you furthest into the unflooded territory. OSS Blog Don't just pick the colour that absorbs the most adjacent squares; pick the one that opens up the longest path into new regions.
2. Plan Sequences, Not Single Moves
Instead of evaluating one move at a time, mentally (or on paper) plan 3–5 moves ahead. Ask: "If I pick red now, what colours does that unlock next?"
3. Identify "Bottleneck" Colours
Some colours act as bridges to large regions. Delay or avoid wasting moves on colours that are isolated or small — save those for when they connect two large blobs.
4. Backtrack When You Hit a Dead End
If you've used several moves and the flooded region grew slowly, undo (Ctrl+Z) back to the branching point and try the alternative colour sequence. The game supports undo, so use it freely to explore branches.
5. Prioritise the Perimeter
Work toward the farthest corners early. The bottom-right corner is hardest to reach last, so try to connect to distant regions before mopping up nearby ones.
6. Avoid Colour Repetition
Consecutive moves of the same colour are almost always wasted (since you already absorbed all that colour's neighbours). Backtrack if you find yourself cycling through the same colours without gaining ground.
7. Count Remaining Colours
Near the end, count how many distinct colour regions remain and compare to your remaining moves. If the numbers don't match up, backtrack earlier to find a more efficient path.
"""
"""
Backtracking Strategy for Flood It!
-------------------------------------
Unlike DP (which looks ahead a fixed depth and maximizes flooded size),
backtracking searches for the SHORTEST sequence of moves to solve the board.

Key ideas:
  - DFS through possible color sequences
  - Prune any branch where moves_used >= current best known solution
  - Use greedy heuristic to ORDER the color choices (try promising moves first)
  - Memoize visited (state, moves_used) pairs to avoid re-exploring

Entry point: backtracking_color_selector(graph, color) -> int
  Returns the FIRST move of the best sequence found.
"""

from dp import simulate_move, boundary_options, get_flooded_size_sim

# ── tuneable limits ───────────────────────────────────────────────────────────
BT_MAX_DEPTH = 20   # hard cap: won't search deeper than this many moves
# ─────────────────────────────────────────────────────────────────────────────

bt_memo = {}        # maps (state_tuple, moves_used) → True  (visited guard)
best_result = {}    # shared mutable dict so recursion can update it easily


def is_solved(current_colors):
    """Board is solved when every cell has the same color as cell 0."""
    c = current_colors[0]
    return all(x == c for x in current_colors)


def greedy_order(graph, current_colors):
    """
    Return boundary colors sorted by how many boundary nodes each one has.
    Trying the 'biggest' color first helps find a good solution early,
    which tightens the pruning bound for later branches.
    """
    options = boundary_options(graph, current_colors)
    if not options:
        return []

    counts = {}
    start_color = current_colors[0]

    # BFS to find flooded region boundary
    queue = [0]
    visited = {0}
    while queue:
        u = queue.pop(0)
        for v in graph[u]:
            if v not in visited:
                if current_colors[v] == start_color:
                    visited.add(v)
                    queue.append(v)
                elif current_colors[v] in options:
                    counts[current_colors[v]] = counts.get(current_colors[v], 0) + 1

    # sort descending by boundary count
    return sorted(options, key=lambda c: counts.get(c, 0), reverse=True)


def bt_solve(graph, current_colors, moves_used, path):
    """
    Recursive backtracking search.

    Parameters
    ----------
    graph         : adjacency dict (unchanged throughout)
    current_colors: list of ints, current board state
    moves_used    : how many moves deep we currently are
    path          : list of color choices made so far (for reconstructing solution)
    """

    # ── pruning ───────────────────────────────────────────────────────────────
    # If we've already used as many (or more) moves than the best known solution,
    # this branch can NEVER improve on it → cut it.
    if moves_used >= best_result["best_moves"]:
        return

    # Hard depth cap to keep runtime acceptable
    if moves_used >= BT_MAX_DEPTH:
        return

    # ── visited guard ─────────────────────────────────────────────────────────
    state_key = (tuple(current_colors), moves_used)
    if state_key in bt_memo:
        return
    bt_memo[state_key] = True

    # ── base case: board solved ───────────────────────────────────────────────
    if is_solved(current_colors):
        # Found a solution that uses fewer moves than anything seen so far
        best_result["best_moves"] = moves_used
        best_result["best_path"]  = list(path)
        return

    # ── recursive step ────────────────────────────────────────────────────────
    for color_choice in greedy_order(graph, current_colors):
        next_state = simulate_move(graph, current_colors, color_choice)

        # Skip moves that don't actually expand the flooded region
        if next_state == current_colors:
            continue

        path.append(color_choice)
        bt_solve(graph, next_state, moves_used + 1, path)
        path.pop()


def backtracking_color_selector(graph, color) -> int:
    """
    Main entry point — mirrors dp_color_selector() interface.

    Returns the first color of the best (fewest-move) sequence found.
    Falls back to the greediest boundary color if no solution is found
    within BT_MAX_DEPTH.
    """
    global bt_memo, best_result

    # Reset shared state for each fresh call
    bt_memo = {}
    best_result = {
        "best_moves": BT_MAX_DEPTH + 1,   # anything better than this wins
        "best_path":  []
    }

    bt_solve(graph, list(color), 0, [])

    if best_result["best_path"]:
        return best_result["best_path"][0]   # first move of optimal sequence

    # Fallback: greedy (boundary color with most nodes)
    options = greedy_order(graph, color)
    return options[0] if options else 1