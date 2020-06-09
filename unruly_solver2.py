
def is_correct(line, pos, value):
    line[pos] = value
    stack, half = [(0, '')],  len(line) // 2
    while stack:
        pos, current = stack.pop()
        if current[-3:] in {'WWW', 'BBB'} or \
           any(current.count(x) > half for x in 'WB'):
            continue
        if pos == len(line):
            return True
        cases = line[pos] if line[pos] in 'WB' else 'WB'
        stack += [(pos+1, current+x) for x in cases]

def unruly(grid):
    from itertools import product
    grid, dots = list(map(list, grid)), ''.join(grid).count('.')
    while dots:
        for _ in range(4):  # rotate 4 times
            grid = [list(x) for x in zip(*grid)]
            height, width = len(grid), len(grid[0])
            for x, y in product(range(height), range(width)):
                if grid[x][y] == '.':
                    if not is_correct(list(grid[x]), y, 'W'):
                        grid[x][y], dots = 'B', dots - 1
                    if not is_correct(list(grid[x]), y, 'B'):
                        grid[x][y], dots = 'W', dots - 1
    return [''.join(line) for line in grid]