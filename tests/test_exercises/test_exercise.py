import pytest

from ft_app.models.exercises.exercise import Exercise


def test_is_abstract():
    with pytest.raises(TypeError):
        a = Exercise()


