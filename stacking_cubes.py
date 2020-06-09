from functools import lru_cache
from collections import defaultdict, Counter


def stacking_cubes(cubes):
    cubes = list(map(tuple, cubes))
    merged_cubes = []
    for k, v in Counter(cubes).items():
        x, y, h = k
        if h == 1:
            merged_cubes.append((x, y, h, h * v))
        else:
            for _ in range(v):
                merged_cubes.append((x, y, h, h))
    cubes = merged_cubes

    def is_stack(cube_1, cube_2):
        x1, y1, e1, _ = cube_1
        x2, y2, e2, _ = cube_2
        return (x2 <= x1 < x2 + e2 or x1 <= x2 < x1 + e1) and (y2 <= y1 < y2 + e2 or y1 <= y2 < y1 + e1)

    @lru_cache()
    def height(st):
        return sum(s[3] for s in st)

    def search(rest, stack):
        if not rest:
            return stack

        last = stack and stack[-1]

        max_stack = tuple(stack)

        for i, cube in enumerate(rest):
            if not last or is_stack(cube, last):
                rs = search(rest[:i] + rest[i + 1:], stack + [cube])

                if height(rs) > height(max_stack):
                    max_stack = rs

        return tuple(max_stack)

    result = search(cubes, [])
    return height(tuple(result))

stacking_cubes([[-2,-1,3],[-1,0,2]])