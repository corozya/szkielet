# Task: BACKEND-CLEANUP-001 - Backend cleanup i refaktoryzacja zbędnych elementów

## Context
Audyt backendu wskazał kilka obszarów z nadmiarem kodu, martwymi metodami i zbyt ciężkimi klasami:
- martwy presenter `OrderItemConfigurationPresenter`
- martwa metoda `OrderPricing::getGrandTotal()`
- nadmiarowe parametry w `CartService::addItem()`
- przeładowany `OrderItemEmbroiderySnapshotPresenter`
- monolityczny `WizzardPreviewService`

Cel: odchudzić backend bez zmiany zachowania i bez regresji w panelu admina, koszyku, zamówieniach i preview haftu.

## Expected Outcome
- Usunięty martwy kod i nieużywane API.
- Rozbite lub uproszczone klasy z największym długiem technicznym.
- Zachowane testy i działanie obecnych flow.

## Backend Tasks
- [x] Usunąć martwy `OrderItemConfigurationPresenter` i potwierdzić brak referencji `status: DONE`
- [x] Usunąć martwą metodę `OrderPricing::getGrandTotal()` oraz oczyścić powiązane testy `status: DONE`
- [x] Uprościć `CartService::addItem()` przez usunięcie nieużywanych parametrów `status: DONE`
- [x] Rozbić `OrderItemEmbroiderySnapshotPresenter` na mniejsze odpowiedzialności albo zredukować duplikację w renderowaniu HTML `status: DONE`
- [x] Wydzielić wspólne fragmenty w `WizzardPreviewService` dla PNG/WebP i szpulki nici `status: DONE`
- [x] Uruchomić testy backendowe dla koszyka, zamówień, preview i presenterów `status: DONE` (Docker: `php artisan test` → 90 passed)

## Frontend Tasks
- [ ] Brak zmian frontendowych w tym zadaniu `status: TODO`

## DevOps Tasks
- [ ] Brak zmian DevOps w tym zadaniu `status: TODO`

## Validation
- `php artisan test` w backendzie
- dodatkowo sprawdzić testy dot.:
  - `CartService`
  - `OrderService` / `OrderCreator`
  - `OrderItemEmbroiderySnapshotPresenter`
  - `WizzardPreviewService`
- manualnie potwierdzić, że panel order/admin nadal renderuje konfigurację i podglądy haftu
- lokalnie walidacja jest zablokowana, bo dostępny jest tylko `PHP 8.1.2`, a `vendor` wymaga `>= 8.4.0`

## Questions/Issues for Architect
- Czy priorytetem jest najpierw wycięcie martwego kodu, czy rozbicie dużych klas w jednym PR?
- Jeśli rozbijamy `WizzardPreviewService`, czy preferujemy podział na osobne serwisy renderujące, czy tylko ekstrakcję helperów współdzielonych?
- Lokalny `php artisan test` jest zablokowany przez PHP 8.1.2; repo wymaga `>=8.4`. Potrzebny jest runtime 8.4 do pełnej weryfikacji.
