from typing import *  # noqa
import pytest
from catty import reduce, Quote


def check_reduce(quote: Quote, expected: Sequence) -> None:
    assert reduce(quote) == expected


def check_error(quote: Quote, klass_error: Type[Exception]) -> None:
    with pytest.raises(klass_error):
        reduce(quote)
        pytest.fail()
