# Week 18: Graphs and the fewest steps

## The pattern in five lines

1. A graph (places joined by links) is stored as an adjacency dict: each place maps to a list of the places it links to.
2. BFS (breadth-first search) visits places in order of their distance from the start: first every place one step away, then two steps, then three.
3. So the first time BFS reaches a place, it has used the fewest steps. Keep a `seen` set so no place goes in the queue twice.
4. Reach for it when every step costs the same and the question asks for the fewest steps, moves or changes.
5. BFS takes O(V + E) time and O(V) extra space, where V is the number of places and E the number of links.

## Problem A (warm-up, 10 minutes): Fewest hops for a rider

TiffinTrack splits Pune into delivery areas. The map lists, for each area, the areas that share a border with it. A hop is one move from an area to a neighbouring area. Find the fewest hops a rider needs from `start` to `end`.

```python
def fewest_hops(neighbours: dict[str, list[str]], start: str, end: str) -> int:
```

The examples use this map:

```python
pune = {
    "Kothrud": ["Deccan", "Warje"],
    "Warje": ["Kothrud"],
    "Deccan": ["Kothrud", "Shivajinagar", "Swargate"],
    "Shivajinagar": ["Deccan", "Aundh", "Koregaon Park"],
    "Aundh": ["Shivajinagar", "Baner", "Wakad"],
    "Baner": ["Aundh", "Hinjewadi"],
    "Hinjewadi": ["Baner", "Wakad"],
    "Wakad": ["Hinjewadi", "Aundh"],
    "Koregaon Park": ["Shivajinagar", "Viman Nagar", "Hadapsar"],
    "Viman Nagar": ["Koregaon Park"],
    "Hadapsar": ["Koregaon Park", "Swargate"],
    "Swargate": ["Deccan", "Hadapsar"],
    "Lohegaon": [],
}
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `fewest_hops(pune, "Kothrud", "Baner")` | `4` | Kothrud, Deccan, Shivajinagar, Aundh, Baner. |
| `fewest_hops(pune, "Deccan", "Hadapsar")` | `2` | Through Swargate. The route through Koregaon Park takes 3 hops. |
| `fewest_hops(pune, "Wakad", "Wakad")` | `0` | The rider is already there. |
| `fewest_hops(pune, "Baner", "Lohegaon")` | `-1` | No border joins Lohegaon to the other areas yet. |
| `fewest_hops({}, "Baner", "Aundh")` | `-1` | The map is empty. |

**Rules**

- `neighbours` has 0 to 10,000 areas. Each area lists 0 to 10 neighbours.
- Every border appears twice: when area A lists area B, area B also lists area A.
- An area that is not a key in `neighbours` has no neighbours.
- Return `0` when `start` equals `end`, even on an empty map.
- Return `-1` when no route joins `start` to `end`.
- Do not change `neighbours`.

## Problem B (main, 25 minutes): Fewest trains

RailSeat suggests journeys with as few train changes as possible. Each train has a number and a list of the stations where it stops. You can board or leave a train at any of its stops, in either direction. Find the fewest trains you must take from `start` to `end`.

```python
def fewest_trains(trains: dict[str, list[str]], start: str, end: str) -> int:
```

The examples use this network:

```python
network = {
    "91001": ["CSMT", "DR", "TNA", "KYN", "PUNE"],
    "91002": ["PUNE", "DD", "SUR"],
    "91003": ["KYN", "NK", "BSL"],
    "91004": ["BSL", "AK", "NGP"],
    "91005": ["BCT", "ST", "BRC", "ADI"],
}
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `fewest_trains(network, "CSMT", "PUNE")` | `1` | Train 91001 stops at both. |
| `fewest_trains(network, "TNA", "SUR")` | `2` | Take 91001 to PUNE, then 91002 to SUR. |
| `fewest_trains(network, "DR", "NGP")` | `3` | Take 91001 to KYN, 91003 to BSL, then 91004 to NGP. |
| `fewest_trains(network, "CSMT", "ADI")` | `-1` | No train joins the 91005 stations to the others. |
| `fewest_trains(network, "PUNE", "PUNE")` | `0` | You are already there. |
| `fewest_trains({}, "PUNE", "CSMT")` | `-1` | There are no trains. |

**Rules**

- `trains` has 0 to 500 trains. Each train has 2 to 100 stops, and no station appears twice on one train.
- Train numbers are 5-digit strings. Station codes are 1 to 5 capital letters.
- The answer counts trains, not stops. A journey with 2 trains has 1 change.
- Return `0` when `start` equals `end`.
- Return `-1` when no journey exists. An empty `trains` dict also returns `-1`.
- Do not change `trains`.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. What is one step in this graph, and what must you build before the BFS starts?
3. Which edge cases (unusual inputs, such as an empty map) could break your code? Name three.

## After the session

Change `fewest_hops` so that it returns the route itself, as a list of areas from `start` to `end`. Return `[]` when no route exists. Add two tests for your choice.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
