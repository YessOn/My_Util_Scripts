from typing import List, Tuple

def isvalid(p1, p2):
    return all([(min(p1[i] + p1[2], p2[i] + p2[2]) - max(p1[i], p2[i])) > 0 for i in range(2)])

def stacking_cubes(cubes: List[Tuple[int, int, int]], current=None) -> int:
    valid = {idx: item for idx, item in enumerate(cubes) if current is None or isvalid(current, item)}
    return 0 if not valid else max(
        [valid[idx][2] + stacking_cubes(cubes[:idx] + cubes[idx + 1:], valid[idx]) for idx in valid])