from collections.abc import Iterator
from typing import List


class SimpleChatbot(Iterator[str]):
    def __init__(self, questions: List[str]) -> None:
        self._questions = questions
        self._index = 0

    def __iter__(self) -> "SimpleChatbot":
        return self

    def __next__(self) -> str:
        if self._index >= len(self._questions):
            raise StopIteration
        q = self._questions[self._index]
        self._index += 1
        return q


# Przykładowa sesja
if __name__ == "__main__":
    bot = SimpleChatbot(["Jak się nazywasz?", "Ulubiony kolor?"])
    for question in bot:
        print(question)
        input("> ")
