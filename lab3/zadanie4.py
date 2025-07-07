from typing import Iterator


def fibonacci() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# Użycie
if __name__ == "__main__":
    from itertools import islice

    print(list(islice(fibonacci(), 10)))
