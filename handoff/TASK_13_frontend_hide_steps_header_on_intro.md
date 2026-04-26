# TASK_13 — Ukryć nagłówek kroków na intro

## Cel
- Na głównej stronie kreatora (intro) ukryć nagłówek z krokami (progress bar + „Krok X z Y”).
- Zostawić **przycisk „X” do zamykania** bez zmian.

## Diagnoza
- Nagłówek kroków na desktop renderuje `PersonalizationTopBar`:
  - `apps/reczniki-haftowane/frontend/src/components/personalization/PersonalizationFlow.jsx`
  - `apps/reczniki-haftowane/frontend/src/components/personalization/PersonalizationTopBar.jsx`
- Przycisk „X” jest osobnym przyciskiem (fixed) w `PersonalizationFlow.jsx` i nie zależy od topbara.

## Implementacja
- Zmienić `PersonalizationFlow.jsx`, aby `PersonalizationTopBar` był renderowany tylko gdy `activeStep?.type !== 'intro'`.

## Do zrobienia
- [ ] Warunkowy render `PersonalizationTopBar` (tylko poza intro)
- [ ] Lint dla `PersonalizationFlow.jsx`

## Status
- owner: Frontend
- state: todo

