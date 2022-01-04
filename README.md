# catty -- Concatenative programming integrated in Python

[Concatenative programming](https://concatenative.org/wiki/view/Front%20Page)
is a method and coding style that emphasizes functional composition through
implicit parameter passing and postfix notation. It is often understood as
*stack programming*, mimicking the constraints of stack machines. While it
carries some hipster cred, it is popular in development circles involving
dedicated hardware. Its most popular incarnation is the
[FORTH](https://concatenative.org/wiki/view/Forth) language; the
[Factor](https://factorcode.org/) language and platform provides a more modern
programming system over its principles.

This project is an attempt at integrating a concatenative style and approach
to the Python language and software ecosystem. Its present incarnation is
somewhat clumsy as it parasites the Python syntax: a catty program is valid
Python code. The catty semantics also attempt to leverage the Python built-ins
and library as much as possible. Here is a taste:


```python
from operator import add, mul
from catty import reduce
from catty.words import dup


result = reduce([5, 6, dup, mul, add])
print(result)  # Yields [41]
```

So this early take yields the answer to life, the universe and everything,
but it's off by one. Should be fixed in next version.

The interpretation is performed in a Python code loop, so speed cannot be
expected. However, the interpreter in its current form optimizes tail calls,
enabling arbitrary recursive applications:

```python
from operator import mul
from catty import reduce
from catty.words import dup, tuck, fork, apply, Word

factorial_ = Word(  # prod, n -- prod, n-1
    dup, 0, eq,
    [],
    [dup, tuck, mul, swap, 1, sub, apply.factorial_],
    fork
)
factorial = Word(  # n -- n!
    1, swap, factorial_
)
print(reduce([5, factorial]))  # Yields [120]
```

This project is meant for incremental exploration of interactions between
concatenative and applicative programming styles. It will not shy away from
changing completely as it progresses. Current plans involve digging further
into tapping into namespace control through function definitions, replacing
the interpretation loop with Python bytecode generation, and further
strengthening integration so that concatenative and regular Python code can
live side by side.
