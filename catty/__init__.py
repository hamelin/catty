from typing import *


class InstantBar(type):

    def __or__(klass, x: Any) -> Type:
        return klass([x])


class Stack(metaclass=InstantBar):

    def __init__(self, elements: Sequence[Any] = []) -> None:
        self._elements = [x for x in elements]

    def __iter__(self) -> Iterator[Any]:
        return iter(self._elements)

    def __len__(self) -> int:
        return len(self._elements)

    def __bool__(self) -> bool:
        return bool(self._elements)

    def __getitem__(self, ref: Union[int, slice, Sequence[int]]) -> Union[Any, "Stack"]:
        if isinstance(ref, int):
            index = cast(int, ref)
            self._check_index_valid(index)
            return self._elements[index]
        elif isinstance(ref, slice):
            sl = cast(slice, ref)
            self._check_index_valid(sl.start)
            return Stack(self._elements[sl])
        elif hasattr(ref, "__getitem__"):
            indices = list(cast(Sequence[int], ref))
            for i in indices:
                self._check_index_valid(i)
            return Stack([self._elements[i] for i in indices])
        else:
            raise TypeError(
                "Stack indices must be integers, slices or sequences of integers; "
                f"not {ref.__class__}"
            )

    def _check_index_valid(self, i: int) -> None:
        ll = len(self)
        if i < -ll or i >= ll:
            raise IndexError(f"Index {i} is invalid")

    @property
    def head(self) -> Any:
        return self[0]

    def push(self, x: Any) -> "Stack":
        self._elements.insert(0, x)
        return self

    def pop(self) -> Any:
        if self._elements:
            return self._elements.pop(0)
        raise IndexError("Stack is empty")

    def __or__(self, x: Any) -> "Stack":
        return Stack([x, *self._elements])
