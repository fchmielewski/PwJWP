import re
from collections import Counter


class TextAnalyzer:

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        # Słowa definiowane jako sekwencja literr (interpunkcja i wielkość są ignorowane)
        return re.findall(r"\b\w+\b", text.lower())

    def word_count(self, text: str) -> int:
        return len(self._tokenize(text))

    def char_count(self, text: str) -> int:
        return len(text)

    def unique_words(self, text: str) -> int:
        return len(set(self._tokenize(text)))


class AdvancedTextAnalyzer(TextAnalyzer):

    _positive = {
        "wspaniały",
        "świetny",
        "cudowny",
        "dobry",
        "fantastyczny",
        "super",
        "miły",
    }
    _negative = {"okropny", "zły", "fatalny", "straszny", "ponury", "zniechęcający"}

    def sentiment_analysis(self, text: str) -> str:
        tokens = set(self._tokenize(text))
        pos_hits = tokens & self._positive
        neg_hits = tokens & self._negative

        if pos_hits and not neg_hits:
            return "Pozytywny"
        if neg_hits and not pos_hits:
            return "Negatywny"
        # Jeżeli mieszane albo brak słów-kluczy
        return "Neutralny"


# Przykładowe użycie i test
ta = AdvancedTextAnalyzer()
sample_texts = [
    "To był naprawdę wspaniały dzień!",
    "To był naprawdę okropny dzień!",
    "Dzisiaj po prostu dzień jak co dzień.",
]
for t in sample_texts:
    print(
        f'"{t}" → słowa={ta.word_count(t)},  znaki={ta.char_count(t)}, '
        f"unikalne={ta.unique_words(t)},  sentyment={ta.sentiment_analysis(t)}"
    )
