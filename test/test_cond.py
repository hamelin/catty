from . import check_reduce, check_error
from catty.words import fork


def test_fork_happy():
    check_reduce([True, ["yes"], ["no"], fork], ["yes"])
    check_reduce([False, ["yes"], ["no"], fork], ["no"])


def test_fork_missing_all():
    check_error([fork], IndexError)


def test_fork_missing_two():
    check_error([True, fork], IndexError)


def test_fork_missing_one():
    check_error([False, ["yes"], fork], IndexError)


def test_fork_consequence_not_quote():
    check_error([True, 5, [], fork], ValueError)


def test_fork_alternative_not_quote():
    check_error([False, [], 5, fork], ValueError)
