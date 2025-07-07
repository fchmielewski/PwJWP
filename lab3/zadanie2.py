from typing import Iterable


def average(values: Iterable[float]) -> float:
    nums = list(values)
    if not nums:
        raise ValueError("Lista jest pusta")
    return sum(nums) / len(nums)


print(average([1.0, 2.5, 3.5]))
