from typing import Dict, Optional


class Library:
    def __init__(self) -> None:
        self._books: Dict[str, str] = {}

    def add_book(self, isbn: str, title: str) -> None:
        self._books[isbn] = title

    def find_book(self, isbn: str) -> Optional[str]:
        return self._books.get(isbn)


# Test
lib = Library()
lib.add_book("9788301234567", "Algorytmy w Pythonie")
print(lib.find_book("9788301234567"))
print(lib.find_book("000"))
