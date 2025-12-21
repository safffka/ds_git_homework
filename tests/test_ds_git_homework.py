#!/usr/bin/env python
import pytest
from typing import Any
"""Tests for `ds_git_homework` package."""


# from ds_git_homework import ds_git_homework


@pytest.fixture
def response() -> Any:
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyfeldroy/cookiecutter-pypackage')


def test_content(response: Any) -> None:
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
