from __future__ import annotations
from typing import List


class Book:

    def __init__(self, title: str, author: str, available: bool = True) -> None:
        self.title = title
        self.author = author
        self.available = available

    def is_available(self) -> bool:
        return self.available

    def __repr__(self) -> str:
        return (
            f"Book(title={self.title!r}, author={self.author!r}, "
            f"available={self.available})"
        )


class Library:

    def __init__(self) -> None:
        self._books: List[Book] = []

    # Public API
    def add_book(self, book: Book) -> None:
        self._books.append(book)

    def borrow_book(self, title: str) -> str:
        for book in self._books:
            if book.title == title:
                if book.is_available():
                    book.available = False
                    return f"Wypozyczono: {title}"
                return f"Ksiazka {title} niedostepna"
        return f"Brak ksiazki: {title}"

    def return_book(self, title: str) -> str:
        for book in self._books:
            if book.title == title:
                book.available = True
                return f"Zwrocono: {title}"
        return f"Nie nalezy do biblioteki: {title}"

    def available_books(self) -> list[str]:
        return [book.title for book in self._books if book.is_available()]


# Demo
def main() -> None:
    library = Library()
    library.add_book(Book("Wiedzmin", "Sapkowski"))
    library.add_book(Book("Solaris", "Lem"))
    library.add_book(Book("Lalka", "Prus", available=False))

    print(library.borrow_book("Solaris"))
    print(library.borrow_book("Lalka"))
    print(library.return_book("Lalka"))
    print("Dostepne ksiazki:", library.available_books())


if __name__ == "__main__":
    main()
