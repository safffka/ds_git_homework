"""Tests for `ds_git_homework` package."""

import pytest


@pytest.fixture
def response() -> None:
    """Sample pytest fixture.

    See more at:
    http://doc.pytest.org/en/latest/fixture.html
    """
    return None


def test_content(response: None) -> None:
    """Sample pytest test function with the pytest fixture as an argument."""
    assert response is None
