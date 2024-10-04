def no_heuristic(state):
    '''
        This function uses no computation at all and just returns 0 (Dijkstra's algorithm)

        Returns:
            (int) : a zero.
    '''
    return 0

def wagdy_heuristic(state):
    '''
        For each succesive pair of balls that are not the same color, add an estimated cost of 2

        Returns:
            f (int) : the heuristic's value.
    '''
    cost = 0
    tubes = state.to_list()
    for tube in tubes:
        for i in range(len(tube) - 1):
            if tube[i] != tube[i + 1]:
                cost += 2
    return cost

def repeated_color_heuristic(state):
    '''
        For each ball that is not the same color of the most repeated color in a tube, add an estimated cost of 1.

        Returns:
            f (int) : the heuristic's value.
    '''
    cost = 0
    tubes = state.to_list()
    for tube in tubes:
        if len(tube) > 0:
            repeated = max(set(tube), key = tube.count)
            not_repeated = len(tube) - tube.count(repeated)
            cost += not_repeated
    return cost