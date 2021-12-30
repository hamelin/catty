from typing import *

import pytest

from catty import Stack


def test_stack_empty():
    s = Stack()
    assert list(s) == []
    assert len(s) == 0
    assert not s


def test_stack_init():
    s = Stack([0, 12])
    assert list(s) == [0, 12]
    assert s


def test_stack_deconstruct():
    s = Stack([12, 34, "asdf", "hoho"])
    assert len(s) == 4
    x, y, z, *rest = s
    assert x == 12
    assert y == 34
    assert z == "asdf"
    assert rest == ["hoho"]


def test_stack_deconstruct_single():
    s = Stack(["heyhey"])
    h, = s
    assert h == "heyhey"


def test_stack_get_item():
    s = Stack(["heyhey", "hoho"])
    assert s[0] == "heyhey"
    assert s[1] == "hoho"


def test_stack_get_item_none():
    with pytest.raises(IndexError):
        s = Stack([])
        s[0]


def test_stack_get_item_beyond_length():
    s = Stack(["heyhey", "hoho"])
    assert len(s) == 2
    with pytest.raises(IndexError):
        s[2]


def test_stack_head():
    s = Stack(["heyhey", "hoho"])
    assert s.head == "heyhey"


def test_stack_head_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.head


def test_stack_push():
    s = Stack([])
    assert not s
    s.push(80)
    assert list(s) == [80]
    s.push(28)
    assert s.head == 28
    assert list(s) == [28, 80]


def test_stack_pop():
    s = Stack([28, 80])
    assert list(s) == [28, 80]
    assert s.pop() == 28
    assert list(s) == [80]
    s.push(300)
    assert list(s) == [300, 80]
    assert s.pop() == 300
    assert s.pop() == 80
    assert not s


def test_stack_pop_empty():
    with pytest.raises(IndexError):
        Stack().pop()
