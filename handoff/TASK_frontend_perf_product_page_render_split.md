<!-- STATUS: DONE -->
# TASK — Frontend perf: rozbicie renderu strony produktu i `SetVisualization`

## Kontekst
- Źródło: audyt frontendu 2026-05-18
- Obszar: `frontend/src/hooks/useProductPageLogic.js`, `frontend/src/pages/ProductPage.jsx`, `frontend/src/components/shared/SetVisualization.jsx`

## Problem
- `ProductPage` dostaje jeden duży obiekt stanu i renderuje całą stronę razem z sekcjami statycznymi przy każdej zmianie danych kreatora.
- `SetVisualization` robi kosztowne pochodne obliczenia dla każdego slotu na każdym renderze.
- Komponent sam odpala query `drawings-grouped`, więc ten sam koszt może się powtarzać w kilku miejscach, np. w koszyku i podsumowaniu zamówienia.

## Proponowana zmiana
- Oddzielić dynamiczny obszar kreatora od statycznych sekcji strony produktu.
- Zmniejszyć liczbę propsów przekazywanych przez `useProductPageLogic`, tak aby statyczne sekcje nie rerenderowały bez potrzeby.
- W `SetVisualization` przygotowywać dane do preview raz na slot i przekazywać już znormalizowane wejście do renderera.
- Rozważyć przeniesienie `drawings-grouped` do poziomu wyższego cache / contextu, jeśli jest używane w wielu miejscach.

## Zakres prac
- Refactor `useProductPageLogic.js`
- Rozbicie `ProductPage.jsx` na mniejsze sekcje / memoizowane podkomponenty
- Redukcja kosztu `SetVisualization.jsx` dla list i podsumowań

## Kryteria akceptacji
- Zmiana konfiguracji kreatora nie przerysowuje całej strony produktu.
- `SetVisualization` ma mniejszy koszt przy renderze listy i checkoutu.
- Zachowane zostają istniejące funkcje: preview, CTA, SEO, order summary.

## Status
- owner: Frontend
- state: done
- priorytet: medium
