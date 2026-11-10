"""Per-IP token bucket for POST /links (task 18).

Redis holds the bucket, so every API container shares it.
Key: rl:<ip>, a hash with two fields:
  tokens  the tokens left (may be a fraction)
  ts      the time of the last refill, in seconds (as from time.time())
"""

from fastapi import Request

# TODO(task 18): write the token bucket in Lua, so the refill and the take run as one step
#   and two requests cannot take the same last token. The script's inputs and output:
#     KEYS[1]  rl:<ip>
#     ARGV     the burst, the rate per minute and `now` (and an expiry in seconds, if you pass one)
#     returns  whether the call passed (1 or 0) and the whole seconds to wait (0 when it passed)
#   It must end with EXPIRE, so the keys of idle IPs disappear.
#   Register it once with register_script() on the Redis client from app/cache.py.
TOKEN_BUCKET_LUA = """
-- TODO(task 18): the token bucket, following steps 3 and 4 of the task
"""


async def take_token(ip: str, now: float) -> tuple[bool, int]:
    """Try to take one token from the bucket of `ip` at time `now`.

    Inputs: the client's IP address, and the time in seconds. Tests pass a fake
    `now`, so they never wait for the clock.
    Output: (allowed, retry_after): True when the call may pass, and the whole
    seconds to wait for the next token (0 when allowed).
    The burst and the rate come from settings.rate_limit_burst and
    settings.rate_limit_per_minute.

    The tests check, with burst 5 and 10 a minute: at now=1000.0 five calls
    pass and the sixth fails; at now=1006.0 one more call passes.
    """
    raise NotImplementedError("TODO(task 18): run the Lua token bucket for rl:<ip>")


async def rate_limit(request: Request) -> None:
    """FastAPI dependency for POST /links only (redirects stay unlimited).

    Reads the IP from request.client.host and calls take_token(ip, time.time()).
    When the bucket is empty, it raises HTTPException 429 with a Retry-After
    header in whole seconds.
    """
    raise NotImplementedError("TODO(task 18): 429 with Retry-After when take_token refuses")
