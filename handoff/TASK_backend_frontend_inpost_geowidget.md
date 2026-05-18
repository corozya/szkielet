<!-- STATUS: IN PROGRESS -->
# Task: INPOST-001 - Integracja wyboru Paczkomatu (Geowidget V5)

## Context

Sklep nie oferuje wysyłki Paczkomatami inPost — brakuje zarówno widgetu do wyboru paczkomatu
przez klienta, jak i miejsca do zapisu danych punktu przy zamówieniu.

Rekomendowane rozwiązanie to **InPost Geowidget V5** — gotowy, osadzalny widget mapowy.
Nie wymaga własnej mapy ani pobierania listy punktów z API. Użytkownik klika na mapie i wybiera
paczkomat, widget odpala callback z danymi punktu.

Dane paczkomatu zapisujemy w nowym polu `shipping_meta` (nullable JSON) na tabeli `orders`.
Pole jest zaprojektowane ogólnie — może w przyszłości przechowywać dane innych integracji
(np. DPD Pickup, odbiór osobisty z lokalizacją).

**Geowidget V5 — jak działa:**
- Embed przez CDN `<script>` lub npm `@inpost/geowidget`
- Wymaga tokena z panelu **Manager Paczkomaty → zakładka API**
- Po wyborze punktu odpala event/callback z obiektem:
  `{ name: "WAW01A", address: { street, building_number, city, post_code, province }, ... }`

**ShipX API** (tworzenie przesyłek, etykiety) to osobny krok fulfillmentu — poza zakresem tego zadania.

## Expected Outcome

- Podczas checkout, po wyborze metody wysyłki = Paczkomat, pojawia się widget mapowy inPost.
- Użytkownik wybiera punkt — widget znika, pojawia się potwierdzenie (nazwa + adres paczkomatu).
- Dane paczkomatu są zapisywane w `orders.shipping_meta` jako JSON.
- Panel admina wyświetla wybrany paczkomat przy zamówieniu.
- Przy innych metodach wysyłki (kurier) widget nie pojawia się — standardowy formularz adresu.

## Backend Tasks

- [ ] Nowa migracja: dodać kolumnę `type` (nullable string) do tabeli `shipping_methods`; wartości: `null` (standardowa), `inpost` (Paczkomat inPost)
- [ ] `ShippingMethod` model: dodać `type` do `$fillable`; ustawić istniejącą metodę Paczkomat na `type = 'inpost'` (seeder lub migracja danych)
- [ ] Nowa migracja: dodać kolumnę `shipping_meta` (nullable JSON) do tabeli `orders`
- [ ] `Order` model: dodać `shipping_meta` do `$fillable`, cast na `array`
- [ ] `CreateOrderRequest`: dodać opcjonalne pole `shipping_meta` (nullable array/json)
- [ ] Walidacja warunkowa: jeśli wybrana `ShippingMethod.type === 'inpost'` → `shipping_meta.point_name` wymagane
- [ ] `OrderCreator`: zapisać `shipping_meta` z requestu do modelu
- [ ] API `GET /shipping-methods`: zwracać pole `type` w odpowiedzi
- [ ] Panel admina / OrderPresenter: wyświetlić dane paczkomatu przy zamówieniu (jeśli `shipping_meta` nie jest puste)

## Frontend Tasks

- [ ] Komponent `InPostGeowidget` — ładuje widget przez CDN/npm, nasłuchuje eventu wyboru punktu, wywołuje callback z danymi punktu
- [ ] Token Geowidget: env var `VITE_INPOST_GEOWIDGET_TOKEN` w `.env` frontendu
- [ ] `CheckoutPage` / `useCheckoutLogic`: wykrywać czy `selectedShippingMethod.type === 'inpost'`
- [ ] Gdy Paczkomat: ukryć standardowy formularz adresu, pokazać `InPostGeowidget`
- [ ] Po wyborze punktu: zapisać dane w stanie formularza jako `shipping_meta`, pokazać potwierdzenie (nazwa + adres)
- [ ] `orders.js` API: dołączyć `shipping_meta` do body żądania `POST /orders`
- [ ] Obsługa błędu: jeśli Paczkomat wybrany, ale punkt nie wybrany → zablokować submit z komunikatem

## DevOps Tasks

- [ ] Dodać `VITE_INPOST_GEOWIDGET_TOKEN` do zmiennych środowiskowych frontendu (staging + prod)
- [ ] Opcjonalnie: `INPOST_GEOWIDGET_TOKEN` w backendzie jeśli token będzie serwowany przez API

## Validation

1. Wybrać metodę wysyłki = Paczkomat → widget mapowy inPost pojawia się w checkout
2. Wybrać punkt na mapie → potwierdzenie (nazwa + adres) widoczne, adres ręczny ukryty
3. Próba złożenia zamówienia bez wyboru punktu → błąd walidacji
4. Złożyć zamówienie → `orders.shipping_meta` w bazie zawiera `{ "provider": "inpost", "point_name": "...", "address": {...} }`
5. Panel admina → widok zamówienia pokazuje wybrany paczkomat
6. Wybrać kuriera → widget się nie pojawia, standardowy formularz adresu działa normalnie

## Decisions

- `ShippingMethod.type` — pole string na modelu metody dostawy; wartość `inpost` oznacza Paczkomat i triggeruje widget. Rozszerzalne na kolejnych przewoźników (np. `dpd_pickup`).
- Token Geowidget: `VITE_INPOST_GEOWIDGET_TOKEN` w `.env` frontendu (prostsze, wystarczające).

## Status

- owner: Frontend + Backend
- state: open
- priorytet: medium
- źródło: zgłoszenie użytkownika
