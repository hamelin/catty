import inspect as ins
from typing import *  # noqa

from catty import internal, State, no_check, is_quote, of_type


@internal
def unquote(state: State) -> None:
    quote, = state.consume(is_quote)
    state.push(quote)


class Word(internal):

    def __init__(self, *quote: Any) -> None:
        def _apply(state: State) -> None:
            state.push(quote)
        super().__init__(apply=_apply)


class _apply(type):

    def __getattr__(klass, name):
        frame = ins.currentframe()
        while frame and frame.f_code.co_name != "<module>":
            frame = frame.f_back
        if frame is None:
            raise RuntimeError(
                f"Cannot find the closest module context where word {name} could "
                "be defined"
            )
        return klass(name, frame.f_globals)


class apply(internal, metaclass=_apply):

    def __init__(self, name: str, env: Mapping[str, Any]) -> None:
        assert name
        self._name = name

        def _apply(state: State) -> None:
            word = env[name]
            word.apply(state)

        super().__init__(apply=_apply)

    def __str__(self) -> str:
        return f"apply.{self._name}"

    def __repr__(self) -> str:
        return str(self)


@internal
def fork(state: State) -> None:
    condition, consequence, alternative = state.consume(no_check, is_quote, is_quote)
    state.push(consequence if condition else alternative)


@internal
def dupN(state: State) -> None:
    n, = state.consume(of_type(int))
    terms = state.consume_any_n(n)
    state.feed(*terms, *terms)


dup = Word(1, dupN)
dup2 = Word(2, dupN)


@internal
def swap(state: State) -> None:
    x, y = state.consume_any_n(2)
    state.feed(y, x)


@internal
def over(state: State) -> None:
    x, y = state.consume_any_n(2)
    state.feed(x, y, x)


@internal
def tuck(state: State) -> None:
    x, y, z = state.consume_any_n(3)
    state.feed(z, x, y)
