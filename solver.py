"""
This module can be used to solve instances of the water bucket puzzle, also
frequently known as the Die Hard puzzle from the movie it was popularized in
(see https://mindyourdecisions.com/blog/2013/02/04/the-water-jug-riddle/).
"""
import itertools

class State(object):
    """
    Represents a state of the water bucket puzzle, that would make up a single
    node in the search tree.

    Attributes:
        values: a tuple of integers, representing the amount of water stored
            in each bucket
        constraints: a tuple of integers, representing the maximum amount of
            water that can be stored in each bucket
        target: the integer value, which is the target amount of water to
            end up with in a single bucket
        allow_refills: whether or not buckets can be refilled to their
            respective capacities
    """
    def __init__(self, values, constraints, target, allow_refills=True):
        self.values = values
        self.constraints = constraints
        self.target = target
        self.allow_refills = allow_refills

    @staticmethod
    def _replace(values, index, new_val):
        return values[:index] + (new_val,) + values[index+1:]

    def get_neighbors(self):
        """
        Returns all of the state's neighbors.

        The state's neighbors are all of the positions by obtained by a single
        move, i.e. filling a bucket completely, emptying a bucket completely,
        or pouring water from one bucket into the other as much as possible.
        """

        neighbors = set()
        # first, try emptying buckets and filling buckets
        for i, val in enumerate(self.values):
            if val != 0:
                neighbors.add(self._replace(self.values, i, 0))
            if val != self.constraints[i] and self.allow_refills:
                neighbors.add(self._replace(self.values, i, self.constraints[i]))

        # try pouring non-empty buckets (i) into other buckets (j)
        for i, val_i in enumerate(self.values):
            if val_i != 0:
                for j, val_j in enumerate(self.values):
                    if i != j:
                        space_left = self.constraints[j] - val_j
                        if space_left >= 0:
                            moving = min(val_i, space_left)
                            new_values = self._replace(
                                self.values, j, val_j + moving)
                            new_values = self._replace(
                                new_values, i, val_i - moving)
                            neighbors.add(new_values)

        return [State(n, self.constraints, self.target,
                      allow_refills=self.allow_refills) for n in neighbors]

    def is_goal(self):
        """
        Return true if one of the bucket contains the target amount.
        """
        return any([val == self.target for val in self.values])

    def __eq__(self, other):
        return self.values == other.values

    def __hash__(self):
        return hash(self.values)

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        if self.allow_refills:
            return 'State({}, {}, {})'.format(
                repr(self.values), repr(self.constraints),
                repr(self.target))
        return 'State({}, {}, {}, allow_refills={})'.format(
            repr(self.values), repr(self.constraints),
            repr(self.target), repr(self.allow_refills))


def breadth_first_search(initial_state):
    """
    Performs BFS on an initial_state object.

    Generalized BFS works on any object given that it supports
    the methods "is_goal" and "get_neighbors".

    Returns an empty list if there is no way to get to the goal node.

    The explored variable technically keeps track of all nodes that have been
    seen, not necessarily opened up, so the name is slightly misleading...
    but explored is the more canonical term and it serves the same-ish purpose.
    """
    explored = {initial_state: ()}
    queue = [initial_state]
    while queue:
        state = queue.pop(0)  # O(queue) time ~ O(nodes in tree)
        if state.is_goal():
            return unravel_bfs(state, explored)
        for i in state.get_neighbors():
            if i not in explored:
                explored[i] = state
                queue.append(i)
    return []


def unravel_bfs(state, explored):
    """
    Given a state and a dictionary from each node to its previous node, return
    a list of the traversal needed to get to the state.
    """
    path = [state]
    while path[-1] in explored:
        path.append(explored[path[-1]])
    return list(reversed(path))


def argmax(domain, function):
    """
    Given a collection of values and a function, return the value which yields
    the greatest output (based on the > operator).
    """
    if not domain:
        raise IndexError('domain is empty:', domain)
    arg = domain[0]
    max_func_val = function(domain[0])
    for i in domain:
        val = function(i)
        if val > max_func_val:
            max_func_val = val
            arg = i
    return arg


def puzzle_difficulty(state):
    """
    Returns the number of moves to solve a puzzle.
    """
    return len(breadth_first_search(state))


def pretty_print(backtrace):
    """
    Prints out the backtrace from a BFS without less verbosity.
    """
    print(list(map(lambda state: state.values if state else (), backtrace)))


if __name__ == '__main__':
    print('Example: two buckets of capacity 5 and 3, with a target goal of 4.')
    problem = State((0, 0), (5, 3), 4)
    pretty_print(breadth_first_search(problem))

    print('\nExample: three buckets of capacity 10, 7, and 4, with a target goal of 2.')
    problem = State((10, 0, 0), (10, 7, 4), 2, allow_refills=False)
    pretty_print(breadth_first_search(problem))

    print('\nExample: three buckets of capacity 8, 5, and 3, with a target goal of 4.')
    problem = State((8, 0, 0), (8, 5, 3), 4, allow_refills=False)
    pretty_print(breadth_first_search(problem))

    print('\nExample: three buckets of capacity 12, 8, and 5, with a target goal of 2.')
    problem = State((12, 0, 0), (12, 8, 5), 2, allow_refills=False)
    pretty_print(breadth_first_search(problem))

    print('\nExample: two buckets of size at most 10 with the deepest search tree.')
    puzzle_constraints = itertools.product(range(11), repeat=3)
    puzzles = [State((0, 0), c[:2], c[2]) for c in puzzle_constraints]
    hardest = argmax(puzzles, puzzle_difficulty)
    print(repr(hardest))
    pretty_print(breadth_first_search(hardest))
