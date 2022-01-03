from dataclasses import dataclass
import inspect as ins
from typing import *
import warnings as W


Term = Any
Quote = Sequence[Term]
Data = List
TYPE = TypeVar("TYPE")


@dataclass
class Reduction:
    quote: Quote
    index: int = 0

    def shift(self) -> Any:
        t = self.quote[self.index]
        self.index += 1
        return t

    def at_end(self) -> bool:
        return self.index == len(self.quote)


ParamCheck = Callable[[Any], bool]


def with_attr(*attrs: str) -> ParamCheck:
    def _check(p: Any) -> bool:
        return all(hasattr(p, a) for a in attrs)
    return _check


is_quote = with_attr("__iter__", "__len__")
is_iterable = with_attr("__iter__")
is_mapping = with_attr("__iter__", "__len__", "items")


def of_type(T: Type) -> ParamCheck:
    return lambda p: isinstance(p, T)


no_check = of_type(object)


@dataclass
class State:
    data: Data
    execution: List[Reduction]

    def consume(self, *checks: ParamCheck) -> Sequence:
        if len(checks) == 0:
            W.warn("Consuming 0 term is no-op.", category=RuntimeWarning)
            return []
        elif len(self.data) < len(checks):
            raise IndexError(
                f"Consuming {len(checks)} data elements is not possible, "
                f"stack depth is {len(self.data)}"
            )

        consumed = []
        num_checks = len(checks)
        for i, check in enumerate(checks):
            p = self.data[i - num_checks]
            if not check(p):
                raise ValueError(f"Parameter {i} fails suitability check")
            consumed.append(p)
        del self.data[-num_checks:]
        return consumed

    def consume_any_n(self, n: int) -> Sequence:
        return self.consume(*([no_check] * n))

    def feed(self, *terms: Term) -> None:
        self.data += list(terms)

    def push(self, quote: Quote) -> None:
        if quote:
            self.execution.append(Reduction(quote))

    def next_term(self) -> Any:
        assert self.execution
        current = self.execution[-1]
        term = current.shift()
        if current.at_end():
            self.execution.pop()
        return term


@dataclass
class internal:
    apply: Callable[[State], None]

    @property
    def __name__(self) -> str:
        return self.apply.__name__

    @__name__.setter
    def __name__(self, name_new: str) -> None:
        self.apply.__name__ = name_new

    def __str__(self) -> str:
        return self.apply.__name__

    def __repr__(self) -> str:
        return str(self)


class SubReference(Protocol):

    def resolve(self, x: Any) -> Any:
        ...


@dataclass
class Attr:
    name: str

    def resolve(self, x: Any) -> Any:
        return getattr(x, self.name)


@dataclass
class Item:
    key: Any

    def resolve(self, x: Any) -> Any:
        return x[self.key]


@dataclass
class Reference:
    key: Union[int, slice]
    subrefs: List[SubReference]

    def __getattr__(self, name: str) -> "Reference":
        return Reference(self.key, self.subrefs + [Attr(name)])

    def __getitem__(self, key: Any) -> "Reference":
        return Reference(self.key, self.subrefs + [Item(key)])

    def resolve(self, stack: Data) -> Tuple[Any, int]:
        x: Any
        if isinstance(self.key, int):
            depth = self.key + 1
            x = stack[-self.key - 1]
        elif isinstance(self.key, slice):
            start = self.key.start or 0
            stop = self.key.stop
            assert stop is not None
            step = self.key.step or 1
            x = stack[-stop - start + (step if start else 0)::step]
            depth = self.key.stop
        else:
            raise RuntimeError(f"Reference key should be int or slice: got {self.key}")

        for subref in self.subrefs:
            x = subref.resolve(x)
        return x, depth


def resolve_references(c: Any, state: State) -> Any:
    depth = 0

    def resolve(x: Any) -> Any:
        nonlocal depth
        if isinstance(x, (list, tuple)):
            return type(x)(resolve(e) for e in x)
        elif isinstance(x, set):
            return {resolve(e) for e in x}
        elif isinstance(x, dict):
            return {k: resolve(v) for k, v in x.items()}
        elif isinstance(x, Reference):
            result, d = x.resolve(state.data)
            depth = max(depth, d)
            return result
        else:
            return x

    resolved = resolve(c)
    if depth > 0:
        state.consume_any_n(depth)
    return resolved


def reduce(quote: Quote) -> Sequence:
    if not quote:
        return []

    state = State(data=[], execution=[Reduction(quote=quote)])

    while state.execution:
        term_raw = state.next_term()
        term = resolve_references(term_raw, state)

        if isinstance(term, internal):
            cast(internal, term).apply(state)
        elif hasattr(term, "__call__"):
            sig = ins.signature(term)
            num_args = len([
                p
                for p in sig.parameters.values()
                if (
                    p.kind in {
                        ins.Parameter.POSITIONAL_ONLY,
                        ins.Parameter.POSITIONAL_OR_KEYWORD
                    } and p.default is ins.Parameter.empty
                )
            ])
            args: Sequence
            if num_args == 0:
                args = []
            else:
                args = state.consume_any_n(num_args)

            result = term(*args)
            if result is not None:
                state.feed(result)
        else:
            state.feed(term)

    return state.data
