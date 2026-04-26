# TASK_19 — Dwa tryby składania zamówienia: rozłączne payloady (kreator vs opis)

## Cel
- Utrwalić model UX i danych: są **2 tryby** składania zamówienia:
  - **wizualny (kreator)**: konfiguracja w `configuration.slots`
  - **tekstowy (textarea)**: opis w `configuration.custom_notes`
- Tryby są **rozłączne w payloadzie**: backend dostaje tylko dane aktywnego trybu (żeby nie mieszać i nie generować mylących podglądów).
- Stan nieaktywnego trybu może zostać w UI (Zustand) dla łatwego powrotu, ale **nie jest wysyłany**.

## Ustalenia po dyskusji (2026-04-26)
- **Tryb tekstowy (`description`)**:
  - `options` są **opcjonalne** (backend przestaje wymagać).
  - Frontend **nie autouzupełnia** wariantów/`option_id` „na siłę”.
  - **Nie tworzymy `wizzard_projects`** w tym trybie.
  - Backend musi działać deterministycznie, gdy `options` brak (np. cena bazowa albo domyślne warianty serwerowe).

## Zakres
### Frontend
- Źródło trybu: `PersonalizationIntro.jsx` (toggle).
- Przy dodaniu do koszyka:
  - jeśli aktywny tryb = description:
    - wysyłaj `configuration.custom_notes`
    - wysyłaj `configuration.slots` jako `{}` albo `null` (ustalić spójnie), niezależnie od tego co jest w store
    - `options`: wysyłaj `{}` lub pomiń całkowicie (backend przyjmuje)
    - **nie twórz** `wizzard_projects`
  - jeśli aktywny tryb = designer:
    - wysyłaj `configuration.slots` (snapshot)
    - `custom_notes` opcjonalnie (np. snapshot) lub null
    - `options` pozostają wymagane (jak dziś)

### Backend
- Upewnić się, że:
  - `configuration` może mieć puste `slots` (już jest `nullable|array`)
  - walidacja tekstów haftu nie wybucha, gdy `slots` puste
  - `Order` snapshot przechowuje to, co przyszło (bez dopisywania slotów)
  - **Tryb tekstowy** nie wymaga `options`:
    - zaktualizować walidację `AddCartItemRequest` (`options` → `nullable|array`, `options.*` tylko jeśli `options` jest podane)
    - logika koszyka/pricing działa gdy `options` brak (spójna odpowiedź API, np. `options: {}`)

## Miejsca w kodzie (orientacyjnie)
- Frontend payload: `apps/reczniki-haftowane/frontend/src/lib/wizzard/wizardConfigSchema.js` (`toCartPayload`, `buildCartConfigSnapshot`)
- Add-to-cart flow: `apps/reczniki-haftowane/frontend/src/hooks/useProductPageLogic.jsx`
- Backend request: `apps/reczniki-haftowane/backend/app/Http/Requests/Cart/AddCartItemRequest.php`
- Order snapshot: `apps/reczniki-haftowane/backend/app/Services/Order/ConfigurationSnapshotBuilder.php`

## Kryteria akceptacji (manual)
- W trybie tekstowym, po dodaniu do koszyka:
  - w API `cart.items[].configuration.slots` jest puste,
  - `cart.items[].configuration.custom_notes` ma opis,
  - podglądy nie sugerują „wyklikanych” ręczników/haftu,
  - działa także gdy request nie wysyła `options`.
- W trybie kreatora:
  - `configuration.slots` zawiera dane (jak dziś),
  - opis działa niezależnie (jeśli włączony).

## Status
- owner: Backend (Claude)
- state: **ready-for-claude** (frontend done, backend snapshot+service do dorobienia)
- **Suggested AI:** Claude
- **Fallback AI:** Codex
- **Context size needed:** Medium
- **Baseline commit:** `cde75e1` (apps/reczniki-haftowane@main, pushnięty na origin 2026-04-26)

## Ready for Claude — brief

### Cel
Domknąć backendową część TASK_19: snapshot zamówienia ma respektować pusty `slots` w trybie description, a `CartService::addItem` nie wymaga `options` w sygnaturze.

### Whitelist plików do modyfikacji
- `apps/reczniki-haftowane/backend/app/Services/Order/ConfigurationSnapshotBuilder.php`
- `apps/reczniki-haftowane/backend/app/Services/CartService.php`
- `apps/reczniki-haftowane/backend/app/Http/Controllers/Api/V1/CartController.php` (tylko metoda `addItem`, nie ruszamy `show/updateItem/removeItem/merge`)
- `apps/reczniki-haftowane/backend/tests/Feature/Cart/AddCartItemTest.php` (nowy lub istniejący — feature test)

**Nie ruszamy:** żadnych plików frontendu, walidacji `AddCartItemRequest` (już zaktualizowana w `fd2eb6e`), `OrderItemsRelationManager`, emaili, `wizardStore`, `cartStore`. Reszta backendu poza listą — też nie.

### Definition of Done

1. **`ConfigurationSnapshotBuilder::build()`** — gdy `$baseConfig['custom_notes']` jest niepusty stringiem oraz `$baseSlots` jest puste/brak ORAZ `$cartItem->options` jest pusty/brak, metoda zwraca:
   ```php
   ['slots' => [], 'custom_notes' => $baseConfig['custom_notes']]
   ```
   bez iteracji po `$product->slots` i bez dopisywania pustych slotów. W każdym innym przypadku zachowane jest obecne zachowanie (fill z product slots + opcjonalna injekcja `$project`).

2. **`CartService::addItem`** — sygnatura:
   ```php
   public function addItem(
       CartSession $session,
       int $productId,
       int $quantity,
       ?array $options = [],
       ?int $embroideryProjectId = null,
       ?array $configuration = null
   ): CartItem
   ```
   W ciele: `'options' => $options ?? [],`.

3. **`CartController::addItem`** — `$request->options` zastąpione przez `$request->input('options') ?? []` (defensive).

4. **Test feature `AddCartItemTest`** — pokrywa 3 przypadki:
   - `POST /cart/items` z `options: { "1": 5 }` + `configuration.slots` (designer mode) → sukces, `cart.items[0].options == { "1": 5 }`, `configuration.slots` zawiera dane
   - `POST /cart/items` bez klucza `options` + `configuration.custom_notes: "tekst"` (description mode) → sukces, `cart.items[0].options == []`, `configuration.slots == {}`, `custom_notes == "tekst"`
   - `POST /cart/items` z `options: null` + `configuration.custom_notes: "tekst"` → sukces (nullable validation OK), `cart.items[0].options == []`

5. **Manual E2E** (Claude opisuje w komencie do PR/handoff, nie wykonuje):
   - Description mode → `Order.items[].options_snapshot` lub `configuration_snapshot.slots` jest **puste** (nie zawiera dopisanych slotów z `product->slots`).
   - `configuration_snapshot.custom_notes` zawiera opis klienta.

6. **Status handoff** — po commitcie zmienić w tym pliku `state: ready-for-claude` → `state: done` i dopisać w sekcji „Weryfikacja" SHA finalnego commita.

### Verification Claude powinien uruchomić
```bash
cd apps/reczniki-haftowane/backend
php artisan test --filter=AddCartItemTest
php artisan test --filter=ConfigurationSnapshotBuilder
```
Oba muszą zielenieć. Jeśli `ConfigurationSnapshotBuilder` test nie istnieje, Claude może go opcjonalnie dodać (poza zakresem DoD, ale mile widziane).

### Format commita
```
fix(task-19): backend snapshot empty slots + service nullable options

- ConfigurationSnapshotBuilder::build respects empty slots payload
  in description mode (no fill from product->slots when only custom_notes)
- CartService::addItem accepts ?array $options (default [])
- CartController::addItem defensive null fallback
- Feature test: AddCartItem with/without options
```

## Weryfikacja commita `fd2eb6e` (2026-04-26)

Repo: `apps/reczniki-haftowane/`, commit `fd2eb6e feat(task-19): implement exclusive payloads for order modes`.

### Zrobione (zgodne ze spec)
- Frontend, tryb description: `toCartPayload(..., 'description')` w `frontend/src/lib/wizzard/wizardConfigSchema.js` zwraca `options: {}` i `configuration: { slots: {}, custom_notes }` niezależnie od stanu store.
- Frontend, tryb description: `useAddToCart` w `frontend/src/hooks/useProductPageLogic.jsx` opakowuje całą logikę w `if (wizardMode !== 'description') { ... }` — pomija auto-fill, walidację „Wybierz wariant produktu" i tworzenie `wizzard_projects`.
- Frontend, tryb designer: zachowane `options` z `slots[].option_id` + pełen `configuration` ze slotami.
- Backend walidacja: `AddCartItemRequest` — `options` → `nullable|array`, `options.*` bez `required` (tylko `integer, min:1`).
- Mode source: `useWizardStore.getMode(slug)` czytany w `useProductPageLogic.jsx`, toggle w `PersonalizationIntro.jsx` (bez zmian w tym commicie).

### Luki vs spec — do domknięcia

1. **Backend snapshot (spec linia 35: „bez dopisywania slotów")** — `backend/app/Services/Order/ConfigurationSnapshotBuilder.php` nie został zmieniony w commicie. Linie 28-42 nadal iterują `$product->slots` i dopisują puste sloty do snapshotu, więc w trybie description Order zapisze sloty z `null`-ami zamiast respektować `slots: {}` z payloadu.
   - **Fix:** w `build()` dodać branch — jeśli `$baseConfig['custom_notes']` jest niepuste i `$baseSlots` puste, zwróć `['slots' => [], 'custom_notes' => ...]` bez fillu z `$product->slots`.

2. **Backend service signature** — `CartService::addItem` (`backend/app/Services/CartService.php:38`) ma `array $options` (nie-nullable). Walidacja pozwala na `null`/missing, ale `CartController::addItem:82` woła `$request->options` — przy braku klucza Laravel zwraca `null`, co rzuci `TypeError`. Aktualnie frontend zawsze wysyła `{}` więc nie wybucha, ale kontrakt jest niespójny ze specem („pomiń całkowicie (backend przyjmuje)").
   - **Fix:** zmienić signature na `?array $options = []` + w controllerze `$options = $request->input('options') ?? []`.

3. **Status handoff** — po (1) i (2) zmienić `state` na `done`.

### Off-scope w commicie (do oddzielenia w follow-up commitach)
- Schema slotu zyskała `option_is_user_selected` i per-slot `custom_notes` — pasuje do TASK_20, nie 19.
- W trybie designer `useAddToCart` wymusza auto-wybór pierwszej opcji per slot + toast „Wybierz wariant produktu" — zmiana zachowania, niewymagana przez TASK_19.
- Usunięty toast „Zmiany zapisane! Wróć do koszyka?" + auto-`navigate('/cart')` — UX zmiana spoza zakresu.
- Reguła `configuration.slots.*.custom_notes` w `AddCartItemRequest.php` — pasuje do TASK_20.

### Stan repo (working tree) — triage 24 plików (2026-04-26)

Repo `apps/reczniki-haftowane`, 22 zmodyfikowane + 2 untracked. Pogrupowane pod commit-targety:

**Bucket A — TASK_19 follow-up (snapshot/cart service/endpoint/admin)**
- `backend/app/Services/Order/ConfigurationSnapshotBuilder.php` — dodaje pole `custom_notes` w `slots[*]`, ale **nie naprawia** dopisywania slotów z `$product->slots` w trybie description (luka 1 ze specu wciąż otwarta — Claude musi to dorobić).
- `backend/app/Http/Controllers/Api/V1/CartController.php` — 2 zmiany: (a) `show()` przestaje tworzyć `cart_session` przy GET (zwraca pusty kontrakt) — to UX/perf, nie 19; (b) nowa metoda `updateItem(PATCH /cart/items/{id})` — to TASK_20 (edit notatek z koszyka).
- `backend/routes/api.php` — `PATCH /cart/items/{id}`, idzie z `updateItem` (TASK_20).
- `backend/app/Http/Requests/Cart/UpdateCartItemRequest.php` (NEW) — walidacja `configuration.custom_notes`, idzie z `updateItem` (TASK_20).
- `backend/app/Filament/Resources/Orders/RelationManagers/OrderItemsRelationManager.php` — w admin pokazuje per-slot `custom_notes` (TASK_20).
- `backend/resources/views/emails/orders/confirmation.blade.php` — email confirmation pokazuje per-slot `custom_notes` (TASK_20).

**Bucket B — TASK_20 (per-slot custom_notes) i UX cleanup wokół trybów**
- `frontend/src/store/wizardStore.js` — dodaje `getMode/setMode`, `setSlotOptionAuto`, `setSlotCustomNotes`, `modeByProduct` w persist. `getMode/setMode` należy do TASK_19, reszta do TASK_20. (Uwaga: w `fd2eb6e` API tych funkcji już jest używane — to znaczy że store w working tree jest źródłowo „ten sam"; bez tego commita commit `fd2eb6e` wybucha runtime'm.)
- `frontend/src/components/cart/CartItemCard.jsx` — dodaje edytowalne pole opisu z auto-generacją (TASK_20).
- `frontend/src/components/personalization/PersonalizationStepSlot.jsx` — usuwa wewnętrzne taby Designer/Description w slot stepie (cleanup TASK_19 — toggle żyje już w intro).
- `frontend/src/components/personalization/PersonalizationFlow.jsx` — chowa topbar na intro stepie (UX, blisko TASK_19 ale opcjonalnie do osobnego commita).
- `frontend/src/api/cart.js` — `updateCartItem(id, payload)` (TASK_20).
- `frontend/src/store/cartStore.js` — akcja `updateItem` w storze (TASK_20).
- `frontend/src/hooks/useCartPageLogic.js` — usuwa `toast.success('✓ Zmiany zapisane')` (UX cleanup, opcjonalnie).
- `frontend/src/api/responseHandler.js` — fix `getResponseData` (axios `response` zamiast `response?.data`) — generyczny bugfix, najpewniej wymagany przez `addCartItem`/`updateCartItem`.

**Bucket C — wizualizacja zestawu z `option_is_user_selected` (potrzebne do TASK_19 description)**
- `frontend/src/components/shared/SetVisualization.jsx` — pomija auto-opcje (`option_is_user_selected === false`) w renderze.
- `frontend/src/components/shared/SetVisualizationIntro.jsx` — j.w.
- `frontend/src/components/shared/SlotPreviewTile.jsx` — fallback gradient gdy brak `bgUrl`.
> Bez tych 3 plików tryb description w koszyku może pokazywać podgląd „wyklikanego" ręcznika z `options` z auto-fillu — łamie kryterium akceptacji TASK_19 linia 50 („podglądy nie sugerują »wyklikanych«"). **Idą razem z TASK_19.**

**Bucket D — infra / dev environment (zupełnie poza zakresem 19/20)**
- `.env.example`, `.gitignore`, `docker-compose.yml`, `backend/.env.docker.example` (NEW) — Docker dev env.
- `frontend/vite.config.js` — proxy `/api` i `/storage` via `nginx`.
- `frontend/src/lib/cacheUrl.js`, `frontend/src/lib/storageUrl.js` — DEV vs PROD origin handling, opcjonalny `VITE_STORAGE_ORIGIN`.
- `frontend/package-lock.json` — duży diff (regeneracja).

### Rekomendowany plan commitów przed Claude'em

1. **`fix(task-19): wizard mode + auto-option visualization`** (Bucket B fragment + Bucket C) — files: `frontend/src/store/wizardStore.js` (tylko: `getMode/setMode/setSlotOptionAuto/modeByProduct/partialize`), `frontend/src/components/personalization/PersonalizationStepSlot.jsx`, `frontend/src/components/personalization/PersonalizationFlow.jsx`, `frontend/src/components/shared/SetVisualization.jsx`, `frontend/src/components/shared/SetVisualizationIntro.jsx`, `frontend/src/components/shared/SlotPreviewTile.jsx`.
   > **Problem podziału:** w wizardStore te zmiany siedzą w jednym diffie razem z `setSlotCustomNotes` (TASK_20). Łatwiej zacommitować całość jako TASK_19+20 supplement albo zrobić selektywne `git add -p`.
2. **`feat(task-20): per-slot custom_notes + cart edit endpoint`** (Bucket A fragment + Bucket B reszta) — files: `backend/app/Http/Controllers/Api/V1/CartController.php` (tylko `updateItem`), `backend/routes/api.php`, `backend/app/Http/Requests/Cart/UpdateCartItemRequest.php`, `backend/app/Filament/Resources/Orders/RelationManagers/OrderItemsRelationManager.php`, `backend/resources/views/emails/orders/confirmation.blade.php`, `backend/app/Services/Order/ConfigurationSnapshotBuilder.php` (tylko dodanie `custom_notes`), `frontend/src/store/wizardStore.js` (`setSlotCustomNotes`), `frontend/src/store/cartStore.js`, `frontend/src/api/cart.js`, `frontend/src/api/responseHandler.js`, `frontend/src/components/cart/CartItemCard.jsx`, `frontend/src/hooks/useCartPageLogic.js`.
3. **`fix(api): GET /cart should not create cart_sessions`** — `backend/app/Http/Controllers/Api/V1/CartController.php::show()` (osobny commit, niezwiązany z task'iem).
4. **`chore(devops): docker dev env + vite proxy nginx`** (Bucket D) — wszystko z infrastruktury.

Po commitach 1-4 working tree jest czyste, `fd2eb6e` da się spushować, a Claude dostaje **clean baseline** z całą obecną pracą zacommitowaną.

### Co zostaje dla Claude'a (TASK_19a/19b)

Po commitach powyżej **rzeczywiste pozostałe luki spec TASK_19** to tylko:

1. **`ConfigurationSnapshotBuilder::build()`** — branch dla pustego `slots` + niepustego `custom_notes`: nie iterować po `$product->slots`, zwrócić `['slots' => [], 'custom_notes' => $baseConfig['custom_notes'] ?? null]`. Plus: zachowanie obecne (fill z product slots) tylko gdy `$baseSlots` niepuste lub `$cartItem->options` niepuste.
2. **`CartService::addItem`** — signature `?array $options = []` + `CartController::addItem` `$request->input('options') ?? []`. Plus feature test (request bez `options`, request z `options: []`, request z `options: { "1": 5 }`).
3. **Status handoff** — `state: in-review` → `state: done`.

## Pozostałe zadania (follow-up)

- [ ] **TASK_19a — backend snapshot empty slots:** w `ConfigurationSnapshotBuilder::build()` respektować `slots: {}` w trybie description (nie dopisywać slotów z `$product->slots`). → Claude
- [ ] **TASK_19b — backend service nullable options:** `CartService::addItem` signature `?array $options = []`, controller `?? []`, dodać test feature pokrywający request bez klucza `options`. → Claude
- [x] ~~TASK_19c — wizualizacja w koszyku trybu description~~ → zacommitowane w `66c5878` (SetVisualization* + SlotPreviewTile fallback).
- [x] ~~TASK_19e — Filament admin (per-slot custom_notes)~~ → zacommitowane w `cde75e1` (TASK_20).
- [ ] **TASK_19f — handoff finalize:** po 19a+19b zmienić `state: ready-for-claude` → `state: done` i wpisać SHA finalnego commita w sekcji „Weryfikacja".

## Historia commitów wokół TASK_19 (apps/reczniki-haftowane@main)

| SHA | Commit | Rola |
|-----|--------|------|
| `fd2eb6e` | feat(task-19): implement exclusive payloads for order modes | Frontend payload + backend validation (zacommitował Claude Haiku 4.5) |
| `05b3ed1` | chore(devops): docker dev env + vite proxy nginx | Infra, niepowiązane |
| `afd77b2` | fix(api): GET /cart nie tworzy nowych cart_sessions | Bug fix, niepowiązane |
| `66c5878` | fix(task-19): wizard mode toggle + auto-option visualization | Domknięcie frontu (PersonalizationIntro toggle + visualization fallback) |
| `cde75e1` | feat(task-20): per-slot custom_notes + cart edit endpoint | TASK_20 (pokrywa też filament admin / email) |
| **TBD** | fix(task-19): backend snapshot + service nullable options | **Czeka na Claude'a (TASK_19a + 19b)** |

