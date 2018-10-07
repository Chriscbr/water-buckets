# Water Bucket Puzzle Solver

A simple Python class for solving the water bucket puzzle. In this puzzle,
you are given a number of buckets that can hold different quantities of
water, and the goal is to reach a target amount given that you can only fill
and pour out of buckets in exact amounts, i.e. without guessing. So with two
buckets that hold 5 liters and 3 liters respectively, you could fill the
5-bucket completely, then fill the 3-bucket using the 5-bucket so that 2
liters remain in the 5 bucket, and then perhaps empty the 3-bucket, and
so on.

This problem is simple and fun to explain to other people, although solving
it is usually just a matter of experimentation to see what kinds of new values
you can reach. Translating this into code, this means simply using breadth
first search (although other types of tree searching, like depth first search,
will also produce reasonable answers).

I use this approach to solve several example problems, such as one based
on the example above, where the buckets begin empty, have capacities 5 and 3,
and the target value is 4:

```python
problem = State((0, 0), (5, 3), 4)
pretty_print(breadth_first_search(problem))
```

outputs:

```
[(), (0, 0), (5, 0), (2, 3), (2, 0), (0, 2), (5, 2), (4, 3)]
```

The class allows for puzzles that don't involve refilling, by adding
`allow_refills=False` to the State constructor.

Intrestingly, I was also able to use this to find that the puzzle
with the longest solution (given I cap the buckets at 10 liter capacities)
is a puzzle with 10 and 9 capacity buckets and a target of 5. Adding more
buckets doesn't tend to make the puzzles longer to solve, which makes
intuitive sense since they effectively just give the person pouring water
between buckets more working space.
