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
