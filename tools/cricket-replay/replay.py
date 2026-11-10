#!/usr/bin/env python3
"""Replay one IPL match from Cricsheet, ball by ball, as if it were live.

Match Centre (P2) reads this feed. Start it in Git Bash and leave the terminal open:

    uv run replay.py                     # the default match (see DEFAULT_MATCH below)
    uv run replay.py --match 1529297     # any match id from the IPL archive (find ids with --list)
    uv run replay.py --file match.json   # one Cricsheet JSON match file that you downloaded

Then open http://localhost:8765/live and http://localhost:8765/meta in a browser.
A new ball appears every 2 seconds; change that with --speed.

The data comes from Cricsheet (https://cricsheet.org) under the Open Data
Commons Attribution License 1.0. A public page that shows it must say so.

Only the Python standard library is used, so there is nothing to install.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Callable

ARCHIVE_URL = "https://cricsheet.org/downloads/ipl_json.zip"
DEFAULT_MATCH = "1527687"  # Gujarat Titans v Delhi Capitals, 8 April 2026, won by 1 run
DEFAULT_PORT = 8765
DEFAULT_CACHE = Path.home() / ".cache" / "fspy-cricket-replay"
SOURCE = "Cricsheet (https://cricsheet.org)"
LICENCE = "Open Data Commons Attribution License 1.0 (https://opendatacommons.org/licenses/by/1-0/)"


class ReplayError(Exception):
    """A problem the user can fix, such as a wrong match id. main() prints it without a traceback."""


# ---------------------------------------------------------------------------
# Reading a Cricsheet match
# ---------------------------------------------------------------------------

@dataclass
class Match:
    match_id: str
    meta: dict  # teams, venue, date and more, for GET /meta
    innings: list[dict]  # one entry per innings: number, team, and super_over when true
    deliveries: list[tuple[int, dict]] = field(default_factory=list)  # (innings index, ball), in playing order


def make_ball(delivery: dict, over: int, ball_number: int) -> dict:
    """Turn one Cricsheet delivery into the ball that the feed serves.

    The ball keeps Cricsheet's own facts only. Totals, scorecards and
    commentary are left for Match Centre to work out.
    """
    runs = delivery["runs"]
    ball = {
        "over": over,  # counts from 0, as in Cricsheet: ball 0.1 is the first ball of the innings
        "ball": ball_number,  # 1 to 6; a wide or no-ball does not move it on, so the next ball repeats it
        "batter": delivery["batter"],
        "non_striker": delivery["non_striker"],
        "bowler": delivery["bowler"],
        "runs": {"batter": runs["batter"], "extras": runs["extras"], "total": runs["total"]},
    }
    if runs.get("non_boundary"):
        ball["runs"]["non_boundary"] = True  # 4 runs that were run, not a boundary
    if delivery.get("extras"):
        ball["extras"] = dict(delivery["extras"])  # only the kinds that happened, such as {"wides": 1}
    if delivery.get("wickets"):
        first = delivery["wickets"][0]  # no IPL delivery has two wickets
        wicket = {"player_out": first["player_out"], "kind": first["kind"]}
        fielders = [f["name"] for f in first.get("fielders", []) if "name" in f]
        if fielders:
            wicket["fielders"] = fielders
        ball["wicket"] = wicket
    return ball


def ball_numbers(deliveries: list[dict]) -> list[int]:
    """The ball number (1 to 6) of each delivery in one over.

    Cricsheet 1.3.0 writes it in "actual_delivery", such as "3.2". Older
    files do not have it, so we count: wides and no-balls are not legal
    balls, so they share the number of the next legal ball.
    """
    numbers = []
    legal = 0
    for delivery in deliveries:
        actual = delivery.get("actual_delivery")
        if actual and "." in str(actual):
            numbers.append(int(str(actual).split(".")[1]))
        else:
            numbers.append(legal + 1)
        if not {"wides", "noballs"} & set(delivery.get("extras", {})):
            legal += 1
    return numbers


def load_match(data: dict, match_id: str, seconds_per_ball: float = 2.0) -> Match:
    """Read a Cricsheet match (already parsed from JSON) into a Match."""
    info = data["info"]
    event = info.get("event", {})
    meta = {
        "match_id": match_id,
        "teams": info["teams"],
        "venue": info.get("venue"),
        "city": info.get("city"),
        "date": info["dates"][0],
        "event": event.get("name"),
        "match_number": event.get("match_number"),
        "stage": event.get("stage"),
        "season": str(info.get("season", "")),
        "toss": info.get("toss"),
        "overs": info.get("overs"),
        "balls_per_over": info.get("balls_per_over", 6),
        "players": info.get("players", {}),
        "seconds_per_ball": seconds_per_ball,
        "source": SOURCE,
        "licence": LICENCE,
    }
    match = Match(match_id=match_id, meta=meta, innings=[])
    for index, innings in enumerate(data.get("innings", [])):
        head = {"number": index + 1, "team": innings["team"]}
        if innings.get("super_over"):
            head["super_over"] = True
        match.innings.append(head)
        for over in innings.get("overs", []):
            deliveries = over["deliveries"]
            for delivery, number in zip(deliveries, ball_numbers(deliveries)):
                match.deliveries.append((index, make_ball(delivery, over["over"], number)))
    return match


def start_index(match: Match, innings_number: int = 1, from_over: int = 0) -> int:
    """How many deliveries come before the chosen start point.

    from_over=15 starts with 15 overs of that innings already bowled, so the
    next ball is 15.1. It counts the overs of one innings, from 0.
    """
    if not 1 <= innings_number <= max(1, len(match.innings)):
        raise ReplayError(f"this match has {len(match.innings)} innings, so --innings must be 1 to {len(match.innings)}")
    for position, (index, ball) in enumerate(match.deliveries):
        if index == innings_number - 1 and ball["over"] >= from_over:
            return position
        if index > innings_number - 1:
            return position
    return len(match.deliveries)


# ---------------------------------------------------------------------------
# The replay clock and the two answers
# ---------------------------------------------------------------------------

class Replay:
    """Shows one more delivery every `seconds_per_ball` seconds, from a start point."""

    def __init__(self, match: Match, seconds_per_ball: float = 2.0, start_count: int = 0,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self.match = match
        self.seconds_per_ball = seconds_per_ball
        self.start_count = start_count
        self.clock = clock
        self.started_at = clock()

    def shown(self) -> int:
        """How many deliveries have been bowled so far."""
        ticks = int((self.clock() - self.started_at) / self.seconds_per_ball)
        return min(len(self.match.deliveries), self.start_count + ticks)

    def live(self) -> dict:
        return live_state(self.match, self.shown())

    def meta(self) -> dict:
        return self.match.meta


def live_state(match: Match, shown: int) -> dict:
    """The answer to GET /live: the balls so far, grouped by innings.

    The first innings is always there, with an empty "balls" list before
    the first ball. A later innings appears with its first ball.
    """
    total = len(match.deliveries)
    status = "not started" if shown == 0 else ("finished" if shown >= total else "live")
    grouped: dict[int, list[dict]] = {}
    for index, ball in match.deliveries[:shown]:
        grouped.setdefault(index, []).append(ball)
    innings = []
    for index, head in enumerate(match.innings):
        if index in grouped or index == 0:
            innings.append({**head, "balls": grouped.get(index, [])})
    return {"match_id": match.match_id, "status": status, "innings": innings}


# ---------------------------------------------------------------------------
# The web server
# ---------------------------------------------------------------------------

def make_handler(replay: Replay, quiet: bool = False) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        server_version = "CricketReplay/1.0"

        def end_headers(self) -> None:
            # Any web page may read this feed: it is public match data, on your own computer only.
            self.send_header("Access-Control-Allow-Origin", "*")
            super().end_headers()

        def send_json(self, status: int, body: dict) -> None:
            data = json.dumps(body, ensure_ascii=False, indent=1).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")  # always ask again: the match changes every ball
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(data)

        def do_GET(self) -> None:
            path = self.path.split("?")[0].rstrip("/") or "/"
            if path == "/live":
                self.send_json(200, replay.live())
            elif path == "/meta":
                self.send_json(200, replay.meta())
            elif path == "/":
                self.send_json(200, {"endpoints": ["/live", "/meta"], "match_id": replay.match.match_id,
                                     "source": SOURCE, "licence": LICENCE})
            else:
                self.send_json(404, {"error": f"no page at {path}", "endpoints": ["/live", "/meta"]})

        do_HEAD = do_GET

        def do_OPTIONS(self) -> None:
            # A browser sends OPTIONS (a "preflight") before a cross-origin request with extra headers.
            self.send_response(204)
            self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", self.headers.get("Access-Control-Request-Headers") or "*")
            self.send_header("Access-Control-Max-Age", "600")
            if self.headers.get("Access-Control-Request-Private-Network", "").lower() == "true":
                # Chrome asks this when a public page (such as your github.io site) calls localhost.
                self.send_header("Access-Control-Allow-Private-Network", "true")
            self.send_header("Content-Length", "0")
            self.end_headers()

        def log_message(self, format: str, *args) -> None:
            if not quiet:
                sys.stderr.write(f"{time.strftime('%H:%M:%S')} {self.command} {self.path} {args[1] if len(args) > 1 else ''}\n")

    return Handler


class ReplayServer(ThreadingHTTPServer):
    # On Windows, "reuse address" lets a second server take a busy port without an error,
    # so we turn it off there. Then a second copy of the replay says clearly that the port is busy.
    allow_reuse_address = sys.platform != "win32"
    daemon_threads = True


def serve(replay: Replay, host: str, port: int, quiet: bool = False) -> ThreadingHTTPServer:
    try:
        return ReplayServer((host, port), make_handler(replay, quiet))
    except OSError as error:
        raise ReplayError(f"port {port} is busy ({error.strerror}). Another replay server may be running: "
                          f"stop it with Ctrl+C in its terminal, or add --port {port + 1}") from error


# ---------------------------------------------------------------------------
# Getting the match from Cricsheet's IPL archive
# ---------------------------------------------------------------------------

def download_archive(cache_dir: Path, refresh: bool = False) -> Path:
    """Download Cricsheet's IPL archive once, and keep it in the cache folder."""
    path = cache_dir / "ipl_json.zip"
    if path.exists() and not refresh:
        return path
    cache_dir.mkdir(parents=True, exist_ok=True)
    print(f"Downloading the IPL archive (about 5 MB) from {ARCHIVE_URL} ...")
    request = urllib.request.Request(ARCHIVE_URL, headers={"User-Agent": "fspy-v3-kit cricket-replay"})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = response.read()
    except (urllib.error.URLError, TimeoutError) as error:
        raise ReplayError(f"could not download {ARCHIVE_URL} ({error}). Check your internet connection, "
                          f"or download it in your browser and save it as {path}") from error
    partial = path.with_suffix(".part")
    partial.write_bytes(data)
    partial.replace(path)  # only a complete download gets the real name
    print(f"Saved it as {path}")
    return path


def read_from_archive(zip_path: Path, match_id: str) -> dict:
    """Read one match's JSON from the archive by its id, such as 1527687."""
    if not re.fullmatch(r"\d+", match_id):
        raise ReplayError(f"a match id is a number, such as {DEFAULT_MATCH}, not {match_id!r}")
    try:
        with zipfile.ZipFile(zip_path) as archive:
            return json.loads(archive.read(f"{match_id}.json"))
    except KeyError as error:
        raise ReplayError(f"match {match_id} is not in the IPL archive. Find a match id with --list") from error
    except zipfile.BadZipFile as error:
        raise ReplayError(f"{zip_path} is not a complete zip file. Download it again with --refresh") from error


def list_matches(zip_path: Path, season: str | None = None, team: str | None = None) -> list[tuple[str, str, str]]:
    """The (match id, date, teams) of every match in the archive, newest first.

    The archive's README.txt has one line per match, for example:
    2026-04-08 - club - IPL - male - 1527687 - Gujarat Titans vs Delhi Capitals
    """
    with zipfile.ZipFile(zip_path) as archive:
        text = archive.read("README.txt").decode("utf-8")
    found = []
    for line in text.splitlines():
        parts = line.split(" - ", 5)
        if len(parts) == 6 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", parts[0]) and parts[4].strip().isdigit():
            date, teams, match_id = parts[0], parts[5].strip(), parts[4].strip()
            if season and not date.startswith(season):
                continue
            if team and team.lower() not in teams.lower():
                continue
            found.append((match_id, date, teams))
    return found


# ---------------------------------------------------------------------------
# The command line
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay an IPL match from Cricsheet ball by ball on "
                                                 "http://localhost:8765/live and /meta.")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--match", help=f"a match id from the IPL archive (default {DEFAULT_MATCH})")
    source.add_argument("--file", help="a Cricsheet JSON file of one match")
    source.add_argument("--list", action="store_true", help="list the match ids in the IPL archive, then stop")
    parser.add_argument("--season", help="with --list: only this season, such as 2026")
    parser.add_argument("--team", help="with --list: only matches of a team whose name contains this text")
    parser.add_argument("--speed", type=float, default=2.0,
                        help="seconds between two balls (default 2; 0.5 is faster, 5 is slower)")
    parser.add_argument("--innings", type=int, default=1, help="the innings to start in (default 1)")
    parser.add_argument("--from-over", type=int, default=0,
                        help="start with this many overs of that innings already bowled (default 0)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"the port to serve on (default {DEFAULT_PORT})")
    parser.add_argument("--host", default="127.0.0.1", help="the address to listen on (default 127.0.0.1: this computer only)")
    parser.add_argument("--cache-dir", default=str(DEFAULT_CACHE), help="where to keep the downloaded archive")
    parser.add_argument("--refresh", action="store_true", help="download the IPL archive again")
    parser.add_argument("--quiet", action="store_true", help="do not print a line for every request")
    args = parser.parse_args(argv)
    if args.speed < 0.05:
        parser.error("--speed must be at least 0.05 seconds")
    if args.from_over < 0:
        parser.error("--from-over must be 0 or more")
    return args


def main(argv: list[str] | None = None) -> int:
    # Git Bash connects programs through a pipe, and Python then holds printed lines back.
    # Line buffering makes every message appear as soon as it is printed.
    sys.stdout.reconfigure(line_buffering=True)
    args = parse_args(argv)
    try:
        cache_dir = Path(args.cache_dir)
        if args.list:
            for match_id, date, teams in list_matches(download_archive(cache_dir, args.refresh), args.season, args.team):
                print(f"{match_id}  {date}  {teams}")
            return 0
        if args.file:
            path = Path(args.file)
            if not path.exists():
                raise ReplayError(f"there is no file {path}")
            data = json.loads(path.read_text(encoding="utf-8"))
            match_id = path.stem
        else:
            match_id = args.match or DEFAULT_MATCH
            data = read_from_archive(download_archive(cache_dir, args.refresh), match_id)
        match = load_match(data, match_id, args.speed)
        replay = Replay(match, args.speed, start_index(match, args.innings, args.from_over))
        server = serve(replay, args.host, args.port, args.quiet)
    except ReplayError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    meta = match.meta
    left = len(match.deliveries) - replay.start_count
    print(f"Replaying match {match_id}: {' v '.join(meta['teams'])}, {meta['venue']}, {meta['date']}")
    minutes = max(1, round(left * args.speed / 60))
    print(f"One ball every {args.speed:g} seconds: {left} deliveries, about {minutes} minute{'s' if minutes != 1 else ''}.")
    print(f"Feed: http://localhost:{args.port}/live   Match details: http://localhost:{args.port}/meta")
    print(f"Data: {SOURCE}, {LICENCE}.")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
