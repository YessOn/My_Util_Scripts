
ACTION = ("L", "R", "F")
CHERRY = 'C'
TREE = 'T'
SNAKE_HEAD = '0'
SNAKE = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
EMPTY = "."
SIZE = 10


def snake(field_map):
    cherrys = []
    snake = {}
    for i, row in enumerate(field_map):
        for j, ch in enumerate(row):
            if ch in SNAKE:
                snake[ch] = (i, j)
            if ch == CHERRY:
                cherrys.append((i, j))

    def route_search(start, goal):
        dist = 1
        find_target = False
        next_cells = [goal]
        guide_map = [['X' for _ in range(SIZE)] for _ in range(SIZE)]
        guide_map[goal[0]][goal[1]] = 0

        while next_cells or not find_target:
            search_cells = next_cells[:]
            next_cells = []
            for p in search_cells:
                py, px = p[0], p[1]
                for sp in [(py - 1, px), (py + 1, px), (py, px + 1), (py, px - 1)]:
                    sy, sx = sp[0], sp[1]
                    if 0 <= sy < SIZE and 0 <= sx < SIZE:
                        if (sy, sx) == start:
                            find_target = True
                            break
                        ch = field_map[sy][sx]
                        if ch == TREE:
                            continue
                        if ch in SNAKE:
                            if int(ch) < len(snake) - 1:
                                continue
                        if guide_map[sy][sx] != 'X':
                            continue
                        guide_map[sy][sx] = dist
                        next_cells.append((sy, sx))
                if find_target:
                    break
            dist += 1
        return guide_map, dist

    guide_map1, dist1 = route_search(snake['0'], cherrys[0])
    guide_map2, dist2 = route_search(snake['0'], cherrys[1])
    guide_map = guide_map1 if dist1 < dist2 else guide_map2

    def dir_evaluate(prev, cur, next):
        py, px = prev
        cy, cx = cur
        y_def, x_def = cy - py, cx - px
        dir_dic = {}
        n, w, e, s = (cy - 1, cx), (cy, cx - 1), (cy, cx + 1), (cy + 1, cx)
        if y_def == -1:
            dir_dic = {n: 'F', e: 'R', w: 'L'}
        elif y_def == 1:
            dir_dic = {s: 'F', w: 'R', e: 'L'}
        elif x_def == -1:
            dir_dic = {w: 'F', n: 'R', s: 'L'}
        elif x_def == 1:
            dir_dic = {e: 'F', s: 'R', n: 'L'}

        return dir_dic[next]

    min_dist = 99
    steps = ''
    cur_cell = snake['0']
    prev_cell = snake['1']
    next_cell = ()
    while min_dist > 0:
        dr = ''
        cy, cx = cur_cell
        for np in [(cy - 1, cx), (cy + 1, cx), (cy, cx + 1), (cy, cx - 1)]:
            ny, nx = np
            if 0 <= ny < SIZE and 0 <= nx < SIZE:
                num = guide_map[ny][nx]
                if num != 'X' and num < min_dist:
                    next_cell = (ny, nx)
                    min_dist = num
                    dr = dir_evaluate(prev_cell, cur_cell, next_cell)
        prev_cell = cur_cell
        cur_cell = next_cell
        steps += dr

    return steps
##################


class Node:
    "mixin class for A*"
    heuristic = lambda self, goal: 0 #must be monotonic
    def astar(self, goal):
        cl, op, parent, kls = set(), {self}, {}, type(self)
        g, f = {self: 0}, {self: self.heuristic(goal)}
        while op:
            t = min(op, key=f.get)
            op.remove(t)
            if t == goal:
                path = []
                while t is not self:
                    t, way = parent[t]
                    path.append(way)
                path.reverse()
                return path
            cl.add(t)
            for u, way, dist in t.neighbors():
                if u not in cl:
                    gu = g[t] + dist
                    if u not in op or gu < g[u]:
                        parent[u] = t, way
                        g[u] = gu
                        f[u] = gu + u.heuristic(goal)
                        op.add(u)

def checkio(field_map):
    class Cell(Node, tuple):
        def neighbors(self):
            pos, to = self
            t = field.get(pos, "X")
            if t == "C": yield Cell((pos, 0)), "", 0
            if t in ".0":
                for l, n in dict(F=to, L=to*1j, R=to/1j).items():
                    yield Cell((pos + n, n)), l, 1
    field = {}
    for i, row in enumerate(field_map):
        for j, t in enumerate(row):
            z = j - i*1j
            if t != "T": field[z] = t
            if t == "C": cherry = z
            if t == "0": head = z
            if t == "1": neck = z
    return ''.join(Cell((head, head - neck)).astar(Cell((cherry, 0))))
###########################

from heapq import heappop, heappush

CHERRY, TREE, EMPTY = "CT."
MOVES = {'F': ((1, 0), (0, 1)), 'L': ((0, -1), (1, 0)), 'R': ((0, 1), (-1, 0))}

sum_coords         = lambda xA, yA, xB, yB: (xA + xB, yA + yB)
vector             = lambda xA, yA, xB, yB: (xB - xA, yB - yA)
manhattan_distance = lambda xA, yA, xB, yB: abs(xB - xA) + abs(yB - yA)
dot_product        = lambda xA, yA, xB, yB: xA * xB + yA * yB

def snake(field_map) -> str:
    """ Find a path to cherry for the snake without being stuck later. """
    field_map, initial_snake, cherry = clean_input(field_map)
    def heuristic(path, snake) -> int:
        """ Rough estimate of the full path length to cherry. """
        return len(path) + manhattan_distance(*cherry, *snake[0])
    nb_rows, nb_cols = len(field_map), len(field_map[0]) # 10, 10 here...
    possible = lambda i, j: (0 <= i < nb_rows and 0 <= j < nb_cols
                             and field_map[i][j] == EMPTY)
    def move(path, snake):
        """ Generate new paths & snakes for possible actions. """
        for action, vects in MOVES.items():
            head, body = snake[:2]
            direction = vector(*body, *head)
            new_direction = (dot_product(*direction, *vect) for vect in vects)
            new_head = sum_coords(*head, *new_direction)
            if possible(*new_head):
                new_body = snake if new_head == cherry else snake[:-1]
                if new_head not in new_body:
                    yield path + [action], [new_head] + new_body
    def not_stuck(snake) -> bool: # probably can be improved.
        if len(snake) > 10:
            return True # We found the last cherry so we can't be stuck!
        queue, visited = [snake[0]], set() # simple BFS from snake head.
        while queue:
            i, j = queue.pop(0)
            visited.add((i, j))
            if len(visited) > len(snake):
                return True # enough place to not be stuck...
            for new in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                if possible(*new) and new not in snake and new not in visited:
                    queue.append(new)
    # Priority queue minimizing the length of paths, thanks to the heuristic.
    pq_item = lambda *item: (heuristic(*item), item)
    queue = [pq_item([], initial_snake)]
    while queue:
        for new_path, new_snake in move(*heappop(queue)[1]):
            if new_snake[0] == cherry and not_stuck(new_snake):
                return ''.join(new_path)
            heappush(queue, pq_item(new_path, new_snake))

def clean_input(field_map):
    """ Return a clean field, the snake list, and cherry position. """
    field_map = list(map(list, field_map))
    # Find snake and cherry items.
    items = {cell: (i, j) for i, row in enumerate(field_map)
                          for j, cell in enumerate(row)
                          if cell not in (EMPTY, TREE)}
    snake = [items[n] for n in sorted(filter(str.isdigit, items))]
    for i, j in items.values():
        field_map[i][j] = EMPTY
    return tuple(map(''.join, field_map)), snake, items[CHERRY]
