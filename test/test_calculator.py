from calculator import *
import pytest


def test_add_pass():
    assert 3 == add(1, 2)


def test_add_fail():
    assert 4 == add(1, 2)


@pytest.mark.skip(reason='just don\'t like it')
def test_add_skip():
    assert 4 == add(1, 2)
