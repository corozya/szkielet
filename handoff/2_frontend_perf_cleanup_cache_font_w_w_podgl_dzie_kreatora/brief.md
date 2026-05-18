# Brief: Frontend perf: cleanup cache fontów w podglądzie kreatora

**Task ID:** 2
**URL:** http://localhost/task/2
**Kolumna:** None
**Rola:**
**Suggested AI:**
**Fallback:**

## Opis zadania
Problem: Globalny cache loadedFontFamilies używa unikalnej nazwy fontu per instancja, ensureFontFace() dokleja kolejne <style> bez reuse.
Zadanie: Ujednolicić identyfikację fontu, dodać deduplikację stylów w head, rozdzielić cache ładowania od nazwy renderu.

## Status
- [x] Implementacja
- [x] Testy
- [x] Weryfikacja
