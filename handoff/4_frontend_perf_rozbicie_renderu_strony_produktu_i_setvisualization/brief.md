# Brief: Frontend perf: rozbicie renderu strony produktu i SetVisualization

**Task ID:** 4
**URL:** http://localhost/task/4
**Kolumna:** None
**Rola:**
**Suggested AI:**
**Fallback:**

## Opis zadania
Problem: ProductPage renderuje całość przy zmianie danych kreatora. SetVisualization robi kosztowne obliczenia per slot.
Zadanie: Rozbicie ProductPage na memoizowane sekcje, optymalizacja SetVisualization, wyższy poziom cache dla drawings-grouped.

## Status
- [ ] Implementacja
- [ ] Testy
- [ ] Weryfikacja
