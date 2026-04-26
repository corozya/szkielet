# TASK_11 — Intro kreatora: jedno pole opisu + szablon

## Cel
- Na stronie głównej kreatora (intro) w trybie **„Opisz zamówienie”** ma być **jedno wspólne textarea** zamiast pól per element.
- Jeśli użytkownik **nic nie wpisał** i przechodzi do „Opisz zamówienie”, textarea ma się **automatycznie wypełnić szablonem** na podstawie elementów zestawu.

## Aktualny stan (frontend)
- Komponent: `apps/reczniki-haftowane/frontend/src/components/personalization/PersonalizationIntro.jsx`
- Zapisywanie opisu: `wizardConfig.custom_notes` przez `useWizardStore().setCustomNotes(slug, ...)`
- Walidacja: w trybie opisu wymagane jedno pole (trim != '').

## Wymagania UX (szablon)
- Wstawić szablon **za każdym wejściem** w „Opisz zamówienie”, **tylko jeśli** pole nadal jest puste.
- Szablon ma mieć sekcje per element zestawu.
- Nagłówek sekcji zamiast „Element 1” ma być w formie:
  - `"{slotTypeLabel(slot)} {i+1}"` (np. „Ręcznik kąpielowy 1”)
- W każdej sekcji użytkownik ma uzupełnić:
  - Kolor ręcznika:
  - Wzór haftu:
  - Kolor nici:
  - Tekst do wyhaftowania:

## Do zrobienia
- [ ] W `PersonalizationIntro.jsx` dodać generator szablonu z `customizableSlots` + `slotTypeLabel(slot)`
- [ ] Przy przełączeniu na `mode === 'description'` jeśli `wizardConfig.custom_notes` jest puste → `setCustomNotes(slug, template)`
- [ ] Upewnić się, że nadal działa limit 1000 znaków oraz walidacja „wymagane”
- [ ] Lint dla `PersonalizationIntro.jsx`

## Status
- owner: Frontend
- state: todo

