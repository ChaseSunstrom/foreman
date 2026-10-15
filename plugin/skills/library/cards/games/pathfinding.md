---
name: pathfinding
title: Pathfinding
area: games
tags: [pathfinding, astar, navmesh, grid, heuristic, steering]
detect: [dep:pathfinding, dep:easystarjs, dep:astar, dep:pathfinding-rs]
related: [game-loop, procedural-generation, game-physics]
---
Game pathfinding: A* on grids or navmeshes with an admissible heuristic, cached and budgeted per frame, tested for optimality and unreachable goals.

## Verify
- Run the project's test target (for example `pytest -q`, `cargo test` or `npm test`): path tests pass on fixed maps.
- `grep -rnE "sqrt|hypot" src/ai`: finds Euclidean distance in heuristics on 4-neighbour grids, which needs checking for admissibility.
- `grep -rnE "findPath|find_path" src`: lists callers, each of which must handle the no-path result.

## Test first
Use tiny hand-drawn maps with known optimal lengths.
```python
def test_path_goes_around_wall():
    g = Grid(["S.#.", "..#.", "...E"])
    p = find_path(g, g.start, g.end)
    assert p is not None and len(p) - 1 == 5

def test_unreachable_returns_none():
    g = Grid(["S#E"])
    assert find_path(g, g.start, g.end) is None

def test_heuristic_never_overestimates():
    assert manhattan((0, 0), (3, 4)) <= 7
```

## Do
- Pick the heuristic to match movement: Manhattan for 4-way, octile for 8-way, straight-line for free movement. Keep it admissible so A* stays optimal.
- Use a binary heap for the open set and a map from node to best g-cost. Skip stale heap entries instead of decreasing keys.
- Return an explicit "no path" (`None`, empty, or an error), and have every caller handle it.
- Spread long searches across frames with a node-expansion budget, and keep the best partial result.
- Cache paths by (start cell, goal cell) and invalidate on map change. For many agents to one goal, run one Dijkstra or flow field from the goal.
- Smooth the grid path afterward (line-of-sight shortcuts or string pulling on navmeshes), and keep the raw path for debugging.
- Weight terrain through edge costs, not by editing the heuristic.
- Handle diagonal moves by forbidding corner cutting through blocked neighbours.

## Avoid
- Euclidean heuristic on a 4-connected grid with unit costs: fine but weak, and weighted by more than 1 it becomes inadmissible. Use Manhattan.
- A heuristic multiplied by a large weight for speed without noting it: paths become suboptimal. Document the weight and test the bound.
- Scanning a list for the lowest f-cost: O(n^2) stalls. Use a heap.
- Recomputing every agent's path every frame: use a repath interval or react to blocked-node events.
- Mixing world and cell coordinates: off-by-half bugs. Convert at the boundary in one function.
- Treating moving agents as static walls in the search: use local avoidance on top of the path.

## Review
- [ ] Tests cover optimal length, detour, unreachable goal, and start equal to goal.
- [ ] The heuristic is admissible for the movement model.
- [ ] Callers handle the no-path result.
- [ ] Search work per frame is bounded and cached where repeated.
- [ ] Diagonal moves do not cut blocked corners.
