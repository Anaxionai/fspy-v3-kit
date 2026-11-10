#!/usr/bin/env python3
"""Make RailSeat's seed data: four CSV files of stations, trains, coaches and stops.

RailSeat is the train-booking product you build from P3. You design your own
database schema, and you load these files into it yourself.

Run it from Git Bash:

    uv run make_seed.py              # 62 stations and 120 trains, written next to this script
    uv run make_seed.py --scale      # 10,000 trains for performance work (P10), written to scale/
    uv run make_seed.py --trains 2000 --out-dir big   # any number of trains, any folder

The station codes, names, states, zones and coordinates are real. The trains,
their numbers and their timetables are made up in the style of Indian Railways.
RailSeat is a training product, not a real railway.

The script uses only the Python standard library. The same command always
writes exactly the same files, and the first 120 trains of a bigger set are
the same as the normal set.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_TRAINS = 120  # the normal set
SCALE_TRAINS = 10_000  # the --scale set
SEATS_PER_COACH = {"1A": 24, "2A": 54, "3A": 72, "SL": 72, "CC": 78}
COACH_LETTER = {"1A": "H", "2A": "A", "3A": "B", "SL": "S", "CC": "C"}  # coach codes such as B3 or S7
WEEK = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
DETOUR = 1.18  # tracks are longer than a straight line between two stations


# ---------------------------------------------------------------------------
# Random numbers that stay the same on every Python version
# ---------------------------------------------------------------------------

class Dice:
    """Every helper uses random() only, which Python keeps the same across versions."""

    def __init__(self, seed_text: str) -> None:
        digest = hashlib.sha256(seed_text.encode("utf-8")).digest()
        self._rng = random.Random(int.from_bytes(digest[:8], "big"))

    def number(self, low: int, high: int) -> int:
        """A whole number from low to high, both included."""
        return low + int(self._rng.random() * (high - low + 1))

    def pick(self, items):
        return items[int(self._rng.random() * len(items))]

    def chance(self, probability: float) -> bool:
        return self._rng.random() < probability

    def between(self, low: float, high: float) -> float:
        return low + (high - low) * self._rng.random()


# ---------------------------------------------------------------------------
# Stations (real)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Station:
    code: str
    name: str
    city: str
    state: str
    zone: str  # the Indian Railways zone, as a short code (see README.md)
    latitude: float
    longitude: float


# Coordinates come from each station's English Wikipedia page (November 2026), rounded.
STATIONS = (
    Station("NDLS", "New Delhi", "New Delhi", "Delhi", "NR", 28.6428, 77.2191),
    Station("DLI", "Delhi Junction", "Delhi", "Delhi", "NR", 28.6610, 77.2277),
    Station("NZM", "Hazrat Nizamuddin", "Delhi", "Delhi", "NR", 28.5892, 77.2542),
    Station("CDG", "Chandigarh Junction", "Chandigarh", "Chandigarh", "NR", 30.7030, 76.8220),
    Station("UMB", "Ambala Cantonment Junction", "Ambala", "Haryana", "NR", 30.3382, 76.8287),
    Station("LDH", "Ludhiana Junction", "Ludhiana", "Punjab", "NR", 30.9120, 75.8480),
    Station("ASR", "Amritsar Junction", "Amritsar", "Punjab", "NR", 31.6328, 74.8672),
    Station("JAT", "Jammu Tawi", "Jammu", "Jammu and Kashmir", "NR", 32.7063, 74.8802),
    Station("DDN", "Dehradun", "Dehradun", "Uttarakhand", "NR", 30.3139, 78.0336),
    Station("JP", "Jaipur Junction", "Jaipur", "Rajasthan", "NWR", 26.9208, 75.7866),
    Station("AII", "Ajmer Junction", "Ajmer", "Rajasthan", "NWR", 26.4561, 74.6377),
    Station("KOTA", "Kota Junction", "Kota", "Rajasthan", "WCR", 25.2231, 75.8810),
    Station("AGC", "Agra Cantonment", "Agra", "Uttar Pradesh", "NCR", 27.1589, 77.9906),
    Station("GWL", "Gwalior Junction", "Gwalior", "Madhya Pradesh", "NCR", 26.2161, 78.1819),
    Station("VGLJ", "Virangana Lakshmibai Jhansi Junction", "Jhansi", "Uttar Pradesh", "NCR", 25.4439, 78.5534),
    Station("CNB", "Kanpur Central", "Kanpur", "Uttar Pradesh", "NCR", 26.4539, 80.3512),
    Station("LKO", "Lucknow Charbagh", "Lucknow", "Uttar Pradesh", "NR", 26.8320, 80.9190),
    Station("PRYJ", "Prayagraj Junction", "Prayagraj", "Uttar Pradesh", "NCR", 25.4460, 81.8289),
    Station("BSB", "Varanasi Junction", "Varanasi", "Uttar Pradesh", "NR", 25.3269, 82.9864),
    Station("GKP", "Gorakhpur Junction", "Gorakhpur", "Uttar Pradesh", "NER", 26.7598, 83.3818),
    Station("DDU", "Pt. Deen Dayal Upadhyaya Junction", "Chandauli", "Uttar Pradesh", "ECR", 25.2767, 83.1173),
    Station("PNBE", "Patna Junction", "Patna", "Bihar", "ECR", 25.6028, 85.1375),
    Station("DHN", "Dhanbad Junction", "Dhanbad", "Jharkhand", "ECR", 23.7922, 86.4283),
    Station("ASN", "Asansol Junction", "Asansol", "West Bengal", "ER", 23.6913, 86.9748),
    Station("HWH", "Howrah Junction", "Howrah", "West Bengal", "ER", 22.5829, 88.3428),
    Station("KGP", "Kharagpur Junction", "Kharagpur", "West Bengal", "SER", 22.3399, 87.3250),
    Station("TATA", "Tatanagar Junction", "Jamshedpur", "Jharkhand", "SER", 22.7684, 86.2000),
    Station("BBS", "Bhubaneswar", "Bhubaneswar", "Odisha", "ECoR", 20.2656, 85.8431),
    Station("PURI", "Puri", "Puri", "Odisha", "ECoR", 19.8097, 85.8404),
    Station("NJP", "New Jalpaiguri Junction", "Siliguri", "West Bengal", "NFR", 26.6825, 88.4439),
    Station("GHY", "Guwahati", "Guwahati", "Assam", "NFR", 26.1821, 91.7504),
    Station("CSMT", "Mumbai Chhatrapati Shivaji Maharaj Terminus", "Mumbai", "Maharashtra", "CR", 18.9399, 72.8354),
    Station("BCT", "Mumbai Central", "Mumbai", "Maharashtra", "WR", 18.9697, 72.8194),
    Station("PUNE", "Pune Junction", "Pune", "Maharashtra", "CR", 18.5289, 73.8743),
    Station("NGP", "Nagpur Junction", "Nagpur", "Maharashtra", "CR", 21.1534, 79.0889),
    Station("BSL", "Bhusaval Junction", "Bhusawal", "Maharashtra", "CR", 21.0469, 75.7880),
    Station("SUR", "Solapur", "Solapur", "Maharashtra", "CR", 17.6640, 75.8930),
    Station("ADI", "Ahmedabad Junction", "Ahmedabad", "Gujarat", "WR", 23.0263, 72.6019),
    Station("BRC", "Vadodara Junction", "Vadodara", "Gujarat", "WR", 22.3108, 73.1809),
    Station("ST", "Surat", "Surat", "Gujarat", "WR", 21.2055, 72.8410),
    Station("RJT", "Rajkot Junction", "Rajkot", "Gujarat", "WR", 22.3116, 70.8028),
    Station("BPL", "Bhopal Junction", "Bhopal", "Madhya Pradesh", "WCR", 23.2672, 77.4130),
    Station("ET", "Itarsi Junction", "Itarsi", "Madhya Pradesh", "WCR", 22.6080, 77.7670),
    Station("JBP", "Jabalpur Junction", "Jabalpur", "Madhya Pradesh", "WCR", 23.1647, 79.9511),
    Station("INDB", "Indore Junction", "Indore", "Madhya Pradesh", "WR", 22.7167, 75.8678),
    Station("R", "Raipur Junction", "Raipur", "Chhattisgarh", "SECR", 21.2564, 81.6298),
    Station("MAO", "Madgaon Junction", "Margao", "Goa", "KR", 15.2677, 73.9711),
    Station("MAS", "Chennai Central", "Chennai", "Tamil Nadu", "SR", 13.0825, 80.2750),
    Station("KPD", "Katpadi Junction", "Vellore", "Tamil Nadu", "SR", 12.9722, 79.1383),
    Station("SA", "Salem Junction", "Salem", "Tamil Nadu", "SR", 11.6714, 78.1132),
    Station("CBE", "Coimbatore Junction", "Coimbatore", "Tamil Nadu", "SR", 10.9964, 76.9672),
    Station("TPJ", "Tiruchchirappalli Junction", "Tiruchirappalli", "Tamil Nadu", "SR", 10.7942, 78.6854),
    Station("MDU", "Madurai Junction", "Madurai", "Tamil Nadu", "SR", 9.9200, 78.1103),
    Station("ERS", "Ernakulam Junction", "Kochi", "Kerala", "SR", 9.9689, 76.2916),
    Station("TVC", "Thiruvananthapuram Central", "Thiruvananthapuram", "Kerala", "SR", 8.4874, 76.9520),
    Station("SBC", "KSR Bengaluru City Junction", "Bengaluru", "Karnataka", "SWR", 12.9783, 77.5694),
    Station("MYS", "Mysuru Junction", "Mysuru", "Karnataka", "SWR", 12.3163, 76.6454),
    Station("UBL", "SSS Hubballi Junction", "Hubballi", "Karnataka", "SWR", 15.3500, 75.1491),
    Station("SC", "Secunderabad Junction", "Secunderabad", "Telangana", "SCR", 17.4337, 78.5016),
    Station("BZA", "Vijayawada Junction", "Vijayawada", "Andhra Pradesh", "SCoR", 16.5184, 80.6195),
    Station("GTL", "Guntakal Junction", "Guntakal", "Andhra Pradesh", "SCoR", 15.1750, 77.3670),
    Station("VSKP", "Visakhapatnam Junction", "Visakhapatnam", "Andhra Pradesh", "SCoR", 17.7221, 83.2897),
)
BY_CODE = {station.code: station for station in STATIONS}


# ---------------------------------------------------------------------------
# Train types (made up, in the style of Indian Railways)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TrainType:
    name: str  # written in trains.csv, for example "Rajdhani"
    formation: tuple[tuple[str, int], ...]  # (class, number of coaches), in coach order
    speed: int  # average speed in km/h between two stops
    halts: tuple[int, ...]  # possible stops at a station, in minutes
    departs: tuple[int, int]  # earliest and latest departure from the first station (minutes after midnight)
    days_per_week: tuple[int, ...]  # how many days a week a train of this type can run
    numbers: tuple[tuple[int, int], ...]  # ranges for the train number


DAY = (5 * 60, 7 * 60 + 30)  # day trains leave early in the morning
TYPES = {
    "Rajdhani": TrainType("Rajdhani", (("1A", 1), ("2A", 4), ("3A", 9)), 90, (5, 10), (16 * 60, 17 * 60 + 55),
                          (7,), ((12301, 12499), (20501, 20599))),
    "Duronto": TrainType("Duronto", (("1A", 1), ("2A", 2), ("3A", 6), ("SL", 6)), 86, (5, 10),
                         (20 * 60, 23 * 60 + 40), (2, 3, 7), ((12201, 12299), (22201, 22299))),
    "Shatabdi": TrainType("Shatabdi", (("CC", 8),), 84, (5,), DAY, (6, 7), ((12001, 12049),)),
    "Vande Bharat": TrainType("Vande Bharat", (("CC", 8),), 90, (5,), DAY, (6,), ((20601, 20999), (26001, 26099))),
    "Tejas": TrainType("Tejas", (("CC", 10),), 80, (5,), DAY, (5, 6), ((22101, 22199),)),
    "Jan Shatabdi": TrainType("Jan Shatabdi", (("CC", 6),), 66, (5,), DAY, (6, 7), ((12051, 12099),)),
    "Intercity": TrainType("Intercity", (("CC", 5),), 58, (5,), (6 * 60, 9 * 60), (7,), ((12101, 12199), (22301, 22399))),
    "Superfast": TrainType("Superfast", (("2A", 2), ("3A", 5), ("SL", 8)), 62, (5, 5, 10),
                           (6 * 60, 23 * 60 + 55), (3, 5, 7, 7), ((12501, 12999), (22401, 22999))),
    "Mail": TrainType("Mail", (("1A", 1), ("2A", 2), ("3A", 4), ("SL", 9)), 56, (5, 10, 10, 15),
                      (17 * 60, 23 * 60 + 55), (7,), ((12101, 12199), (12601, 12699))),
    "Express": TrainType("Express", (("2A", 1), ("3A", 3), ("SL", 10)), 50, (5, 10, 15),
                         (0, 23 * 60 + 55), (2, 3, 7, 7), ((11001, 11999), (13001, 19999))),
    "Garib Rath": TrainType("Garib Rath", (("3A", 12),), 64, (5, 10), (18 * 60, 23 * 60 + 30), (2, 3),
                            ((12201, 12299), (22201, 22299))),
    "Humsafar": TrainType("Humsafar", (("3A", 12),), 64, (5, 10), (12 * 60, 23 * 60 + 30), (1, 2),
                          ((22801, 22999),)),
    "Sampark Kranti": TrainType("Sampark Kranti", (("2A", 1), ("3A", 4), ("SL", 8)), 60, (5, 10),
                                (10 * 60, 23 * 60 + 30), (2, 3), ((12401, 12699),)),
}

# The normal set: 60 pairs of trains, each pair running a route in both directions.
# Every station appears in at least one route.
PLAN: tuple[tuple[tuple[str, ...], str], ...] = (
    (("NDLS", "KOTA", "BRC", "ST", "BCT"), "Rajdhani"),
    (("NDLS", "KOTA", "BRC", "ST", "BCT"), "Superfast"),
    (("NDLS", "BCT"), "Duronto"),
    (("NZM", "KOTA", "BRC", "ST", "BCT"), "Garib Rath"),
    (("NZM", "AGC", "GWL", "VGLJ", "BPL", "ET", "BSL", "CSMT"), "Rajdhani"),
    (("NZM", "AGC", "GWL", "VGLJ", "BPL", "ET", "BSL", "CSMT"), "Mail"),
    (("NDLS", "CNB", "PRYJ", "DDU", "DHN", "ASN", "HWH"), "Rajdhani"),
    (("NDLS", "CNB", "PRYJ", "DDU", "PNBE", "ASN", "HWH"), "Superfast"),
    (("NDLS", "CNB", "DHN", "HWH"), "Duronto"),
    (("NZM", "AGC", "GWL", "VGLJ", "BPL", "ET", "NGP", "BZA", "MAS"), "Rajdhani"),
    (("NZM", "AGC", "GWL", "VGLJ", "BPL", "ET", "NGP", "BZA", "MAS"), "Express"),
    (("NZM", "AGC", "GWL", "VGLJ", "BPL", "NGP", "SC", "SBC"), "Rajdhani"),
    (("NZM", "AGC", "GWL", "VGLJ", "BPL", "NGP", "SC", "SBC"), "Superfast"),
    (("CSMT", "PUNE", "SUR", "GTL", "MAS"), "Mail"),
    (("CSMT", "PUNE", "UBL", "SBC"), "Superfast"),
    (("CSMT", "BSL", "NGP", "R", "TATA", "KGP", "HWH"), "Mail"),
    (("CSMT", "NGP", "HWH"), "Duronto"),
    (("MAS", "BZA", "VSKP", "BBS", "KGP", "HWH"), "Superfast"),
    (("MAS", "BZA", "VSKP", "BBS", "KGP", "HWH"), "Express"),
    (("MAS", "KPD", "SBC", "MYS"), "Shatabdi"),
    (("MAS", "KPD", "SBC", "MYS"), "Vande Bharat"),
    (("MAS", "KPD", "SA", "CBE", "ERS", "TVC"), "Mail"),
    (("MAS", "TPJ", "MDU"), "Vande Bharat"),
    (("MAS", "TPJ", "MDU"), "Tejas"),
    (("CSMT", "MAO"), "Vande Bharat"),
    (("ASR", "LDH", "UMB", "NDLS", "KOTA", "BRC", "ST", "BCT"), "Mail"),
    (("CSMT", "MAO", "ERS", "TVC"), "Superfast"),
    (("NDLS", "UMB", "LDH", "ASR"), "Shatabdi"),
    (("NDLS", "UMB", "LDH", "JAT"), "Rajdhani"),
    (("NDLS", "DDN"), "Shatabdi"),
    (("NDLS", "UMB", "CDG"), "Shatabdi"),
    (("NDLS", "UMB", "CDG"), "Vande Bharat"),
    (("NDLS", "JP", "AII"), "Shatabdi"),
    (("JAT", "LDH", "UMB", "NDLS", "AGC", "GWL", "VGLJ", "BPL", "ET", "BSL", "PUNE"), "Express"),
    (("NDLS", "CNB", "LKO"), "Shatabdi"),
    (("NDLS", "CNB", "LKO"), "Tejas"),
    (("NDLS", "CNB", "PRYJ", "BSB"), "Vande Bharat"),
    (("NDLS", "LKO", "GKP", "NJP", "GHY"), "Rajdhani"),
    (("NDLS", "LKO", "GKP", "NJP", "GHY"), "Express"),
    (("HWH", "ASN", "PNBE"), "Jan Shatabdi"),
    (("MAS", "BZA", "SC"), "Express"),
    (("HWH", "KGP", "BBS", "PURI"), "Vande Bharat"),
    (("HWH", "KGP", "BBS", "PURI"), "Superfast"),
    (("ADI", "BRC", "ST", "BCT"), "Shatabdi"),
    (("ADI", "BRC", "ST", "BCT"), "Vande Bharat"),
    (("RJT", "ADI", "BRC", "ST", "BCT"), "Superfast"),
    (("ADI", "AII", "JP", "DLI"), "Superfast"),
    (("PUNE", "SUR", "SC"), "Shatabdi"),
    (("SC", "GTL", "SBC"), "Express"),
    (("SC", "BZA", "VSKP"), "Vande Bharat"),
    (("SC", "BZA", "VSKP"), "Garib Rath"),
    (("SBC", "SA", "CBE", "ERS"), "Intercity"),
    (("INDB", "BPL", "VGLJ", "GWL", "AGC", "NZM"), "Express"),
    (("NGP", "BSL", "PUNE"), "Garib Rath"),
    (("BBS", "TATA", "DHN", "DDU", "PRYJ", "CNB", "NDLS"), "Rajdhani"),
    (("GHY", "NJP", "HWH"), "Superfast"),
    (("JP", "KOTA", "BRC", "ST", "BCT"), "Superfast"),
    (("TVC", "ERS", "CBE", "SA", "BZA", "NGP", "BPL", "VGLJ", "AGC", "NDLS"), "Superfast"),
    (("HWH", "ASN", "DHN", "DDU", "PRYJ", "JBP", "ET", "BSL", "CSMT"), "Mail"),
    (("GKP", "LKO", "CNB", "VGLJ", "BPL", "ET", "BSL", "CSMT"), "Express"),
)
# Types used for the extra trains of a bigger set, with the longest route (km) each suits.
EXTRA_TYPES = (("Express", 4000), ("Express", 4000), ("Superfast", 4000), ("Superfast", 4000), ("Mail", 4000),
               ("Intercity", 550), ("Jan Shatabdi", 650), ("Vande Bharat", 800), ("Garib Rath", 4000),
               ("Humsafar", 4000), ("Sampark Kranti", 4000), ("Duronto", 4000))


# ---------------------------------------------------------------------------
# Building the trains
# ---------------------------------------------------------------------------

@dataclass
class Train:
    number: int
    name: str
    kind: str
    stops: tuple[str, ...]
    runs_on: tuple[str, ...]
    schedule: list[tuple[str, str, str, int, int]]  # (station, arrival, departure, day_offset, km)


def km_between(a: str, b: str) -> int:
    """Rail distance estimate: the great-circle distance times a detour factor."""
    s1, s2 = BY_CODE[a], BY_CODE[b]
    lat1, lon1, lat2, lon2 = map(math.radians, (s1.latitude, s1.longitude, s2.latitude, s2.longitude))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return max(5, round(2 * 6371 * math.asin(math.sqrt(h)) * DETOUR))


def clock(minutes: int) -> str:
    """Minutes after midnight on any day, as HH:MM on a 24-hour clock."""
    return f"{minutes // 60 % 24:02d}:{minutes % 60:02d}"


def up_to_five(minutes: float) -> int:
    """Round up to the next 5 minutes, because timetables use 5-minute steps."""
    return int(math.ceil(minutes / 5) * 5)


def make_schedule(dice: Dice, kind: TrainType, stops: tuple[str, ...]) -> list[tuple[str, str, str, int, int]]:
    """Work out the arrival, departure, day and distance for every stop.

    Times are counted in minutes from midnight of the day the train leaves its
    first station, so 1,500 minutes is 01:00 on the next day (day_offset 1).
    A halt never crosses midnight: if it would, the train arrives at 00:00.
    """
    depart = up_to_five(dice.number(*kind.departs))
    rows = [(stops[0], "", clock(depart), 0, 0)]
    km = 0
    for previous, station in zip(stops, stops[1:]):
        distance = km_between(previous, station)
        km += distance
        arrive = depart + up_to_five(distance / (kind.speed * dice.between(0.92, 1.08)) * 60)
        if station == stops[-1]:
            rows.append((station, clock(arrive), "", arrive // 1440, km))
            break
        leave = arrive + dice.pick(kind.halts)
        if arrive // 1440 != leave // 1440:  # the halt would cross midnight
            arrive = (arrive // 1440 + 1) * 1440
            leave = arrive + dice.pick(kind.halts)
        rows.append((station, clock(arrive), clock(leave), arrive // 1440, km))
        depart = leave
    return rows


def pick_days(dice: Dice, kind: TrainType) -> tuple[str, ...]:
    count = dice.pick(kind.days_per_week)
    if count == 7:
        return WEEK
    first = dice.number(0, 6)
    step = 7 / count  # spread the running days across the week
    return tuple(WEEK[i] for i in sorted({(first + round(n * step)) % 7 for n in range(count)}))


def return_days(days: tuple[str, ...], schedule: list) -> tuple[str, ...]:
    """The return train leaves the day after the outbound train arrives."""
    if len(days) == 7:
        return WEEK
    shift = schedule[-1][3] + 1
    return tuple(WEEK[i] for i in sorted((WEEK.index(day) + shift) % 7 for day in days))


def pick_number(dice: Dice, kind: TrainType, used: set[int]) -> int:
    """An odd train number that is still free; the return train gets the next number."""
    for _ in range(200):
        low, high = dice.pick(kind.numbers)
        number = dice.number(low, high) | 1  # make it odd
        if number + 1 <= 99_999 and number not in used and number + 1 not in used:
            return number
    while True:  # every range of this type is full, so use any free number from 11001 to 29999
        number = dice.number(11_001, 29_999) | 1
        if number not in used and number + 1 not in used:
            return number


def train_name(stops: tuple[str, ...], kind: str) -> str:
    """Names use the cities at both ends, for example "Pune Howrah Duronto Express"."""
    first, last = BY_CODE[stops[0]].city, BY_CODE[stops[-1]].city
    suffix = {"Mail": "Mail", "Express": "Express", "Superfast": "Superfast Express",
              "Intercity": "Intercity Express"}.get(kind, f"{kind} Express")
    return f"{first} {last} {suffix}"


def extra_route(dice: Dice) -> tuple[tuple[str, ...], str]:
    """A route for the trains of a bigger set: part or all of a planned route."""
    stops, _ = dice.pick(PLAN)
    if len(stops) > 2 and dice.chance(0.5):
        length = dice.number(2, len(stops))
        start = dice.number(0, len(stops) - length)
        stops = stops[start:start + length]
    if dice.chance(0.5):
        stops = tuple(reversed(stops))
    total = sum(km_between(a, b) for a, b in zip(stops, stops[1:]))
    kinds = [name for name, longest in EXTRA_TYPES if total <= longest]
    return stops, dice.pick(kinds)


def make_trains(count: int) -> list[Train]:
    """Make trains in pairs: an odd number one way and the next even number back."""
    dice = Dice("railseat|seed|v1")
    used: set[int] = set()
    trains: list[Train] = []
    pair = 0
    while len(trains) < count:
        stops, kind_name = PLAN[pair] if pair < len(PLAN) else extra_route(dice)
        kind = TYPES[kind_name]
        number = pick_number(dice, kind, used)
        used.update((number, number + 1))
        out_schedule = make_schedule(dice, kind, stops)
        days = pick_days(dice, kind)
        if (stops[0], stops[-1]) == ("NDLS", "BCT"):
            days = WEEK  # the New Delhi to Mumbai Central trains run every day (P3 and P4 use them)
        trains.append(Train(number, train_name(stops, kind_name), kind_name, stops, days, out_schedule))
        if len(trains) < count:
            back = tuple(reversed(stops))
            back_schedule = make_schedule(dice, kind, back)
            trains.append(Train(number + 1, train_name(back, kind_name), kind_name, back,
                                return_days(days, out_schedule), back_schedule))
        pair += 1
    return trains


# ---------------------------------------------------------------------------
# Writing the CSV files
# ---------------------------------------------------------------------------

def coaches_for(train: Train) -> list[tuple[int, str, str, int]]:
    rows = []
    for travel_class, count in TYPES[train.kind].formation:
        for n in range(1, count + 1):
            rows.append((train.number, f"{COACH_LETTER[travel_class]}{n}", travel_class, SEATS_PER_COACH[travel_class]))
    return rows


def write_csv(path: Path, header: list[str], rows) -> int:
    # newline="" and lineterminator="\n" give the same bytes on Windows, macOS and Linux.
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        count = 0
        for row in rows:
            writer.writerow(row)
            count += 1
    return count


def write_all(out_dir: Path, count: int) -> dict[str, int]:
    """Write the four files and return how many rows each has."""
    out_dir.mkdir(parents=True, exist_ok=True)
    trains = make_trains(count)
    sizes = {}
    sizes["stations.csv"] = write_csv(
        out_dir / "stations.csv", ["code", "name", "city", "state", "zone", "latitude", "longitude"],
        ((s.code, s.name, s.city, s.state, s.zone, f"{s.latitude:.4f}", f"{s.longitude:.4f}") for s in STATIONS))
    sizes["trains.csv"] = write_csv(
        out_dir / "trains.csv", ["number", "name", "type", "from_station", "to_station", "runs_on"],
        ((t.number, t.name, t.kind, t.stops[0], t.stops[-1], " ".join(t.runs_on)) for t in trains))
    sizes["coaches.csv"] = write_csv(
        out_dir / "coaches.csv", ["train_number", "coach_code", "class", "seats"],
        (row for t in trains for row in coaches_for(t)))
    sizes["schedules.csv"] = write_csv(
        out_dir / "schedules.csv",
        ["train_number", "stop_seq", "station_code", "arrival", "departure", "day_offset", "km"],
        ((t.number, seq, *stop) for t in trains for seq, stop in enumerate(t.schedule, start=1)))
    sizes["seats"] = sum(seats for t in trains for _, _, _, seats in coaches_for(t))
    return sizes


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Make RailSeat's seed CSV files (stations, trains, coaches, schedules).")
    size = parser.add_mutually_exclusive_group()
    size.add_argument("--scale", action="store_true",
                      help=f"make {SCALE_TRAINS:,} trains for performance work, written to scale/ by default")
    size.add_argument("--trains", type=int, help=f"make this many trains (default {BASE_TRAINS})")
    parser.add_argument("--out-dir", help="the folder to write the CSV files to "
                        "(default: the folder of this script, or its scale/ folder with --scale)")
    args = parser.parse_args(argv)
    if args.trains is not None and not 2 <= args.trains <= 50_000:
        parser.error("--trains must be between 2 and 50000")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    count = SCALE_TRAINS if args.scale else (args.trains or BASE_TRAINS)
    if args.out_dir:
        out_dir = Path(args.out_dir).resolve()
    else:
        out_dir = HERE / "scale" if (args.scale or count != BASE_TRAINS) else HERE
    sizes = write_all(out_dir, count)
    print(f"Wrote RailSeat seed data for {count:,} trains to {out_dir}")
    for name in ("stations.csv", "trains.csv", "coaches.csv", "schedules.csv"):
        print(f"  {out_dir / name}  ({sizes[name]:,} rows)")
    print(f"Your loader will create {sizes['seats']:,} seats from coaches.csv.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
