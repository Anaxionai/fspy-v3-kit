"""POST /ask without the real API (task 12, step 10).

Each test says what to check. Write the body, then delete its skip line.

Override get_gemini with a fake: embed_question() returns a vector you choose,
answer() returns a fixed text and counts its calls. Store a few rules with known
vectors in rule_chunks first, and send a signed-in user's token.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 12)")
async def test_an_off_topic_question_is_refused_without_a_chat_call(client):
    """The fake question vector is far from every rule: refused is true, citations is
    empty, and answer() was never called."""
    raise NotImplementedError("TODO(task 12): write this test")


@pytest.mark.skip(reason="TODO(task 12)")
async def test_citations_come_only_from_retrieved_rules(client):
    """The fake answer cites [Rule 38] and [Rule 99]: citations is [38], because rule 99
    was not retrieved."""
    raise NotImplementedError("TODO(task 12): write this test")


@pytest.mark.skip(reason="TODO(task 12)")
async def test_a_short_question_gets_422(client):
    """A question of 2 characters gets 422."""
    raise NotImplementedError("TODO(task 12): write this test")
