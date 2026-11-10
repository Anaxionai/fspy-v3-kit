"""Distance, speed and arrival time (task 20). Plain functions: no services needed."""

import pytest


@pytest.mark.skip(reason="TODO(task 20)")
def test_one_degree_of_latitude():
    """haversine_m from (18, 73) to (19, 73) is about 111,195 m, within 50 m."""
    raise NotImplementedError("TODO(task 20): test haversine_m over one degree")


@pytest.mark.skip(reason="TODO(task 20)")
def test_a_point_to_itself_is_zero():
    """haversine_m from a point to the same point is 0."""
    raise NotImplementedError("TODO(task 20): test haversine_m with no distance")


@pytest.mark.skip(reason="TODO(task 20)")
def test_eta_for_2600_m_at_18_kmh():
    """eta_minutes(2600, 18) is 12: 2,600 m times 1.3, at 18 km/h, rounded up."""
    raise NotImplementedError("TODO(task 20): test eta_minutes")


@pytest.mark.skip(reason="TODO(task 20)")
def test_too_few_points_use_the_city_speed():
    """average_speed_kmh with fewer than 2 points gives CITY_SPEED_KMH."""
    raise NotImplementedError("TODO(task 20): test the speed fallback")
