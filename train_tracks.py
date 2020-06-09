
"""Train Tracks.

State
-------

Positions are classified to the following.  

* `empty`(set): Position are assured that no track is placed on.
* `Part` (deque): a part of path. 
    - Except edges, tracks are placed and directions are determined. They are called `occupied`.   
    - For Edges, directions are not yet determined. 
* `reserved`(set): Positions where tracks are to be placed, but direction is not yet determined.
    - Edges of `Parts` are excluded from `reserved`. (These are included in `Part`).

* `unused`: states other than the above. 

Although the state of the board is represented by the above, 
for calculation efficiency, `self.occupied` and `self.pos_to_edgeinfo` are used inside `self.update`.


Relationship of positions
------------------------------------------------
* While updating state, we can classify the relationship of two positions (`pos1` and  `pos2`) into the following.  

Under the assumption `pos1` is not `occupied`: 

1. `pos2` is assured to be empty (in `self.empty`). 
2. `pos2` is unused.
3. `pos2` is reserved. 
4. `pos2` is occupied by Parts.
5. `pos2` is the edge of the other Part.
6. `pos2` is the edge of the same Part.(If `pos1` is the Edge of the Part).

This classification is reflected in such as `self._gen_cands` and 
used to construct `Candidate`.


Strategy of Updating States.
-----------------------------

* If available `Candidate` is unique, then it is applied.
* For a `reserved` position, which has only 2 connectable proximities, these connections should be fixed. 
* Referring to `rows` and `columns`, the places of `reserved` or `empty` are fixed. (`self._deduce_space_state`)
* For a `unused` space, which does not have available connection pattern, it is added to `empty`. (`self._fill_empty`) 
    - Referring to both of state of the connected positions and `rows` and `columns`.


Comment
----------------------------
* For me, this problem is very challenging, but very good practice!

* There were many bugs such that the variables of the loop changes inside of the loop unintentionally.  
    - I should take care of these from now on by either implementations or the design of logic itself.

* I feel keeping coherence of `state` variables is the key to write a program to solve this kind of puzzle.  

* This program may require `backtracking` for more various tests.


"""

from typing import Tuple, Dict, Set, List
import collections
from pprint import pprint
from dataclasses import dataclass
from collections import defaultdict
from itertools import combinations

Counts, Coords = List[int], Tuple[int, int]
MOVES = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}

from enum import IntEnum

class CandType(IntEnum):
    EDGE = 0  # Append to the edge of `Part`.
    UNUSED = 1  # Place a track in a non-reserved position.  
    RESERVED = 2 # Place a track in a reserved position.

class EdgeType(IntEnum):
    LEFT = 0 # Left Edge.
    RIGHT = -1  # Right Edge.

EDGES = [EdgeType.LEFT, EdgeType.RIGHT]

@dataclass
class Candidate:
    index: int  # Index of part.  
    edge: EdgeType # Edge
    pos: Tuple  # Position
    type: CandType  # Type of operation.
    r_index: EdgeType = None  # For CandType.EDGE
    r_edge: EdgeType = None  # For CandType.EDGE

 
class Part:
    def __init__(self, deque):
        self.deque = collections.deque(deque)
        self._elems = set(deque)  # For check of occupation.


    def __getitem__(self, key):
        """Notice that this operation is slow.
        """
        return self.deque[key]

    def __str__(self):
        return str(self.deque)

    def __repr__(self):
        return repr(self.deque)

    def __iter__(self):
        return iter(self.deque)

    def __len__(self):
        return len(self.deque)

    def merged(self, other):
        """Merge the two parts and create the new one.
        """
        assert self.is_intersected(other)
        n_wrapped = len((set(self.deque) & set(other.deque)))  
        reversed_map = [(s, o) for s in (False, True) for o in (False, True)]
        def to_content(path, flag):
            if flag:
                return list(reversed(path.deque))
            else:
                return list(path.deque)

        for s_flag, o_flag in reversed_map:
            s_content = to_content(self, s_flag)
            o_content = to_content(other, o_flag)
            if s_content[:n_wrapped] == o_content[-n_wrapped:]:
                n_deque = o_content[:-n_wrapped] + s_content
                return Part(n_deque)

        # May `self` is included in `other` or vice versa.
        p1, p2 = sorted((self, other), key=lambda p: len(p))
        for i, _ in enumerate(p2):
            if len(p2) < i + len(p1):
                break
            if list(p2)[i:i+len(p1)] == list(p1) or list(p2)[i:i+len(p1)] == list(reversed(p1)):
                return Part(p2)
        raise ValueError("Failed to merge of `deque`. ")
        
    def is_intersected(self, other):
        if (set(self.deque) & set(other.deque)):
            return True
        return False

    def append(self, pos):
        self.deque.append(pos)
        self._elems.add(pos)

    def appendleft(self, pos):
        self.deque.appendleft(pos)
        self._elems.add(pos)

    def concat(self, pos, edge):
        if edge == EdgeType.LEFT:
            self.appendleft(pos)
        elif edge == EdgeType.RIGHT:
            self.append(pos)
        else:
            raise RuntimeError("Bug.", edge)


class FailedError(Exception):
    pass


class State:
    def __init__(self, rows, columns, start, end, constraints):
        start = tuple(start)
        end = tuple(end)
        self.height = len(rows)
        self.width = len(columns)
        self.rows = rows
        self.columns = columns

        self.empty = set()  # Assured that nothing is placed.
        self.reserved = set() # Assured that track is placed. However, they are not regarded as elements of `Part`.

        # Initialize `Part` with Constraints.
        parts = list()
        for pos, chars in constraints.items():
            chars = list(chars)
            if tuple(pos) in {start, end}:
                if tuple(pos) == start:
                    s = "START"
                else:
                    s = "END"
                part = Part([s, pos, self._delta_char(pos, chars[0])])
            else:
                part = Part([self._delta_char(pos, chars[0]), pos, self._delta_char(pos, chars[1])])
            parts.append(part)

        # If constraints are connected with each other, 
        # in this point, `parts` does not represent the state correctly.
        # Here, modify this.
        while True:
            merge_target = { (i, j) for i, p1 in enumerate(parts) for j, p2 in enumerate(parts[i+1:], i+1) if p1.is_intersected(p2)}
            if not merge_target:
                break
            i, j = merge_target.pop()
            n_part = parts[i].merged(parts[j])
            parts = [part for k, part in enumerate(parts) if k not in {i, j}]
            parts.append(n_part)
        self.parts = parts

        # Based on `parts`. 
        # `rows` and `columns` are modified.
        for part in self.parts:
            for pos in part:
                if pos in {"START", "END"}:
                    continue
                r, c = pos
                self.rows[r] -= 1
                self.columns[c] -= 1
        # `self.pos_to_edgeinfo`  
        # `self.occupied` are initialized, following to `self.parts`.
        self._init_part_states()

        # Here, states of variables are coherent.

        # `empty` and `reserved` are initialized.
        self._deduce_space_state()

        #self.display()

    def _gen_proximities(self, pos):
        result = list()
        for char in MOVES.keys():
            try:
                result.append(self._delta_char(pos, char))
            except ValueError:
                pass
        return result


    def _gen_cands(self, p_index, edge):
        assert edge in EDGES

        cands = list()
        base_pos = self.parts[p_index][edge] 
        for pos in self._gen_proximities(base_pos):
            # Check for occupied..
            if pos in self.occupied:
                continue

            # Check for the EDGE position of the same `Part`.
            if pos == self.parts[p_index][EdgeType.LEFT]:
                continue
            if pos == self.parts[p_index][EdgeType.RIGHT]:
                continue

            # Check for EDGE position for other `Parts`.
            if pos in self.pos_to_edgeinfo:
                r_index, r_edge = self.pos_to_edgeinfo[pos]
                assert p_index != r_index 
                cand = Candidate(p_index, edge, pos, CandType.EDGE, r_index, r_edge)
                cands.append(cand)
                continue

            # Check of RESERVED position.
            if pos in self.reserved:
                cand = Candidate(p_index, edge, pos, CandType.RESERVED)
                cands.append(cand)
                continue
            else:
                # Check for UNUSED position.
                if pos not in self.empty:
                    cand = Candidate(p_index, edge, pos, CandType.UNUSED)
                    cands.append(cand)
                    continue
        return cands

    def _is_unused(self, r, c):
        return ((r, c) not in self.occupied ) and ((r, c) not in self.pos_to_edgeinfo) and ((r, c) not in self.empty) and ((r, c) not in self.reserved) 


    def _deduce_space_state(self):
        """Basically, this method must be called when tracks are put or `empty` / `reserved` are updated in other methods.
        Status of `empty` and `reserved` are updated.
        """

        def _gen_space_rows(r):
            return {(r, m) for m, _ in enumerate(self.columns) if self._is_unused(r, m)}

        def _gen_space_columns(c):
            return {(m, c) for m, _ in enumerate(self.rows) if self._is_unused(m, c)}

        while True:
            is_changed = False
            for y, _ in enumerate(self.rows):
                if self.rows[y] == 0:
                    target = _gen_space_rows(y)
                    if target:
                        self.empty |= target 
                        is_changed = True
            if is_changed:
                continue

            for x, _ in enumerate(self.columns):
                if self.columns[x] == 0:
                    target = _gen_space_columns(x)
                    if target:
                        self.empty |= target 
                        is_changed = True

            if is_changed:
                continue

            def _modify_numbers(y, x):
                self.rows[y] -= 1
                if self.rows[y] < 0:
                    raise FailedError()
                self.columns[x] -= 1
                if self.columns[x] < 0:
                    raise FailedError()
        
            for y, row in enumerate(self.rows):
                unused = _gen_space_rows(y)
                if row != 0 and len(unused) == row:
                    self.reserved |= unused
                    for y, x in unused:
                        _modify_numbers(y, x)
                    is_changed = True

            if is_changed:
                continue

            for x, column in enumerate(self.columns):
                unused = _gen_space_columns(x)
                if column != 0 and len(unused) == column:
                    self.reserved |= unused
                    for y, x in unused:
                        _modify_numbers(y, x)
                    is_changed = True

            if is_changed:
                continue

            if is_changed is False:
                break

    def _apply_candidate(self, cand):
        """Apply Candidate to this State.
        """
        #print("cand", cand)
        index = cand.index
        edge = cand.edge
        pos = cand.pos
        if cand.type == CandType.UNUSED:
            r, c = pos
            self.rows[r] -= 1
            self.columns[c] -= 1
            self.occupied.add(self.parts[index][edge])
            self.pos_to_edgeinfo[pos] = (index, edge)
            self.parts[index].concat(pos, edge)
        elif cand.type == CandType.RESERVED:
            self.occupied.add(self.parts[index][edge])
            self.pos_to_edgeinfo[pos] = (index, edge)
            self.parts[index].concat(pos, edge)
            self.reserved.remove(pos)

        elif cand.type == CandType.EDGE:
            part = self.parts[index]
            r_part = self.parts[cand.r_index]
            part.concat(pos, edge)
            n_part = part.merged(r_part)
            # Keep Coherence about `parts`.
            n_parts = [part for i, part in enumerate(self.parts) if i not in {index, cand.r_index}]
            n_parts += [n_part]
            self.parts = n_parts

            self._init_part_states()

        else:
            raise NotImplementedError("Bug.")

        self._deduce_space_state()

    def _init_part_states(self):
        """ Suppose that `self.parts` information is valid.
        It makes `self.occupied` and `self.pos_to_edgeinfo` reflects 
        states of `self.parts`.

        This method construct both of `self.occupied` and `self.pos_to_edge`,  
        If you apply `Candidate`, you do not have to reconstruct it from scratch.
        In these cases, partially update it.  

        Comment
        ----------------------------------------------------------------
        If I do not choose the structure which owns `p_index`, 
        then this mechanism can be revised better.
        """

        self.occupied = set()
        self.pos_to_edgeinfo = dict()
        for p_index, part in enumerate(self.parts):
            for i, pos in enumerate(part):
                if i == EdgeType.LEFT:
                    self.pos_to_edgeinfo[pos] = (p_index, EdgeType.LEFT)
                elif i == len(part) - 1:
                    self.pos_to_edgeinfo[pos] = (p_index, EdgeType.RIGHT)
                else:
                    self.occupied.add(pos)
            
    def update(self) -> bool:

        is_changed = False

        # Check the fixed `Candidate` around `Edge` of `Part`.
        for p_index, part in enumerate(self.parts):
            for edge in EDGES:
                if part[edge] in {"END", "START"}:
                    continue # End or Start
                cands = self._gen_cands(p_index, edge)
                if len(cands) == 0:
                    raise FailedError(part, p_index)
                elif len(cands) == 1:
                    cand = cands[0]
                    self._apply_candidate(cand)

                    is_changed = True
                    # self.display()

                    # In cand.type == CandType.EDGE,
                    # merge of `self.parts` occurs, so
                    # premises of the loop breaks. 
                    if cand.type ==  CandType.EDGE:
                        return is_changed
                    # Otherwise, it is possible to continue the processings.

        def _can_connect(p):
            if p in self.empty:
                return False
            if p in self.occupied:
                return False
            return True

        # Inside `for`, self.reserved is modified.
        # Hence, at the first of the loop, check whether
        # `pos` is staled or not.
        for pos in set(self.reserved):
            if pos not in self.reserved:
                continue

            targets = [p for p in self._gen_proximities(pos) if _can_connect(p)]
            assert 2 <= len(targets)
            if len(targets) == 2:
                # In this case, these two positions must be filled with track, 
                # since `entering` and `exiting` are fixed. 

                # Firstly, attempts to merge with existing `Part`.
                # If it is not the case, make the new `Part`.
                for target in targets:
                    if target in self.pos_to_edgeinfo:
                        index, edge = self.pos_to_edgeinfo[target]
                        cand = Candidate(index, edge, pos, CandType.RESERVED)
                        self._apply_candidate(cand)
                        break
                else:
                    # Making a New Part. 
                    part = Part([targets[0], pos, targets[-1]])
                    # Updating of State.
                    for (r, c) in part:
                        if (r, c) not in self.reserved:
                            self.rows[r] -= 1
                            self.columns[c] -= 1
                    self.reserved = self.reserved - set(part)
                    self.parts.append(part)
                    # Index of `Part` changes, so info about `Part` must be re-built.  
                    self._init_part_states()
                    self._deduce_space_state()
                is_changed = True

        # Confirm empty positions.
        if self._fill_empty():
            is_changed = True

        if is_changed is False:
            raise NotImplementedError("Under the assumption that codes are valid, it requires backtracking.")
        return is_changed


    def _fill_empty(self):
        """Based on the current situations, 
        if there are positions which are to be `empty`, do them.
        """

        is_changed = False
        focuses = [(r, c) for r, row in enumerate(self.rows) for c, column in enumerate(self.columns)
                  if self._is_unused(r, c)]


        #import pdb; pdb.set_trace()


        # Inside Loop, result of `unused` changes,  
        # Hence, re-check of (r, c) is required.
        for r, c in focuses:
            if not self._is_unused(r, c):
                continue

            # Enumerate possible candidates.
            # If no combination of candidates are possible, then `(r, c)` is empty.
            #
            proxs = self._gen_proximities((r, c))
            elems = list()

            # `I` means the increment of tracks.
            # If the increment of tracks contradicts with `rows` and `columns`, 
            # it is impossible to place.
            Z = 0
            I = 1
            for prox in proxs:
                if prox in self.pos_to_edgeinfo:
                    elems.append((prox, Z))  # (Position, Increment of Track).
                elif prox in self.occupied:
                    continue
                elif prox in self.reserved:
                    elems.append((prox, Z))
                    continue
                else:
                    if prox not in self.empty:
                        elems.append((prox, I))
                    continue
 
            # In the first place, if there are not 2 connectable positions at least, 
            # it must be empty. 
            groups = list(combinations(elems, 2))
            if not groups:
                self.empty.add((r, c))
                self._deduce_space_state()
                is_changed = True

            # If all the possible candidates
            # contradicts against `rows` or `columns`,  
            # they cannot be applied.
            is_possible = True
            for group in groups:
                ((r1, c1), n1), ((r2, c2), n2) = group
                d_row, d_column = defaultdict(int), defaultdict(int)
                for ((re, ce), ne) in [*group, ((r, c), I)]:
                    d_row[re] += ne
                    d_column[ce] += ne
                
                ok_group = True
                for dr, v in d_row.items():
                    if self.rows[dr] < v:
                        ok_group = False
                for dc, v in d_column.items():
                    if self.columns[dc] < v:
                        ok_group = False
                if ok_group is True:
                    is_possible = True
                    break
            else:
                is_possible = False

            if is_possible is False:
                self.empty.add((r, c))
                self._deduce_space_state()
                is_changed = True
        return is_changed


    def _delta_char(self, pos, char):
        mv = MOVES[char]
        n_pos = (pos[0] + mv[0], pos[1] + mv[1])
        if (0 <= n_pos[0] < self.height) and (0 <= n_pos[1] < self.width):
            return n_pos
        else:
            raise ValueError()

    def is_completed(self):
        return len(self.parts) == 1 and {self.parts[0][0], self.parts[0][-1]} ==  {"START", "END"}


    def display(self):
        """ Display the states. 
        For large problems, `display`'s layout collapsed.  
        """

        chars = [[None] * (len(self.columns) + 1) for _ in range(len(self.rows) + 1)]
        chars[0][0] = "#"
        for i in range(1, len(self.columns) + 1):
            chars[0][i] = str(self.columns[i - 1])[0]
        for i in range(1, len(self.rows) + 1):
            chars[i][0] = str(self.rows[i - 1])[0]

        for y in range(1, len(self.rows) + 1):
            for x in range(1, len(self.columns) + 1):
                chars[y][x] = " "

        for i, part in enumerate(self.parts):
            c = chr(i + 65)
            for i, pos in enumerate(part):
                if pos not in {"START", "END"}:
                    y, x = pos  
                    if i == 0 or i == len(part) - 1:
                        t = c
                    else:
                        t = c.lower()
                    chars[y + 1][x + 1] = t

        for (y, x) in self.empty:
            chars[y + 1][x + 1] = "X"

        for (y, x) in self.reserved:
            chars[y + 1][x + 1] = "R"

        s = "\n".join(map(lambda elems: "".join(elems), chars))
        print(s)

        #for part in self.parts:
        #    print(part)
        
 
def to_moves(state, start):
    d_to_char = {v: k for k, v in MOVES.items()}
    deque = state.parts[0]
    if list(deque[1]) != list(start):
        deque = collections.deque(reversed(deque))
    else:
        deque = collections.deque(deque)
    assert list(deque[1]) == list(start)

    deque.popleft() is None
    prev = deque.popleft() 
    result = list()
    while True:
        c = deque.popleft()
        if c == "END":
            break
        d = (c[0] - prev[0], c[1] - prev[1]) 
        char = d_to_char[d]
        result.append(char)
        prev = c
    return "".join(result)


def train_tracks(rows: Counts, columns: Counts,
                 start: Coords, end: Coords,
                 constraints: Dict[Coords, Set[str]]) -> str:
    state = State(rows, columns, start, end, constraints)
    while not state.is_completed():
        flag = state.update()
        #state.display()
        #import pdb; pdb.set_trace()
    #state.display()
    result = to_moves(state, start)
    return result

