import copy
import inspect as ins
from typing import *  # noqa

from catty import (
    internal,
    State,
    no_check,
    is_quote,
    of_type,
    is_iterable,
    is_mapping,
    Reference,
    resolve_references
)


@internal
def unquote(state: State) -> None:
    quote, = state.consume(is_quote)
    state.push(quote)


class _St:

    def __getitem__(klass, index: int) -> Reference:
        return Reference(index)


St = _St()
top = St[0]
peer = St[1]
alt = St[2]


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
dup3 = Word(3, dupN)


@internal
def swap(state: State) -> None:
    x, y = state.consume_any_n(2)
    state.feed(y, x)


@internal
def over(state: State) -> None:
    x, y = state.consume_any_n(2)
    state.feed(x, y, x)


@internal
def under(state: State) -> None:
    x, y = state.consume_any_n(2)
    state.feed(x, x, y)


@internal
def nip(state: State) -> None:
    x, y = state.consume_any_n(2)
    state.feed(y)


@internal
def tuck(state: State) -> None:
    x, y, z = state.consume_any_n(3)
    state.feed(z, x, y)


@internal
def slide(state: State) -> None:
    z, x, y = state.consume_any_n(3)
    state.feed(x, y, z)


@internal
def snip(state: State) -> None:
    _, x, y = state.consume_any_n(3)
    state.feed(x, y)


@internal
def dropN(state: State) -> None:
    n, = state.consume(of_type(int))
    state.consume_any_n(n)


drop = Word(1, dropN)
drop2 = Word(2, dropN)
drop3 = Word(3, dropN)


@internal
def hide(state: State) -> None:
    x, = state.consume_any_n(1)
    state.data.insert(0, x)


@internal
def reveal(state: State) -> None:
    if not state.data:
        raise IndexError("At least one element must be on the stack")
    x = state.data.pop(0)
    state.feed(x)


@internal
def depth(state: State) -> None:
    state.feed(len(state.data))


@internal
def copy_stack(state: State) -> None:
    state.feed(copy.copy(state.data))


@internal
def set_stack(state: State) -> None:
    stack_new, = state.consume(is_iterable)
    state.data = list(stack_new)


def not_implemented():
    raise NotImplementedError()


save = Word(copy_stack, hide)
restore = Word(reveal, set_stack)


FetchAndCall = Callable[[State], Any]


def _caller(name: str, fetch_and_call: FetchAndCall) -> internal:
    @internal
    def _call(state: State) -> None:
        result = fetch_and_call(state)
        if result is not None:
            state.feed(result)

    _call.__name__ = name
    return _call


def callN(f: Callable, n: int) -> internal:
    def fnc_N(state: State) -> Any:
        args = state.consume_any_n(n)
        return f(*args)

    return _caller("callN", fnc_N)


def callargs(f: Callable) -> internal:
    def fnc_args(state: State) -> None:
        args, = state.consume(is_iterable)
        return f(*args)

    return _caller("callargs", fnc_args)


def callstar(f: Callable) -> internal:
    def fnc_star(state: State) -> None:
        args, kwargs = state.consume(is_iterable, is_mapping)
        return f(*args, **kwargs)

    return _caller("callstar", fnc_star)


def call(f: Callable, *args, **kwargs) -> internal:
    def fnc_resolve(state: State) -> Any:
        args_, kwargs_ = resolve_references((args, kwargs), state)
        return f(*args_, **kwargs_)

    return _caller("call", fnc_resolve)
