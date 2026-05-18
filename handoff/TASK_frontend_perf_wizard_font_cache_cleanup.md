<!-- STATUS: OPEN -->
# TASK — Frontend perf: cleanup cache fontów w podglądzie kreatora

## Kontekst
- Źródło: audyt frontendu 2026-05-18
- Obszar: `frontend/src/components/wizzard/WizzardClientPreview.jsx`, `frontend/src/lib/wizzard/fontCache.js`

## Problem
- Globalny cache `loadedFontFamilies` używa unikalnej nazwy fontu per instancja (`useId()`), więc nie daje realnego reuse między mountami.
- `ensureFontFace()` dokleja kolejne `<style>` do `document.head`, ale nie ma żadnego mechanizmu ponownego użycia, odpinania ani ograniczenia wzrostu.
- Efekt uboczny: narastanie martwych wpisów i stylów przy przechodzeniu między podglądami / ponownych montowaniach.

## Proponowana zmiana
- Ujednolicić identyfikację fontu tak, aby cache był oparty o `fontId` + `fontUrl`, a nie o unikalny `instanceId`.
- Dodać bezpieczny mechanizm deduplikacji stylów w `document.head` po `data-wizzard-font-id` / `data-wizzard-font-family`.
- Rozdzielić cache „font już załadowany” od nazwy używanej do renderu SVG, żeby nie wymuszać nowych wpisów przy każdym mountcie.

## Zakres prac
- Zmiana w `fontCache.js`
- Dostosowanie `WizzardClientPreview.jsx`
- Weryfikacja, czy podgląd nadal poprawnie czeka na załadowanie fontu przed pomiarem tekstu

## Kryteria akceptacji
- Ponowny mount tego samego fontu nie tworzy kolejnych stylów.
- Cache nie rośnie liniowo przy każdym otwarciu podglądu.
- Preview nadal renderuje poprawne metryki po załadowaniu fontu.

## Status
- owner: Frontend
- state: open
- priorytet: high
