
from collections import Counter
from itertools import groupby

from typing import List, Optional, Set, Tuple
ImmutableGrid = Tuple[str, ...]
MutableGrid = List[List[str]]

SWAP = {'W': 'B', 'B': 'W'}

def update(grid: MutableGrid, i: int, j: int, impossible_value: str) -> bool:
    """
    Use this when you know `impossible_value` can not be at `position`.
    Update the grid IN-PLACE. Say if the grid really changed.
    """
    change = grid[i][j] == '.'
    grid[i][j] = SWAP[impossible_value]
    return change

def apply_rule(grid: MutableGrid) -> int:
    """
    Apply the rule on all empty cells:
    'WW.' -> 'WWB' (in four directions)
    'W.W' -> 'WBW' (in two directions)
    """
    changes = 0
    nb_rows, nb_cols = len(grid), len(grid[0])
    empty_cells = ((i, j) for i, row in enumerate(grid)
                   for j, cell in enumerate(row) if cell == '.')
    for i, j in empty_cells:
        #   1
        #   1
        # 33.44
        #   2
        #   2
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if 0 <= i + 2 * di < nb_rows and 0 <= j + 2 * dj < nb_cols:
                if grid[i + di][j + dj] == grid[i + 2 * di][j + 2 * dj] != '.':
                    changes += update(grid, i, j, grid[i + di][j + dj])
        #  2
        # 1.1
        #  2
        for di, dj in ((0, 1), (1, 0)):
            if di <= i < nb_rows - di and dj <= j < nb_cols - dj:
                if grid[i - di][j - dj] == grid[i + di][j + dj] != '.':
                    changes += update(grid, i, j, grid[i + di][j + dj])
    return changes

def reasoning(line: List[str], item: str) -> Optional[Set[int]]:
    """
    A line with only one 'B' to put in the line.
    If there is a possible 'WWW', then 'B' must avoid it.
    In this case, we can reduce possibilities where 'B' can be.
    Same reasoning swapping 'B' and 'W'.
    """
    for not_item, _group in groupby(enumerate(line),
                                    key=lambda x: x[1] != item):
        group = list(_group)
        if not_item and len(group) >= 3:
            # len(group) <= 5 because a group of length 6 with one B? Then WWW!
            if len(group) > 3:
                # Eliminate places where we can not put the item in group.
                # '..W.' with only one 'B', we can deduce some 'W':
                # 'W.WW' ('BWWW' or 'WWWB' otherwise)
                # [(1,'.'),(2,'.'),(3,'W'),(4,'.')], 'B') -> [(2,'.'),(3,'W')]
                group = group[-3: 3]
            return {i for i, _ in group}  # Only keep indexes.
    # No big group to reason with so `item` can be anywhere in the `line`.

def partly_complete_line(grid: MutableGrid) -> int:
    """
    Complete a line: 'BWWB.W' -> 'BWWBBW' ; 'BBWB..' -> 'BBWB..'.
    Deduction: no remaining 'B' then all are 'W'.
    Deduction in a part of a line: '..W.' with only one 'B' -> 'WBWW'.
    """
    changes = 0
    for _type in ('row', 'column'):
        lines = grid if _type == 'row' else zip(*grid)
        for n, line in enumerate(lines):
            d = Counter(line)
            if not d['.']:
                continue
            remains = {item: len(line) // 2 - d[item] for item in 'WB'}
            for item in 'WB':
                if remains[item] >= 2:
                    continue
                empty_cells = {k for k, elem in enumerate(line) if elem == '.'}
                # if not remains[item] then all empty can not be `item`.
                if remains[item]:  # == 1
                    # Nearly all empty can not be `item`.
                    can_be_item = reasoning(line, item)
                    if can_be_item is None:  # Sadly, `item` can be anywhere.
                        continue
                    empty_cells -= can_be_item
                changes += sum(
                    update(grid, *((n, k) if _type == 'row' else (k, n)), item)
                    for k in empty_cells)
    return changes

def unruly(grid: ImmutableGrid) -> ImmutableGrid:
    """
    Complete the grid only by applying the rule and a reasoning on the lines.
    """
    my_grid: MutableGrid = [list(row) for row in grid]
    for _ in range(2):  # Only to solve faster.
        apply_rule(my_grid)
    while partly_complete_line(my_grid) + apply_rule(my_grid):
        pass
    # No warranty it is entirely solved, but it is.
    return tuple(''.join(row) for row in my_grid)
