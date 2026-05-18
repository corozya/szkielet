# Brief: Frontend perf: odchudzenie generowania SVG w kreatorze

**Task ID:** 3
**URL:** http://localhost/task/3
**Kolumna:** None
**Rola:**
**Suggested AI:**
**Fallback:**

## Opis zadania
Problem: Każda zmiana texts przebudowuje cały SVG synchronicznie (DOMParser, XMLSerializer, Canvas, binarne wyszukiwanie font size).
Zadanie: Debounce/requestAnimationFrame, cache wyników fitFontSize, ograniczenie przebudowy do zmienionych slotów.

## Status
- [x] Implementacja
- [x] Testy
- [x] Weryfikacja
