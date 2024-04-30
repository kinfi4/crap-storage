# method send(), throw(), next(), close()
# send() - send data to generator
# throw() - throw exception to generator
# next() - get next value from generator
# close() - close generator
from typing import Generator, Literal


def gen() -> Generator[str, str | int | None, Literal["Done"]]:
    """
    Generator function gets 5 values and print them.
    """

    for i in range(5):
        try:
            x = yield
            print(f"Got {x}")
            yield str(x)  # return value to the caller (aka value = g.send(10))

            yield str(x)  # return value to the next
        except Exception as e:
            print(f"Caught exception {e}")

    return "Done"


g = gen()
next(g)  # the same as next(g). The first call of generator must be without parameter

result = g.send(10)
print(f"Result: {result}")
print(f"Next call in the main {next(g)}")

next(g)

result = g.send("String")
print(f"Result: {result}")
print(f"Next call in the main {next(g)}")

g.throw(ValueError("HELLO"))

g.close()

try:
    g.send("HE")
except StopIteration:
    print("Generator is closed")
