# TASK_23 — Tryb wewnętrzny: wyłączenie GA4 + testowanie PayU sandbox

## Cel

Umożliwić zespołowi wewnętrznemu:
1. Wyłączenie wysyłania danych do GA4 podczas testów
2. Testowanie płatności w trybie PayU sandbox

Mechanizm: zalogowanie do panelu admina (Filament) wykrywa „tryb wewnętrzny" na frontendzie. Dla zwykłych użytkowników sandbox jest całkowicie niewidoczny.

## Kontekst techniczny

- **Panel admina**: Filament, `GET /admin`, auth przez Laravel guard `web` (sesja cookie)
- **Frontend**: React + Zustand, JWT auth w `auth-storage` localStorage (osobny od sesji admina)
- **GA4**: `frontend/src/utils/analytics.js` — `ANALYTICS_ENABLED` to stała, sprawdza `localStorage.getItem('disable_analytics')`; już istnieje hook, ale jest obliczany przy załadowaniu modułu (nie reaktywny)
- **PayU config**: trzymana w DB (`payment_methods.config->payu`), backend zwraca metody bez `config` (`PaymentMethodController::index()` wybiera tylko `code, name, description, is_online, sort_order`)
- **Sandbox toggle**: istnieje w panelu Filament (`config.payu.sandbox`), ale jest per-rekord w DB — dotyczy całego środowiska, nie trybu testowego

## Proponowane rozwiązanie

### Backend (Laravel)

**1. Nowy endpoint `GET /api/v1/internal-mode`**
- Brak middleware auth (zwraca gracefully false gdy niezalogowany)
- Sprawdza `Auth::guard('web')->check()` (sesja Filament)
- Zwraca `{ "internal": true|false }`
- Route w `routes/api.php` (lub dedykowany plik)

**2. Modyfikacja `PaymentMethodController::index()`**
- Jeśli `Auth::guard('web')->check()` → dołącz do odpowiedzi pole `sandbox: config->payu->sandbox` dla metody `payu`
- Dla niezalogowanych adminem: `sandbox` nie pojawia się w odpowiedzi
- Czyść cache dla admina (lub osobny cache key)

### Frontend (React)

**3. Hook `useInternalMode()` (`src/hooks/useInternalMode.js`)**
- Na mount: `GET /api/v1/internal-mode`
- Jeśli `internal: true` → `localStorage.setItem('internal_mode', 'true')`
- Jeśli `internal: false` → `localStorage.removeItem('internal_mode')`
- Eksportuje `isInternal: boolean`

**4. Montowanie hooka w `App.jsx`**
- Wywołaj `useInternalMode()` raz globalnie

**5. Poprawka `analytics.js` — dynamiczne sprawdzanie**
- Zamień stałą `ANALYTICS_ENABLED` na funkcję `isAnalyticsEnabled()`:
  ```js
  function isAnalyticsEnabled() {
    return Boolean(
      import.meta.env.PROD &&
      import.meta.env.VITE_GTM_ID &&
      import.meta.env.VITE_GTM_ENABLED !== 'false' &&
      localStorage.getItem('disable_analytics') !== 'true' &&
      localStorage.getItem('internal_mode') !== 'true'
    )
  }
  ```
- W `dataLayerPush` wywołuj `isAnalyticsEnabled()` przy każdym evenie (nie raz przy załadowaniu)

**6. Checkout — wybór sandbox**
- Jeśli `isInternal` i odpowiedź API zawiera `sandbox: true` dla metody `payu` → pokaż badge „[SANDBOX]" przy nazwie metody w kroku wyboru płatności
- Sandbox nie zmienia logiki – backend i tak używa konfiguracji z DB; chodzi o widoczność stanu dla testera

## Zakres plików

### Backend
- `routes/api.php` — nowy route `GET /internal-mode`
- `app/Http/Controllers/Api/V1/InternalModeController.php` — nowy kontroler
- `app/Http/Controllers/Api/V1/PaymentMethodController.php` — dołącz `sandbox` dla adminów

### Frontend
- `src/hooks/useInternalMode.js` — nowy hook
- `src/App.jsx` — montuj hook
- `src/utils/analytics.js` — dynamiczne `isAnalyticsEnabled()`
- `src/pages/CheckoutPage.jsx` — badge `[SANDBOX]` dla adminów

## Bezpieczeństwo

- Endpoint `/api/v1/internal-mode` nie ujawnia żadnych poufnych danych — tylko boolean
- Dane `config.payu` nigdy nie trafiają do frontendu (sekrety zostają na backendzie)
- `sandbox: true/false` to informacja publiczna (środowisko testowe widoczne tylko dla admina)

## Kryteria akceptacji

- [ ] Zalogowanie do `/admin` → odświeżenie frontendu → brak eventów GA4 w konsoli/dataLayer
- [ ] Wylogowanie z `/admin` → odświeżenie frontendu → GA4 działa normalnie
- [ ] Zalogowany admin widzi `[SANDBOX]` przy PayU gdy `config.payu.sandbox = true`
- [ ] Niezalogowany użytkownik nie widzi `[SANDBOX]` nawet jeśli zmieni localStorage ręcznie (bo sandbox pochodzi z odpowiedzi API)
- [ ] Zwykły użytkownik: brak zmian w zachowaniu

## Uwagi

- Sesja Filament (cookie `laravel_session`) działa na tej samej domenie co API — potwierdzone, cross-origin nie jest problemem
- `disable_analytics` localStorage pozostaje jako alternatywny override (zachowanie wsteczne)
