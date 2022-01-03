from catty.words import St, top, peer, alt
from . import check_reduce


def test_resolve_simple():
    check_reduce([8, [7, top]], [[7, 8]])


def test_resolve_complex():
    check_reduce(
        [2, 3, 4, 5, (78, (St[1], 55), {"p": 67, "q": [St[2]]})],
        [2, (78, (4, 55), {"p": 67, "q": [3]})]
    )


def test_resolve_consume_to_deepest_reference():
    check_reduce(
        [23, 1, 2, 3, 4, [alt]],
        [23, 1, [2]]
    )


def test_resolve_repeat():
    check_reduce(
        [23, 1, 2, 3, {"a": peer, "b": peer, "c": peer}],
        [23, 1, {"a": 2, "b": 2, "c": 2}]
    )


def test_resolve_equiv_literals():
    check_reduce(
        [23, 1, 2, 3, [St[0], top, St[1], peer, St[2], alt]],
        [23, [3, 3, 2, 2, 1, 1]]
    )


def test_bare():
    check_reduce(
        [23, 1, 2, 3, St[2]],
        [23, 1]
    )
