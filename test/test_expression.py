from operator import add
from typing import *

from catty import Stack


def test_pushes():
    assert list(Stack | 0) == [0]
    assert list(Stack | 2 | "asdf") == ["asdf", 2]
