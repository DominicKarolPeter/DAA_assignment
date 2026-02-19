def div_n_conq(current) -> int:
    size = len(current)
    # Stopping conditions
    if size == 1:
        return {current[0]:1}

    # Recursive calls
    first = div_n_conq(current[:size//2])
    second = div_n_conq(current[size//2:])
    combined = {}
    for k, v in first.items():
        combined[k] = combined.get(k, 0) + v

    for k, v in second.items():
        combined[k] = combined.get(k, 0) + v
    return combined
