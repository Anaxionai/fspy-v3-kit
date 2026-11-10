"""Station search with full-text search (task 11, step 5).

Each test says what to check. Write the body, then delete its skip line.

Your test database needs the name_search column: run the migration on railseat_test.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 11)")
async def test_a_prefix_finds_mumbai(client):
    """With Mumbai Central (BCT) in the stations table, q=mum returns it first."""
    raise NotImplementedError("TODO(task 11): write this test")


@pytest.mark.skip(reason="TODO(task 11)")
async def test_a_code_finds_its_station(client):
    """q=NDLS returns New Delhi."""
    raise NotImplementedError("TODO(task 11): write this test")


@pytest.mark.skip(reason="TODO(task 11)")
async def test_special_characters_give_an_empty_list(client):
    """q=&|! gets 200 and [], never a 500."""
    raise NotImplementedError("TODO(task 11): write this test")
