class NegativeValueError(ValueError):

    pass


class DataClassifier:

    def classify(self, value):
        # Walidacja typu
        if not isinstance(value, (int, float)):
            raise TypeError("Wartość musi być liczbą (int lub float).")

        # Walidacja wartości
        if value < 0:
            raise NegativeValueError("Wartość nie może być ujemna.")

        # Klasyfikacja
        if value < 30:
            return "Niska wartość"
        if value <= 70:
            return "Średnia wartość"
        return "Wysoka wartość"


# Przykładowe użycie z obsługą wyjątków
if __name__ == "__main__":
    classifier = DataClassifier()

    test_inputs = [50, -10, "abc", 15, 85]
    for v in test_inputs:
        try:
            print(f"{v!r} → {classifier.classify(v)}")
        except Exception as e:
            print(f"{v!r} → Błąd: {e}")
