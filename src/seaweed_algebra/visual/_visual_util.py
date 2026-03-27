from itertools import chain, islice, tee

from matplotlib.colors import TABLEAU_COLORS

from seaweed_algebra.meander import Meander


def _get_edges(blocks: list[int]) -> list[tuple[int, int]]:
    """Converts a list of blocks into a list of connected vertex pairs."""
    edges = []
    start_offset = 0
    for block in blocks:
        size = block - 1
        arc_offset = 0
        while size >= 1:
            left = start_offset + arc_offset
            right = start_offset + arc_offset + size
            edges.append((left, right))
            size -= 2
            arc_offset += 1
        start_offset += block
    return edges


def generate_component_color_map(
    top_blocks: list[int], bottom_blocks: list[int]
) -> dict[int, str]:

    n = sum(top_blocks)
    # This dictionary will link a node to all other nodes connected with a path.
    adj_list = {i: [] for i in range(n)}

    # Calculates a list of (left, right) connected edges.
    top_edges = _get_edges(top_blocks)
    bottom_edges = _get_edges(bottom_blocks)

    # Add each connection to the list of adjacencies.
    for u, v in top_edges + bottom_edges:
        adj_list[u].append(v)
        adj_list[v].append(u)

    visited = set()
    all_loops = []

    # Depth first search to extract disjoint paths.
    for vertex in range(n):
        if vertex not in visited:
            # Create a new loop, starting with the current node
            current_loop = []
            stack = [vertex]
            while stack:
                # Get the current node
                node = stack.pop()
                if node not in visited:
                    # If we haven't seen this node yet, then it is part of this loop
                    # Mark it as visited, add it to the loop, and add its connected nodes to our stack.
                    visited.add(node)
                    current_loop.append(node)
                    stack.extend(adj_list[node])
            # Once we have emptied the stack, we have finished traversing the loop.
            all_loops.append(current_loop)

    # We want the loops sorted by the first node we come across (the minimum element in the loop).
    all_loops.sort(key=lambda loop: min(loop))

    # Inner loop nodes must also be sorted as the cycle algorithm below requires it.
    for loop in all_loops:
        loop = loop.sort()

    # Create a dictionary to map node indicies to a color.
    color_map = {}
    palette = list(TABLEAU_COLORS.values())

    # The number of cycles is defined by the number of component deletions.
    # ie. the length of the homotopy is how many cycles there are.
    num_cycles = len(Meander(top_blocks, bottom_blocks).homotopy())
    # Create an array which will hold arrays of nodes within each cycle.
    cycles = [[] for _ in range(num_cycles)]

    # Copy the all loops iterable.
    loops, next_loops = tee(all_loops, 2)
    # Create the next_loops iterable to be one element ahead of loops.
    # https://stackoverflow.com/a/1012089
    next_loops = chain(islice(next_loops, 1, None), [None])

    # Store the left and right points of edges so we can quickly determine if a node is an endpoint.
    left_top_edges = {edge[0] for edge in top_edges}
    left_btm_edges = {edge[0] for edge in bottom_edges}
    right_top_edges = {edge[1] for edge in top_edges}
    right_btm_edges = {edge[1] for edge in bottom_edges}

    cycle_idx = 0
    # Iterate over all the loops.
    for loop, next_loop in zip(loops, next_loops):
        # Add the current loop to the current cycle.
        cycles[cycle_idx] += loop
        # Check if there is another loop (ie. this loop isn't the last loop).
        if next_loop is not None:
            # Get the left, and right elements, i and j respectively, of this loop and the next loop.
            i, j = loop[0], loop[-1]
            i2, j2 = next_loop[0], next_loop[-1]

            # Is the next loop is nestled inside by 1 node?
            is_nested = (i + 1 == i2) and (j - 1 == j2)

            # Does the left side connect both a top and bottom edge?
            is_i_continuous = (i in left_top_edges) and (i in left_btm_edges)

            # Does the right side connect both a top and bottom edge?
            is_j_continuous = (j in right_top_edges) and (j in right_btm_edges)

            # If NOT nested, or if EITHER side is an endpoint, begin a new cycle.
            if not is_nested or not is_i_continuous or not is_j_continuous:
                cycle_idx += 1

    # Set a color for each cycle from the palette.
    for i, cycle in enumerate(cycles):
        current_color = palette[i % len(palette)]
        for node in cycle:
            color_map[node] = current_color

    return color_map
