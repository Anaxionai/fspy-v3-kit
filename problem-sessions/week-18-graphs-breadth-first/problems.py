"""Week 18 problem session: graphs and the fewest steps.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def fewest_hops(neighbours: dict[str, list[str]], start: str, end: str) -> int:
    """Return the fewest hops a rider needs from `start` to `end`.

    `neighbours` maps each Pune delivery area to the areas that share a
    border with it. A hop is one move to a neighbouring area. An area that is
    not a key in `neighbours` has no neighbours.

    Return 0 when `start` equals `end`. Return -1 when no route exists.
    Do not change `neighbours`.
    """
    raise NotImplementedError


def fewest_trains(trains: dict[str, list[str]], start: str, end: str) -> int:
    """Return the fewest trains you must take from `start` to `end`.

    `trains` maps each train number to the station codes where it stops.
    You can board or leave a train at any of its stops, in either direction.
    Count trains, not stops.

    Return 0 when `start` equals `end`. Return -1 when no journey exists.
    Do not change `trains`.
    """
    raise NotImplementedError
