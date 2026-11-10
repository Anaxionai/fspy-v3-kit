"""Distances, speeds and arrival times (task 20). Plain functions, so they are easy to test.

Your code here will need math (radians, sin, cos, asin, sqrt, ceil) and CITY_SPEED_KMH from app.settings.
"""

EARTH_RADIUS_M = 6_371_000
ROAD_FACTOR = 1.3  # roads are not straight lines
SLOW_KMH = 5  # below this, the rider is probably waiting at a signal


def haversine_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """The distance in metres between two points on the Earth, by the haversine formula.

    The inputs are in degrees. Edge case: a point to itself is 0.
    TODO(task 20): write it. tests/test_geo.py checks (18, 73) to (19, 73), about 111,195 m.
    """
    raise NotImplementedError("TODO(task 20): the haversine formula")


def average_speed_kmh(points: list[dict]) -> float:
    """The rider's average speed in km/h over `points`, their recent stored points, oldest first.

    Each point has location.coordinates [lng, lat] and ts.
    Add the distances between neighbouring points and divide by the time from the first to the last.
    Edge cases: with fewer than 2 points, or a speed under SLOW_KMH, return CITY_SPEED_KMH.
    TODO(task 20): write it.
    """
    raise NotImplementedError("TODO(task 20): the rider's average speed")


def eta_minutes(distance_m: float, speed_kmh: float) -> int:
    """Whole minutes to travel distance_m at speed_kmh along real roads (ROAD_FACTOR), rounded up.

    Example: 2,600 m at 18 km/h is 12 minutes.
    TODO(task 20): write it.
    """
    raise NotImplementedError("TODO(task 20): the arrival time in minutes")
