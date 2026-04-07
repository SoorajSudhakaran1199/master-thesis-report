import math
 
def generate_candidates(length_m, width_m, step_m):
    return [
        (x, y)
        for x in frange(-length_m/2, length_m/2, step_m)
        for y in frange(-width_m/2, width_m/2, step_m)
    ]
 
 
def is_valid(point, length_m, width_m, min_edge_clear_m, holes, hole_buffer_m):
    x, y = point
 
    # Edge clearance check
    if abs(x) > length_m/2 - min_edge_clear_m:
        return False
    if abs(y) > width_m/2 - min_edge_clear_m:
        return False
 
    # Hole avoidance check
    for h in holes:
        if math.hypot(x - h["x"], y - h["y"]) < h["radius"] + hole_buffer_m:
            return False
 
    return True
 
 
def select_best(candidates):
    return max(candidates, key=lambda p: -(abs(p[0]) + abs(p[1])))
