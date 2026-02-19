def greedy_color_selector(graph, color, C=6) -> int:
    """
    Docstring for greedy_color_selector

    :param graph: The current graph state. It is a dictionary representing the adjacency list.
    :param color: The current color of each node. It is a list
    :return: The color that maximizes the connected region size when selected. TYPE IS INTEGER.
    
    This function should implement a greedy algorithm to select the next color to maximize the size of the connected region
    starting from the top-left corner. It should analyze the current grid and return the color that would result in the largest
    expansion of the connected region.
    """
    n = len(color)
    start_color = color[0]

    flooded = [False] * n
    boundary = set()

    # Step 1: Find current flooded region (BFS)
    queue = [0]
    flooded[0] = True

    while queue:
        u = queue.pop(0)
        for v in graph[u]:
            if not flooded[v] and color[v] == start_color:
                flooded[v] = True
                queue.append(v)

    # Step 2: Build boundary
    for u in range(n):
        if flooded[u]:
            for v in graph[u]:
                if not flooded[v]:
                    boundary.add(v)

    # Step 3: Count colors on boundary
    colorCount = [0] * (C + 1)
    for v in boundary:
        colorCount[color[v]] += 1

    # Step 4: Create (count, color) pairs
    colorPairs = []
    for c in range(1, C + 1):
        if c != start_color:
            colorPairs.append([colorCount[c], c])

    # Step 5: INSERTION SORT (descending by count)
    for i in range(1, len(colorPairs)):
        key = colorPairs[i]
        j = i - 1

        while j >= 0 and colorPairs[j][0] < key[0]:
            colorPairs[j + 1] = colorPairs[j]
            j -= 1

        colorPairs[j + 1] = key

    # Step 6: Return best color
    return colorPairs[0][1]
