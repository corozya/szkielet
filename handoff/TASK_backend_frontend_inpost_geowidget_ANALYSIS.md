# Analiza: TASK_INPOST-001 — Integracja wyboru Paczkomatu (Geowidget V5)

**Źródło:** `handoff/TASK_backend_frontend_inpost_geowidget.md`
**Data analizy:** 2026-05-18
**Status:** IN PROGRESS (analysis-only)

## Kontekst zadania

Sklep nie oferuje wysyłki Paczkomatami inPost. Trzeba zintegrować InPost Geowidget V5 (widget mapowy) w checkout — użytkownik wybiera paczkomat, dane są zapisywane w nowym polu `shipping_meta` (nullable JSON) na tabeli `orders`. Backend dostaje nowe pole `type` na tabeli `shipping_methods` (wartość `inpost` triggeruje widget). Panel admina powinien pokazywać wybrany paczkomat przy zamówieniu.

## Typ zadania

- [x] Frontend (React/Vite)
- [x] Backend (Laravel/Filament)
- [x] DevOps (Docker/CI-CD)

## Uwagi agentów

### Frontend (agent)

#### Pliki do zmiany

| Plik | Zmiana |
|------|--------|
| `src/hooks/useCheckoutLogic.js` | Dodać `shipping_meta: null` do stanu `form`; wykrywać `selectedShipping?.type === 'inpost'`; warunkować logikę `skipAddress`; dołączyć `shipping_meta` do payload `createOrder` |
| `src/lib/validation/checkoutValidator.js` | Dodać opcję `skipAddress` dla InPost (już jest mechanizm `skipAddress`); dodać warunek: jeśli `isInpost && !form.shipping_meta?.point_name` → błąd `shipping_meta` |
| `src/pages/CheckoutPage.jsx` | Przekazać `isInpost` i `shippingMeta`/`setShippingMeta` do `CheckoutFormFields`; `hideAddressSection` zmienić na `hideAddressSection={isInpost || isPersonalPickup}` |
| `src/components/checkout/CheckoutFormFields.jsx` | Gdy `isInpost`: ukryć sekcję adresu, renderować `<InPostGeowidget>` + potwierdzenie wybranego punktu |
| `src/components/checkout/ShippingMethodPicker.jsx` | Brak zmian — komponent renderuje metody z API, nie musi znać `type` |
| `src/api/orders.js` | `createOrder` już przyjmuje dowolny payload — wystarczy że `useCheckoutLogic` dołączy `shipping_meta` |
| `src/components/checkout/InPostGeowidget.jsx` | **Nowy komponent** — ładuje skrypt CDN, inicjalizuje widget, nasłuchuje eventu, wywołuje `onPointSelected(point)` |

#### Aktualny flow checkout — gdzie wstawić logikę InPost

```
useCheckoutLogic
  → selectedShipping (useMemo z shippingMethods + form.shipping_method_id)
  → isInpost = selectedShipping?.type === 'inpost'   ← NOWE

CheckoutPage
  → przekazuje isInpost do CheckoutFormFields
  → hideAddressSection = isInpost || isPersonalPickup  ← zmiana warunku

CheckoutFormFields
  → gdy isInpost: renderuje <InPostGeowidget onPointSelected={...} />
  → po wyborze punktu: pokazuje potwierdzenie (name + adres)

handleSubmit (useCheckoutLogic)
  → validateCheckoutForm(form, { skipAddress: isInpost || isPersonalPickup,
                                  requireShippingMeta: isInpost })  ← NOWE
  → payload do createOrder: { ...formPayload, shipping_meta: form.shipping_meta }
```

#### Gdzie przechowywać `shipping_meta` w stanie formularza

W istniejącym obiekcie `form` w `useCheckoutLogic`:

```js
const [form, setForm] = useState({
  // ... istniejące pola
  shipping_meta: null,   // { provider: 'inpost', point_name, address: { ... } }
})
```

Gdy użytkownik wybierze punkt w Geowidget, callback ustawia:
```js
setForm(prev => ({
  ...prev,
  shipping_meta: {
    provider: 'inpost',
    point_name: point.name,
    address: point.address,
  }
}))
```
Gdy użytkownik zmieni metodę wysyłki na inną niż InPost — wyzerować `shipping_meta: null`.

#### Ładowanie Geowidget — CDN vs npm

**CDN `<script>` tag (rekomendowane dla tego projektu):**
- Plusy: brak bundlowania, widget zawsze w najnowszej wersji InPost, łatwy rollout.
- Plusy: nie blokuje initial bundle — ładowany tylko gdy metoda InPost jest dostępna w sklepie.
- Minusy: dodatkowy request sieciowy w runtime; brak tree-shakingu; wymagana obsługa `onload`/błędu sieci.
- Implementacja: dynamiczny `document.createElement('script')` w `useEffect` wewnątrz `InPostGeowidget`.

**npm `@inpost/geowidget`:**
- Plusy: deterministyczna wersja, offline-capable (jeśli zbudowany lokalnie).
- Minusy: pakiet ciągnie zależności do main bundle; wymaga sprawdzenia licencji dystrybucji; potencjalnie nieaktualna wersja po dłuższym czasie.

**Rekomendacja:** CDN — widget jest heavy (mapa), nie powinien być częścią main bundle. Ładować lazy tylko gdy `isInpost === true` (uniknąć niepotrzebnego requestu dla klientów wybierających kuriera).

#### Ryzyka i edge-casy

1. **Widget może nie załadować się (CDN down, adblocker, brak sieci)** — komponent powinien pokazywać fallback z komunikatem i nie blokować resty formularza; `submitDisabled` musi uwzględniać stan błędu ładowania widgetu.

2. **Race condition: zmiana metody wysyłki po wyborze paczkomatu** — gdy użytkownik wybierze punkt, a potem zmieni metodę na kuriera i z powrotem na InPost: `shipping_meta` powinno się wyzerować przy każdej zmianie `shipping_method_id` (useEffect w `useCheckoutLogic` czyszczący `shipping_meta`).

3. **Mobile** — Geowidget V5 jest responsywny, ale zajmuje dużo miejsca. Na mobile sekcja adresu jest już ukryta (`hideAddressSection`), widget wyrenderuje się w pełnej szerokości — OK. Sprawdzić czy widget nie ma problemów z touch events na iOS Safari (historycznie bywały).

4. **Submit bez wybrania punktu** — `validateCheckoutForm` musi blokować submit z czytelnym błędem (`shipping_meta` wymagane). Błąd powinien pojawić się w `fieldErrors.shipping_meta`, a `scrollToFirstError` w `CheckoutPage.jsx` powinien obsługiwać ten klucz (dodać do tablicy `order`).

5. **Token Geowidget w kodzie frontendowym** — `VITE_INPOST_GEOWIDGET_TOKEN` jest widoczny w bundle. To akceptowalne (token do widgetu mapowego, nie do API ShipX), ale należy ograniczyć token w panelu Manager Paczkomaty do dopuszczonych domen (whitelist origin).

6. **Payload `shipping_meta` nie powinien trafiać do backendu gdy `null`** — w `handleSubmit` warunkować: `...(form.shipping_meta ? { shipping_meta: form.shipping_meta } : {})`.

7. **Sticky przycisk "Zamawiam i płacę" na mobile (UX-M15)** — gdy widget jest otwarty i zajmuje duże obszary ekranu, sticky button z `z-50` może nakładać się na kontrolki widgetu. Warto sprawdzić czy widget nie ma własnego `z-index` problemu.

### Backend (agent)

#### Pliki do zmiany

| Plik | Co zmieniamy |
|---|---|
| `database/migrations/` (2 nowe) | Migracja `type` na `shipping_methods`; migracja `shipping_meta` na `orders` |
| `app/Models/ShippingMethod.php` | Dodać `type` do `#[Fillable]` |
| `app/Models/Order.php` | Dodać `shipping_meta` do `#[Fillable]` + cast na `array` |
| `app/Http/Requests/Order/CreateOrderRequest.php` | Walidacja `shipping_meta` + rozszerzyć `$addressRequired` |
| `app/Services/Order/OrderCreator.php` | Dopisać `shipping_meta` w `Order::create()` |
| `routes/api.php` | Brak zmian kodu — pole `type` pojawi się w odpowiedzi automatycznie |
| `app/Filament/Resources/Orders/Schemas/OrderForm.php` | Nowa sekcja "Paczkomat inPost" + rozszerzyć `isPickupOrder()` |

#### Aktualny schemat tabel — co dodajemy

**`shipping_methods`** — obecne kolumny: `id, name, description, price, max_weight, is_active, sort_order, timestamps`. Brakuje pola `type`.
Nowa migracja:
```php
$table->string('type')->nullable()->after('name');
// null = metoda standardowa, 'inpost' = Paczkomat inPost
```
W tej samej migracji zaktualizować istniejący wpis Paczkomat:
```php
DB::table('shipping_methods')->where('name', 'like', '%inPost%')->update(['type' => 'inpost']);
```

**`orders`** — obecne kolumny: `id, number, user_id, session_token, status, shipping_method_id, items_total, shipping_total, grand_total, shipping_name, shipping_email, shipping_phone, shipping_address, shipping_city, shipping_postal_code, shipping_company, notes, timestamps` (+ dodatkowe kolumny z kolejnych migracji: `nip`, `payu_order_id`, `payment_status`, `payu_redirect_uri`, `payment_method`, `review_token`, `access_token`). Brakuje `shipping_meta`.
Nowa migracja:
```php
$table->json('shipping_meta')->nullable()->after('notes');
```

#### Model Order — jak dodać `shipping_meta`

Model używa atrybutu `#[Fillable([...])]` (Laravel 12 style). Dodać `'shipping_meta'` do listy. Dodać cast:
```php
protected $casts = [
    // ... istniejące encrypted casty ...
    'shipping_meta' => 'array',
];
```
Uwaga: `shipping_meta` **nie szyfrujemy** — dane paczkomatu (nazwa punktu, adres) to publiczne informacje (sieć Paczkomatów jest publiczna), brak danych osobowych.

#### OrderCreator — jak zapisać `shipping_meta`

`OrderCreator::createFromCart()` przyjmuje tablicę `$shippingData` i mapuje pola do `Order::create()`. Wystarczy dopisać jedną linię:
```php
'shipping_meta' => $shippingData['shipping_meta'] ?? null,
```
w bloku `Order::create([...])`. `OrderService::createFromCart()` przekazuje `$request->validated()` przez `array_merge` do `$shippingData`, więc nowe pole pojawi się tam automatycznie po dodaniu reguły walidacji.

#### Walidacja warunkowa w `CreateOrderRequest`

Obecny wzorzec warunkowy: metoda `isPersonalPickup()` sprawdza ShippingMethod po nazwie (`%Odbiór osobisty%`). Dla inpost rozszerzamy o nową metodę pomocniczą bazującą na polu `type`.

Strategia — `Rule::requiredIf` + prywatna metoda:
```php
// W rules():
'shipping_meta'            => ['nullable', 'array'],
'shipping_meta.point_name' => [Rule::requiredIf($this->isInpostShipping()), 'string', 'max:20'],
'shipping_meta.address'    => ['nullable', 'array'],

// Rozszerzyć $addressRequired:
$addressRequired = ($this->isPersonalPickup() || $this->isInpostShipping()) ? 'nullable' : 'required';

// Nowa metoda pomocnicza:
private function isInpostShipping(): bool
{
    $id = $this->input('shipping_method_id');
    if (!$id) return false;
    return \App\Models\ShippingMethod::where('id', $id)
        ->where('type', 'inpost')
        ->exists();
}
```
Podejście spójne z istniejącym `isPersonalPickup()` — jednolity styl w klasie. Przy kolejnych przewoźnikach pickup warto wynieść do osobnej klasy/serwisu.

#### Endpoint `GET /shipping-methods`

Endpoint jest inline w `routes/api.php` — zwraca `$query->get()` bezpośrednio jako Eloquent Collection (auto-serializacja do JSON). Po dodaniu kolumny `type` do bazy pole pojawi się w odpowiedzi **bez żadnych zmian kodu**. Wystarczy zweryfikować po migracji.

#### Filament — wyświetlenie danych paczkomatu w OrderForm

W `OrderForm::configure()` dodać nową sekcję po sekcji "Dostawa":
```php
Section::make('Paczkomat inPost')
    ->hidden(fn (?Order $record): bool => empty($record?->shipping_meta))
    ->components([
        Placeholder::make('inpost_point')
            ->label('Wybrany paczkomat')
            ->content(fn (?Order $record): string => self::formatInpostMeta($record))
            ->columnSpanFull(),
    ]),
```
Helper:
```php
private static function formatInpostMeta(?Order $record): string
{
    $meta = $record?->shipping_meta;
    if (!$meta) return '-';
    $addr = $meta['address'] ?? [];
    return sprintf(
        '%s — %s %s, %s %s',
        $meta['point_name'] ?? '?',
        $addr['street'] ?? '', $addr['building_number'] ?? '',
        $addr['post_code'] ?? '', $addr['city'] ?? ''
    );
}
```

#### Uwaga: `isPickupOrder()` — kolizja z inpost

Obecna metoda `isPickupOrder()` w `OrderForm` ukrywa sekcję "Dostawa" gdy metoda = "Odbiór osobisty". Dla inpost sekcja adresu też powinna być ukryta (pola będą puste). Rozszerzyć warunek:
```php
private static function isPickupOrder(Get $get, ?Order $record): bool
{
    $shippingMethodId = $get('shipping_method_id');
    if (filled($shippingMethodId)) {
        $shippingMethod = ShippingMethod::query()->find($shippingMethodId);
        if ($shippingMethod) {
            if (str_contains($shippingMethod->name, 'Odbiór osobisty')) return true;
            if ($shippingMethod->type === 'inpost') return true;  // NOWE
        }
    }
    $method = $record?->shippingMethod;
    return str_contains((string) ($method?->name ?? ''), 'Odbiór osobisty')
        || $method?->type === 'inpost';  // NOWE
}
```

#### Ryzyka

1. **Istniejące zamówienia bez `shipping_meta`** — kolumna `nullable`, stare rekordy mają `null`. Cast `'array'` zwróci `null` (nie `[]`). Kod w Filament i wszędzie indziej musi sprawdzać `empty($order->shipping_meta)`, nie `=== []`.

2. **Migracja danych dla istniejącego wpisu Paczkomat** — migracja `type` doda kolumnę jako `null` dla wszystkich wpisów. Jeśli w bazie produkcyjnej jest wpis "Paczkomat inPost" bez `type`, dopiero UPDATE w migracji ustawi go poprawnie. Bez tego `GET /shipping-methods` zwróci `"type": null` i frontend nie rozpozna metody InPost.

3. **`shipping_meta` nie jest szyfrowane** — OK dla danych paczkomatu (publiczne punkty). Gdyby w przyszłości dodać telefon kontaktowy do powiadomień InPost — rozważyć szyfrowanie selektywne.

4. **Format `point_name`** — InPost używa kodów w stylu `WAW01A`, ale konwencja nie jest sztywna. Brak walidacji regex — wystarczy `max:20`.

### DevOps (agent)

#### 1. Gdzie i jak dodać `VITE_INPOST_GEOWIDGET_TOKEN`

**`.env.example` (główny)** — `apps/reczniki-haftowane/.env.example`
Należy dopisać sekcję InPost:
```
# --- INPOST ---
VITE_INPOST_GEOWIDGET_TOKEN=   # Token z panelu Manager Paczkomaty → zakładka API
```

**Uwaga krytyczna — brak przekazywania VITE_* do frontendu przez `deploy.sh`:**
Skrypt `deploy.sh` generuje `backend/.env` dynamicznie (sekcja 3 skryptu), ale **nie tworzy żadnego pliku `.env` dla frontendu**. Frontend jest budowany przez CI/CD (GitHub Actions), nie na serwerze. Zmienna `VITE_*` musi być wstrzykiwana **w czasie buildu** w środowisku CI — nie na serwerze.

#### 2. GitHub Secrets — jak przekazać token do buildu frontendu

W obu workflow (`.github/workflows/deploy-prod.yml` i `deploy-beta.yml`) krok `Build` wygląda tak:
```yaml
- name: Build
  working-directory: frontend
  run: npm run build
```
Brakuje przekazania env. Należy rozszerzyć oba kroki:
```yaml
- name: Build
  working-directory: frontend
  env:
    VITE_INPOST_GEOWIDGET_TOKEN: ${{ secrets.VITE_INPOST_GEOWIDGET_TOKEN }}
  run: npm run build
```
Oraz dodać GitHub Secret w ustawieniach repo (Settings → Secrets → Actions):
- `VITE_INPOST_GEOWIDGET_TOKEN` — dla produkcji (token live z panelu InPost)
- Jeśli InPost udostępnia środowisko sandbox: osobny secret np. `VITE_INPOST_GEOWIDGET_TOKEN_BETA`, a workflow beta przekazuje odpowiedni secret

#### 3. Czy `INPOST_GEOWIDGET_TOKEN` potrzebny w backendzie?

Nie — decyzja w zadaniu: token tylko w frontendzie. Backend nie serwuje tokena przez API. Nie trzeba modyfikować `deploy.sh` ani `backend/.env`.

#### 4. Ryzyko: `VITE_*` jest wbudowywane w bundle — zmiana tokena wymaga rebuildu

Vite wbudowuje zmienne `VITE_*` w JavaScript w czasie kompilacji. Aktualizacja tokena wymaga:
1. Zmiany GitHub Secret
2. Ponownego uruchomienia workflow (push taga lub `workflow_dispatch`)

Nie ma możliwości zmiany tokena bez pełnego rebuildu frontendu i ponownego deployu.

#### 5. Plan bezpiecznego wdrożenia — kolejność kroków

1. Dodaj GitHub Secret `VITE_INPOST_GEOWIDGET_TOKEN` (prod + beta osobno)
2. Zaktualizuj oba workflow YAML — dodaj `env: VITE_INPOST_GEOWIDGET_TOKEN` do kroku Build
3. Uzupełnij `.env.example` o sekcję InPost
4. Backend (migracje) + frontend (CI build + rsync) — migracje są automatyczne jako część `deploy.sh`/`deploy-beta.sh` (`php artisan migrate --force`)
5. Kolejność backend→frontend nie jest krytyczna (nowe pola są nullable, brak breaking change), ale zalecane: najpierw backend z migracjami, potem frontend

#### 6. Czy migracja DB jest automatyczna w pipeline?

**Tak.** Zarówno `deploy.sh` (prod) jak i `deploy-beta.sh` wykonują automatycznie:
```bash
php artisan migrate --force
```
Nie wymaga ręcznej interwencji. Migracje są uruchamiane po starcie kontenerów, przed cache config.

#### 7. Staging RPi (192.168.0.170)

Staging RPi nie jest obsługiwany przez GitHub Actions. Token trzeba dodać ręcznie do `.env` na RPi przed uruchomieniem `deploy.sh`. Alternatywnie: zbudować frontend lokalnie z ustawionym `VITE_INPOST_GEOWIDGET_TOKEN` w lokalnym `.env` frontendu i skopiować `dist/` na RPi.

## Plan działania (Architect)

### Faza 1 — Backend (migracje + model + walidacja)

- [ ] **1a.** Nowa migracja: dodać `type` (nullable string) do `shipping_methods` + UPDATE istniejącego wpisu Paczkomat (`type = 'inpost'`) (Backend)
- [ ] **1b.** Nowa migracja: dodać `shipping_meta` (nullable JSON) do `orders` (Backend)
- [ ] **1c.** `ShippingMethod` model: dodać `type` do `#[Fillable]` (Backend)
- [ ] **1d.** `Order` model: dodać `shipping_meta` do `#[Fillable]` + cast `'array'` (Backend)
- [ ] **1e.** `CreateOrderRequest`: dodać walidację `shipping_meta` + metodę `isInpostShipping()` + rozszerzyć `$addressRequired` (Backend)
- [ ] **1f.** `OrderCreator`: dopisać `'shipping_meta' => $shippingData['shipping_meta'] ?? null` (Backend)
- [ ] **1g.** `OrderForm` (Filament): nowa sekcja "Paczkomat inPost" + rozszerzyć `isPickupOrder()` o `type === 'inpost'` (Backend)

### Faza 2 — Frontend (komponent + logika checkout)

- [ ] **2a.** Nowy komponent `InPostGeowidget.jsx` — ładowanie CDN lazy, obsługa eventu wyboru punktu, fallback przy błędzie ładowania (Frontend)
- [ ] **2b.** `useCheckoutLogic.js`: dodać `shipping_meta: null` do stanu `form`; `isInpost` z `selectedShipping?.type`; `useEffect` czyszczący `shipping_meta` przy zmianie metody; dołączyć do payload (warunkowo, nie gdy `null`) (Frontend)
- [ ] **2c.** `checkoutValidator.js`: dodać warunek `requireShippingMeta` — błąd `shipping_meta` gdy InPost bez wybranego punktu (Frontend)
- [ ] **2d.** `CheckoutPage.jsx`: zmienić `hideAddressSection` na `isInpost || isPersonalPickup`; przekazać `isInpost`/setter do `CheckoutFormFields`; dodać `shipping_meta` do `scrollToFirstError` (Frontend)
- [ ] **2e.** `CheckoutFormFields.jsx`: gdy `isInpost` — ukryć sekcję adresu, renderować `<InPostGeowidget>` + potwierdzenie wybranego punktu (Frontend)

### Faza 3 — DevOps (CI/CD + env)

- [ ] **3a.** Uzupełnić `.env.example` o sekcję `# --- INPOST ---` z `VITE_INPOST_GEOWIDGET_TOKEN=` (DevOps)
- [ ] **3b.** Dodać `VITE_INPOST_GEOWIDGET_TOKEN` do GitHub Secrets (prod + beta) (DevOps)
- [ ] **3c.** Rozszerzyć kroki `Build` w `deploy-prod.yml` i `deploy-beta.yml` o `env: VITE_INPOST_GEOWIDGET_TOKEN` (DevOps)
- [ ] **3d.** Dodać token ręcznie do `.env` frontendu na staging RPi lub zbudować lokalnie (DevOps)

### Test plan

1. Checkout → wybrać metodę "Paczkomat inPost" → widget mapowy pojawia się, sekcja adresu ukryta
2. Wybrać punkt na mapie → potwierdzenie (nazwa + adres) widoczne, widget znika
3. Spróbować złożyć zamówienie bez wyboru punktu → błąd walidacji
4. Złożyć zamówienie → `orders.shipping_meta` w DB zawiera `{ provider, point_name, address }`
5. Panel admina → widok zamówienia pokazuje sekcję "Paczkomat inPost"
6. Wybrać metodę kuriera → widget się nie pojawia, standardowy formularz adresu działa
7. Wybrać InPost → wybierz punkt → zmień na kuriera → zmień z powrotem na InPost → `shipping_meta` wyczyszczone (brak wybranego punktu)

## Pytania/Problemy

1. ⚠️ **Token InPost Geowidget** — czy masz już token z panelu Manager Paczkomaty (zakładka API)? Bez niego nie da się przetestować widgetu.
2. ⚠️ **Istniejący wpis Paczkomat w DB** — migracja 1a zakłada UPDATE po nazwie `LIKE '%inPost%'`. Czy nazwa wpisu w tabeli `shipping_methods` zawiera "inPost"? (może być "Paczkomat" lub inna)
3. ℹ️ **Beta token** — czy InPost udostępnia środowisko sandbox/testowe do widgetu? Jeśli nie, beta używa tego samego tokena co prod.

## Status

READY FOR USER
