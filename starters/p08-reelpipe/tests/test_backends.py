"""Contract tests: the same tests for every StorageBackend adapter.

Task 19 runs them on s3, task 20 on s3 and azure, and task 21 adds gcs. In task 22 the backend
fixture moves to tests/conftest.py and every test runs on all three clouds.
    uv run pytest -q tests/test_backends.py
When you have written a test, delete its @pytest.mark.skip line.

TODO(task 22): give every test its own key prefix, such as f"test/{uuid4().hex}/", so tests
    and runs never see each other's objects.
"""

import pytest


@pytest.fixture
def backend():
    """The StorageBackend under test.

    TODO(task 20): parametrise this fixture over "s3" and "azure", and build each adapter by name.
    TODO(task 21): add "gcs".
    """
    raise NotImplementedError("TODO(task 19): return the S3 adapter for the reelpipe-uploads bucket")


# ---- The four contract tests (task 19) ----


@pytest.mark.skip(reason="TODO(task 19)")
def test_put_then_get(backend):
    """put() the bytes b"namaste" at a key, then get() of that key returns the same bytes."""
    raise NotImplementedError("TODO(task 19): write this test, then delete the skip line")


@pytest.mark.skip(reason="TODO(task 19)")
def test_missing_key_raises_key_error(backend):
    """get() of a key that was never put raises KeyError, on every cloud."""
    raise NotImplementedError("TODO(task 19): write this test, then delete the skip line")


@pytest.mark.skip(reason="TODO(task 19)")
def test_list_by_prefix(backend):
    """list(prefix) returns the keys put under that prefix, and no key outside it."""
    raise NotImplementedError("TODO(task 19): write this test, then delete the skip line")


@pytest.mark.skip(reason="TODO(task 19)")
def test_presign_put_then_get(backend):
    """presign_upload(), then httpx.put() to its url with its headers, then get() returns the bytes."""
    raise NotImplementedError("TODO(task 19): write this test, then delete the skip line")


# ---- Three more tests (task 22) ----


@pytest.mark.skip(reason="TODO(task 22)")
def test_put_twice_keeps_the_second_value(backend):
    """Putting a key twice keeps the second value."""
    raise NotImplementedError("TODO(task 22): write this test, then delete the skip line")


@pytest.mark.skip(reason="TODO(task 22)")
def test_random_bytes_come_back_unchanged(backend):
    """Random bytes from os.urandom(2048) come back from get() unchanged."""
    raise NotImplementedError("TODO(task 22): write this test, then delete the skip line")


@pytest.mark.skip(reason="TODO(task 22)")
def test_unused_prefix_lists_nothing(backend):
    """list() of a prefix with no objects returns []."""
    raise NotImplementedError("TODO(task 22): write this test, then delete the skip line")
