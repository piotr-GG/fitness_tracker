import pytest

from exercises.exercise import Exercise


def test_is_abstract():
    with pytest.raises(TypeError):
        a = Exercise()


