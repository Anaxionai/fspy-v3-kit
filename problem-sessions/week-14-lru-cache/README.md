# Week 14: A cache from a dict and an order

## The pattern in five lines

1. A cache (a small, fast store that keeps answers you may need again) saves a slow trip to the database.
2. A dict finds a key in O(1) time, and a Python dict also remembers the order in which you added its keys.
3. A full cache must evict (remove an entry to make room): the oldest entry, or the least recently used one.
4. Reach for a dict plus an order when you need fast lookup and a fixed rule for what to throw away.
5. With a dict or `collections.OrderedDict`, both `get` and `put` are O(1). A separate list of keys makes them O(n). See [the Big-O page](../big-o.md).

## Problem A (warm-up, 10 minutes): Oldest-first link cache

Last week you put Redis in front of Shortly's database. Now you add a small cache inside the API process, which holds at most `capacity` links. When it is full, adding a new link evicts the link that was added first.

```python
class OldestFirstCache:
    def __init__(self, capacity: int) -> None: ...
    def get(self, code: str) -> str | None: ...
    def put(self, code: str, url: str) -> None: ...
```

**Examples**

Each row runs after the rows above it, on the same cache.

| Call | Returns | Cache afterwards, oldest first |
|---|---|---|
| `cache = OldestFirstCache(2)` | | (empty) |
| `cache.get("dl7")` | `None` | (empty) |
| `cache.put("dl7", "https://example.com/delhi")` | `None` | `dl7` |
| `cache.put("mb2", "https://example.com/mumbai")` | `None` | `dl7`, `mb2` |
| `cache.get("dl7")` | `"https://example.com/delhi"` | `dl7`, `mb2`: a `get` does not change the order. |
| `cache.put("ch9", "https://example.com/chennai")` | `None` | `mb2`, `ch9`: the cache was full, so `dl7` left. |
| `cache.get("dl7")` | `None` | `mb2`, `ch9` |
| `cache.put("mb2", "https://example.com/mumbai-new")` | `None` | `mb2`, `ch9`: the URL changes, but `mb2` keeps its place. |
| `cache.put("kl5", "https://example.com/kolkata")` | `None` | `ch9`, `kl5`: `mb2` was still the oldest, so it left. |

**Rules**

- `capacity` is a whole number from 1 to 10,000. A cache gets up to 100,000 calls.
- Codes have 1 to 10 letters and digits. A URL is a string that is never empty.
- `get(code)` returns the URL for `code`, or `None` when the code is not in the cache. It does not change the order.
- `put(code, url)` with a new code: if the cache is full, evict the link that was added first. Then add the new link.
- `put(code, url)` with a code already in the cache: change its URL and keep its place. Nothing is evicted.

## Problem B (main, 25 minutes): Least-recently-used link cache

The cache from Problem A can evict a popular link only because it arrived early. An LRU cache (least recently used) evicts the link that has gone unused for the longest time. Both a `get` that finds the link and a `put` count as a use.

```python
class LeastRecentCache:
    def __init__(self, capacity: int) -> None: ...
    def get(self, code: str) -> str | None: ...
    def put(self, code: str, url: str) -> None: ...
```

**Examples**

Each row runs after the rows above it, on the same cache.

| Call | Returns | Cache afterwards, least recent first |
|---|---|---|
| `cache = LeastRecentCache(2)` | | (empty) |
| `cache.get("dl7")` | `None` | (empty) |
| `cache.put("dl7", "https://example.com/delhi")` | `None` | `dl7` |
| `cache.put("mb2", "https://example.com/mumbai")` | `None` | `dl7`, `mb2` |
| `cache.get("dl7")` | `"https://example.com/delhi"` | `mb2`, `dl7`: `dl7` is now the most recent. |
| `cache.put("ch9", "https://example.com/chennai")` | `None` | `dl7`, `ch9`: the cache was full, so `mb2` left. |
| `cache.get("mb2")` | `None` | `dl7`, `ch9`: a miss changes nothing. |
| `cache.put("dl7", "https://example.com/delhi-new")` | `None` | `ch9`, `dl7`: changing a URL counts as a use. |
| `cache.put("kl5", "https://example.com/kolkata")` | `None` | `dl7`, `kl5`: `ch9` was the least recent, so it left. |

**Rules**

- `capacity` is a whole number from 1 to 10,000. A cache gets up to 100,000 calls.
- Codes have 1 to 10 letters and digits. A URL is a string that is never empty.
- `get(code)` returns the URL for `code`, or `None` when the code is not in the cache. A `get` that finds the link makes it the most recent. A miss changes nothing.
- `put(code, url)` with a code already in the cache: change its URL and make it the most recent. Nothing is evicted.
- `put(code, url)` with a new code: if the cache is full, evict the least recent link. Then add the new link as the most recent.
- Aim for O(1) time for each `get` and each `put`. The tests do not time your code.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O for each call?
2. Which link must leave when the cache is full, and how will you find it in O(1) time?
3. Which edge cases (unusual inputs, such as a cache with room for one link) could break your code? Name three.

## After the session

Add an expiry time to `LeastRecentCache`, like the Redis `EXPIRE` command. Give `put` a `ttl` (time to live: the seconds a link stays valid), and pass the current time to `get` and `put`. A `get` after the link expires returns `None`.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
