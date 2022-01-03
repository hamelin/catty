from catty.words import callN, callargs, callstar, call, St
from . import check_reduce, check_error


def plonk(*args, **kwargs):
    return (list(args), kwargs)


def test_callN_happy():
    check_reduce([23, 1, 2, 3, callN(plonk, 3)], [23, ([1, 2, 3], {})])


def test_callN_insufficient():
    check_error([1, 2, callN(plonk, 3)], IndexError)


def test_callargs_happy():
    check_reduce([23, (1, 2, 3), callargs(plonk)], [23, ([1, 2, 3], {})])


def test_callargs_insufficient():
    check_error([callargs(plonk)], IndexError)


def test_callargs_invalid():
    check_error([3, callargs(plonk)], ValueError)


def test_callstar_happy():
    check_reduce(
        [23, [1, 2, 3], {"a": 123, "b": 456}, callstar(plonk)],
        [23, ([1, 2, 3], {"a": 123, "b": 456})]
    )


def test_callstar_insufficient():
    check_error([(), callstar(plonk)], IndexError)


def test_callstar_wrong_args():
    check_error([None, {}, callstar(plonk)], ValueError)


def test_callstar_wrong_kwargs():
    check_error([(4, 5), [0, 1, 2], callstar(plonk)], ValueError)


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


def test_call_missing_ref():
    check_error([0, 1, call(plonk, St.post)], IndexError)
