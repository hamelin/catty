from operator import add, eq, sub
from typing import *  # noqa

from catty import reduce, internal, State, no_check
from catty.words import fork, Word, apply


def test_word_local():
    w = Word(3, 2, 1)
    assert reduce([w]) == [3, 2, 1]


def test_word_calls_word():
    f = Word(3, 2, 1)
    g = Word(f, add)
    h = Word(g, 0, f)
    assert reduce([h]) == [3, 3, 0, 3, 2, 1]


@internal
def dup(state: State) -> None:
    x, = state.consume(no_check)
    state.feed(x, x)


rec = Word(dup, 0, eq, [], [dup, 1, sub, apply.rec], fork)


def test_recursion():
    # Only possible with words defined in a global context.
    assert reduce([5, rec]) == [5, 4, 3, 2, 1, 0]
