from typing import *  # noqa
import warnings as W

import pytest
from catty import reduce, Quote


def check_reduce(
    quote: Quote,
    expected: Sequence,
    klasses_warning: Sequence[Type[Warning]] = []
) -> None:
    with W.catch_warnings(record=True) as warnings:
        obtained = reduce(quote)
        assert obtained == expected

        for kw_expected in klasses_warning:
            try:
                index, = [
                    i
                    for i, w in enumerate(warnings)
                    if issubclass(w.category, kw_expected)
                ]
                del warnings[index]
            except ValueError:
                pytest.fail(
                    f"Did not get expected warning of class {kw_expected.__name__}"
                )
        if warnings:
            pytest.fail(
                f"Got unexpected warnings: {[w.category.__name__ for w in warnings]}"
            )


def check_error(quote: Quote, klass_error: Type[Exception]) -> None:
    with pytest.raises(klass_error):
        reduce(quote)
        pytest.fail()
