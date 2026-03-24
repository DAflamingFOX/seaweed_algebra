import math

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
    adj_list = {i: [] for i in range(n)}

    top_edges = _get_edges(top_blocks)
    bottom_edges = _get_edges(bottom_blocks)

    for u, v in top_edges + bottom_edges:
        adj_list[u].append(v)
        adj_list[v].append(u)

    visited = set()
    all_loops = []

    # DFS to extract disjoint paths.
    for vertex in range(n):
        if vertex not in visited:
            current_loop = []
            stack = [vertex]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    current_loop.append(node)
                    stack.extend(adj_list[node])
            all_loops.append(current_loop)

    # Sort the loops by the minimum vertex.
    all_loops.sort(key=lambda loop: min(loop))

    color_map = {}
    palette = list(TABLEAU_COLORS.values())
    color_idx = 0
    loop_idx = 0

    homotopy = reversed(Meander(top_blocks, bottom_blocks).homotopy())

    for component in homotopy:
        current_color = palette[color_idx % len(palette)]

        # A component of size c consists of ceil(c/2) parallel paths
        paths = math.ceil(component / 2)

        for _ in range(paths):
            if loop_idx < len(all_loops):
                # Assign this entire loop to the current color
                for vertex in all_loops[loop_idx]:
                    color_map[vertex] = current_color
                loop_idx += 1

        color_idx += 1

    return color_map
