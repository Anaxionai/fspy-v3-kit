"""Week 14 problem session: a cache from a dict and an order.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


class OldestFirstCache:
    """A cache of short links that evicts the link added first.

    It holds at most `capacity` links. A `get` does not change the order.
    A `put` that changes the URL of a cached code keeps that code's place.
    """

    def __init__(self, capacity: int) -> None:
        """Make an empty cache with room for `capacity` links."""
        raise NotImplementedError

    def get(self, code: str) -> str | None:
        """Return the URL for `code`, or None when the code is not cached."""
        raise NotImplementedError

    def put(self, code: str, url: str) -> None:
        """Add a link, or change the URL of a cached code.

        When a new code arrives and the cache is full, first evict the link
        that was added first.
        """
        raise NotImplementedError


class LeastRecentCache:
    """A cache of short links that evicts the least recently used link.

    It holds at most `capacity` links. A `get` that finds the link, and
    every `put`, make that link the most recent. A miss changes nothing.
    """

    def __init__(self, capacity: int) -> None:
        """Make an empty cache with room for `capacity` links."""
        raise NotImplementedError

    def get(self, code: str) -> str | None:
        """Return the URL for `code`, or None when the code is not cached."""
        raise NotImplementedError

    def put(self, code: str, url: str) -> None:
        """Add a link, or change the URL of a cached code.

        When a new code arrives and the cache is full, first evict the least
        recently used link.
        """
        raise NotImplementedError
