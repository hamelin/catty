import copy
from types import SimpleNamespace as SN

import pytest

from catty.words import callN, callargs, callstar, call, St, top, peer, alt
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
            call(plonk, St[4], St[3], alt, a=peer, b=top)
        ],
        [23, ([1, 2, 3], {"a": 123, "b": 456})]
    )


def test_call_missing_ref():
    check_error([0, 1, call(plonk, alt)], IndexError)


@pytest.fixture
def root() -> SN:
    r = SN()
    r.asdf = SN()
    r.ls = [1, 2]
    r.di = {"a": 5, "b": 8}
    return r


def test_set_property_attribute(root):
    expected = copy.copy(root)
    expected.qwer = "hoho"
    check_reduce([root, "hoho", peer.set.qwer], [expected])


def test_set_property_attribute_sub(root):
    expected = copy.copy(root)
    expected.asdf.qwer = "hey"
    check_reduce([root, "hey", peer.asdf.set.qwer], [expected])


def test_set_property_list(root):
    expected = copy.copy(root)
    expected.ls[1] = 123
    check_reduce([root, 123, peer.ls.set[1]], [expected])


def test_set_property_dict(root):
    expected = copy.copy(root)
    expected.di["c"] = 87
    check_reduce([123, root, 87, peer.di.set["c"]], [123, expected])
