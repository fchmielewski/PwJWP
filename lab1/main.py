import json
from typing import Any


class ModelAI:

    liczba_modeli: int = 0

    def __init__(self, nazwa_modelu: str, wersja: Any):
        self.nazwa_modelu = nazwa_modelu
        self.wersja = wersja
        ModelAI.liczba_modeli += 1

    @classmethod
    def nowy_model(cls, nazwa_modelu: str = "unnamed", wersja: Any = 1.0) -> "ModelAI":
        return cls(nazwa_modelu, wersja)

    @classmethod
    def ile_modeli(cls) -> int:
        return cls.liczba_modeli

    @classmethod
    def z_pliku(cls, nazwa_pliku: str) -> "ModelAI":
        with open(nazwa_pliku, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(data["name"], data["version"])

    def __str__(self) -> str:
        return f"{self.nazwa_modelu} v{self.wersja}"

    def __repr__(self) -> str:
        return f"ModelAI({self.nazwa_modelu!r}, {self.wersja!r})"


class Matrix:

    def __init__(self, a: float, b: float, c: float, d: float):
        self.a, self.b, self.c, self.d = a, b, c, d

    def __add__(self, other: "Matrix") -> "Matrix":
        if not isinstance(other, Matrix):
            return NotImplemented
        return Matrix(
            self.a + other.a, self.b + other.b, self.c + other.c, self.d + other.d
        )

    def __mul__(self, other: "Matrix") -> "Matrix":
        if not isinstance(other, Matrix):
            return NotImplemented
        # Mnożenie macierzy 2x2
        e, f, g, h = other.a, other.b, other.c, other.d
        return Matrix(
            self.a * e + self.b * g,  # element (1,1)
            self.a * f + self.b * h,  # element (1,2)
            self.c * e + self.d * g,  # element (2,1)
            self.c * f + self.d * h,  # element (2,2)
        )

    def __str__(self) -> str:
        return f"[{self.a}, {self.b};\n {self.c}, {self.d}]"

    def __repr__(self) -> str:
        return f"M({self.a}, {self.b}; {self.c}, {self.d})"


class Student:

    def __init__(self, name: str, score: float):
        self.name = name
        self.score = score

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.score == other.score

    def __ne__(self, other: object) -> bool:
        eq = self.__eq__(other)
        if eq is NotImplemented:
            return NotImplemented
        return not eq

    def __lt__(self, other: "Student") -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.score < other.score

    def __gt__(self, other: "Student") -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.score > other.score

    def __str__(self) -> str:
        return f"{self.name}: {self.score}"

    def __repr__(self) -> str:
        return f"Student({self.name!r}, {self.score})"
