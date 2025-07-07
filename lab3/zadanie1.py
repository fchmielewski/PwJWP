from __future__ import annotations
from typing import Dict


class Asystent:
    def __init__(self, nazwa: str, wersja: str) -> None:
        self.nazwa = nazwa
        self.wersja = wersja


class AnalizaJezykowa:
    def analizuj_zapytanie(self, zapytanie: str) -> Dict[str, str]:
        # Tu powinien być NLP
        klucz = zapytanie.lower().split()[0]
        return {"intencja": klucz}


class GeneratorOdpowiedzi:
    def generuj_odpowiedz(self, analiza: Dict[str, str]) -> str:
        match analiza.get("intencja"):
            case "hej" | "cześć":
                return "Cześć! W czym mogę pomóc?"
            case "pogoda":
                return "Dziś słonecznie ☀️"
            case _:
                return "Przykro mi, nie rozumiem pytania."


class InteligentnyAsystent(Asystent):

    def __init__(self, nazwa: str, wersja: str) -> None:
        super().__init__(nazwa, wersja)
        self.analityk = AnalizaJezykowa()
        self.generator = GeneratorOdpowiedzi()

    def odpowiedz(self, zapytanie: str) -> str:
        analiza = self.analityk.analizuj_zapytanie(zapytanie)
        return self.generator.generuj_odpowiedz(analiza)


# Prosty test
if __name__ == "__main__":
    bot = InteligentnyAsystent("KompoBot", "1.0")
    print(bot.odpowiedz("hej"))
