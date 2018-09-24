#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the collect-tweets module.
"""
import pytest

from collect-tweets import collect-tweets


def test_something():
    assert True


def test_with_error():
    with pytest.raises(ValueError):
        # Do something that raises a ValueError
        raise(ValueError)


# Fixture example
@pytest.fixture
def an_object():
    return {}


def test_collect-tweets(an_object):
    assert an_object == {}
