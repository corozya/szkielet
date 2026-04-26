# TASK_12 — Fix: `options` required przy „Opisz zamówienie”

## Problem
- Przy próbie dodania do koszyka w trybie „Opisz zamówienie” pojawia się błąd 422:
  - `The options field is required.`

## Diagnoza
- Backend wymaga niepustego `options` w `POST /api/v1/cart/items`:
  - `apps/reczniki-haftowane/backend/app/Http/Requests/Cart/AddCartItemRequest.php`
  - reguły: `options => required|array`, `options.* => required|integer|min:1`
- Frontend buduje `options` tylko z `slotConfig.option_id`:
  - `apps/reczniki-haftowane/frontend/src/lib/wizzard/wizardConfigSchema.js` (`toCartPayload`)
- W `useProductPageLogic.jsx` było używane `initDefaults`, ale jest deprecated i puste (w store), więc `option_id` bywa puste → `options` puste → 422.

## Kierunek rozwiązania (frontend)
- Bez ręcznego wyboru wariantów w trybie opisu.
- Automatycznie ustawić domyślny wariant per slot (pierwsza opcja `slot.options[0].id`) przed wysłaniem requestu.

## Do zrobienia
- [ ] W `apps/reczniki-haftowane/frontend/src/hooks/useProductPageLogic.jsx` (useAddToCart) uzupełnić brakujące `option_id` domyślnymi wartościami przed `toCartPayload`
- [ ] Zsynchronizować do store przez `wizardSetSlotField(slug, slotId, 'option_id', defaultId)`
- [ ] Dodać guard: jeśli produkt ma opcje, a i tak nie udało się wyliczyć żadnego `option_id`, pokazać czytelny błąd i nie wysyłać requestu
- [ ] Lint dla `useProductPageLogic.jsx`

## Status
- owner: Frontend
- state: todo

