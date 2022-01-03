from catty.words import callN, callargs, callstar, call, St
from . import check_reduce, check_error


def plonk(*args, **kwargs):
    return (list(args), kwargs)


def test_callN_happy():
    check_reduce([23, 1, 2, 3, callN(plonk, 3)], [23, ([1, 2, 3], {})])


def test_callargs_happy():
    check_reduce([23, (1, 2, 3), callargs(plonk)], [23, ([1, 2, 3], {})])


def test_callstar_happy():
    check_reduce(
        [23, [1, 2, 3], {"a": 123, "b": 456}, callstar(plonk)],
        [23, ([1, 2, 3], {"a": 123, "b": 456})]
    )


def test_call_happy():
    check_reduce(
        [
            23,
            1,
            2,
            3,
            123,
            456,
            call(plonk, St[4], St + 3, St.post, a=St.next, b=St.top)
        ],
        [23, ([1, 2, 3], {"a": 123, "b": 456})]
    )


def test_call_consume_to_deepest_reference():
    check_reduce(
        [23, 1, 2, 3, 4, call(plonk, St.post)],
        [23, 1, ([2], {})]
    )


def test_call_repeat_arg():
    check_reduce(
        [23, 1, 2, 3, call(plonk, St[1], St[1], St[1])],
        [23, 1, ([2, 2, 2], {})]
    )


def test_call_equiv_index_add():
    check_reduce(
        [23, 1, 2, 3, call(plonk, St[1], St + 1)],
        [23, 1, ([2, 2], {})]
    )


def test_call_equiv_literals():
    check_reduce(
        [23, 1, 2, 3, call(plonk, St[0], St.top, St[1], St.next, St[2], St.post)],
        [23, ([3, 3, 2, 2, 1, 1], {})]
    )
