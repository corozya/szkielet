<!-- STATUS: DONE -->
# TASK — Frontend perf: odchudzenie generowania SVG w kreatorze

## Kontekst
- Źródło: audyt frontendu 2026-05-18
- Obszar: `frontend/src/components/wizzard/WizzardClientPreview.jsx`, `frontend/src/lib/wizzard/wizzardClientSvg.js`

## Problem
- Każda zmiana `texts` przebudowuje cały SVG synchronicznie w main thread.
- Pipeline zawiera `DOMParser`, `XMLSerializer`, `document.createElement('canvas')` i binarne wyszukiwanie font size na każdy slot.
- To jest najbardziej prawdopodobne źródło lagów przy szybkim wpisywaniu i na słabszych urządzeniach.

## Proponowana zmiana
- Wprowadzić debounce lub ograniczenie do `requestAnimationFrame` dla przebudowy SVG.
- Dodać cache wyników `fitFontSize()` po kluczu `{text, width, height, fontFamily, opts}`.
- Rozważyć wydzielenie generowania SVG do web workera albo przynajmniej do osobnego helpera z czystym input/output.
- Ograniczyć przebudowę do slotów, które faktycznie się zmieniły, zamiast regenerować cały dokument przy każdej edycji.

## Zakres prac
- Optymalizacja `wizzardClientSvg.js`
- Minimalna zmiana w `WizzardClientPreview.jsx`, żeby nie odpalać pełnej rekonstrukcji częściej niż trzeba
- Dodanie lub aktualizacja testów dla cache / deterministycznego outputu

## Kryteria akceptacji
- Szybkie wpisywanie tekstu nie powoduje widocznych przycięć.
- Taki sam input nie generuje nadmiarowych przebudów SVG.
- Wynik SVG pozostaje funkcjonalnie zgodny z obecną implementacją.

## Status
- owner: Frontend
- state: done
- priorytet: high
