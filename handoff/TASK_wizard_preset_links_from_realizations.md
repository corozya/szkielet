# Task: Linki z presetem kreatora generowane z realizacji

## Context

Potrzeba możliwości tworzenia gotowych linków do kreatora haftu z predefiniowaną konfiguracją zestawu (produkt, wzory, czcionki, nici, teksty). Linki mają być udostępniane klientom (FB, email, SMS) i prowadzić bezpośrednio do kreatora z wypełnionym zestawem — użytkownik zmienia tylko tekst i dodaje do koszyka.

Realizacje w bazie już trzymają konfigurację elementów (drawing_id, font_id, thread_id, text, product_id), więc to naturalne źródło presetów. Dla zestawów wieloręcznikowych dodano kolumnę `configuration JSON`.

## Zaimplementowane

### Backend

**Nowa migracja**
- `2026_05_14_100000_add_configuration_json_to_realizations_table.php`
- Dodaje kolumnę `configuration JSON nullable` do tabeli `realizations`
- Struktura: `[{label, drawing_id, font_id, thread_id, text}, ...]` — jeden element per ręcznik w zestawie
- Stare pola (`drawing_id`, `font_id`, `thread_id`, `text`) zostają jako fallback dla pojedynczych realizacji
- **Wymaga uruchomienia:** `docker compose exec php php artisan migrate`

**Model `Realization`**
- `app/Models/Realization.php` — dodano `configuration` do `$fillable` i cast `'configuration' => 'array'`

**Nowy endpoint**
- `GET /api/v1/realizations/{id}` → `RealizationController::show()`
- Zwraca pojedynczą aktywną realizację z relacjami (product, drawing, font, thread)
- `routes/api.php` — dodany route

**Nowy kontroler share**
- `app/Http/Controllers/ShareController::realization()`
- Route: `GET /share/r/{hash}` (w `routes/web.php`)
- Serwuje stronę HTML z OG meta tagami (og:title, og:description, og:image) + JS redirect do SPA
- Crawler FB/Twitter zatrzymuje się na OG HTML, prawdziwy użytkownik jest przekierowany do `/wizard/r/{hash}`
- Widok: `resources/views/share/realization.blade.php`

**API Resource**
- `app/Http/Resources/RealizationResource.php` — dodano pole `configuration` w odpowiedzi

**Filament — formularz realizacji**
- `app/Filament/Resources/Realizations/RealizationResource.php`
- Sekcja **„Produkt"**: select z `->live()` + `->afterStateUpdated()` — po wyborze produktu automatycznie pobiera jego customizable sloty (`ProductSlot`) i wypełnia Repeater odpowiednią liczbą pozycji z nazwami slotów
- Sekcja **„Konfiguracja zestawu"**: Repeater zapisywany do `configuration JSON` — każdy item zawiera: `label`, `drawing_id` (z podglądem miniatury), `font_id` (z podglądem), `thread_id` (z próbką koloru), `text`
- Sekcja **„Link do udostępnienia"**: wygenerowany URL `/share/r/{hash}` gotowy do skopiowania/wrzucenia na FB

### Frontend

**`src/lib/wizardRoutes.js`**
- `buildWizardPresetUrl(realizationId)` → `/wizard/r/{base64(id)}` — link wewnętrzny SPA (przycisk „Zamów taki zestaw")
- `buildWizardShareUrl(realizationId)` → `/share/r/{base64(id)}` — link publiczny z OG (do FB)
- `decodeWizardPresetHash(hash)` → ID realizacji
- `encodeWizardParams({drawingId, fontId, threadId, text})` → base64 JSON
- `decodeWizardPreset(searchParams)` → obiekt z parametrami

**`src/pages/WizardPresetPage.jsx`** (nowa strona)
- Trasa: `/wizard/r/:hash`
- Dekoduje hash → pobiera realizację przez API → buduje `?p=` URL z zakodowaną konfiguracją → przekierowuje do `/wizard/:slug?p=...`
- Obsługuje multi-slot (`configuration` tablica) i single-slot (stary format)

**`src/hooks/useWizardInitialization.js`**
- Po `initializeConfig` sprawdza `?p=` param i dekoduje preset
- Multi-slot: mapuje elementy tablicy na kolejne sloty produktu (po indeksie)
- Single-slot: aplikuje do pierwszego customizable slotu
- Tekst: wyszukuje pierwszy `slot_key` rysunku (potrzebuje załadowanych `drawings`)

**`src/components/products/RealizationModal.jsx`**
- Przycisk „Zamów taki zestaw" → `buildWizardPresetUrl(realization.id)` → `/wizard/r/{hash}`

**`src/App.jsx`**
- Nowa trasa `/wizard/r/:hash` → `WizardPresetPage`
- Wildcard redirect `/wizzard/*` → `/wizard/*`

**`vite.config.js`**
- Dodano `/share` do proxy (lokalny dev)

**`src/api/realizations.js`**
- Nowa funkcja `getRealizationById(id)`

**`src/components/personalization/PersonalizationFlow.jsx`**
- Przekazuje `drawings` do `useWizardInitialization` (potrzebne do slot_key dla tekstu)

## Przepływ użytkownika

```
Admin tworzy realizację (zestaw 4 ręczników)
  → wybiera produkt → Repeater auto-wypełnia 4 pozycje
  → konfiguruje każdy ręcznik (wzór, czcionka, nić, tekst)
  → kopiuje link /share/r/<hash>

Klient klika link z FB
  → Laravel /share/r/<hash> → OG HTML (FB widzi podgląd ze zdjęciem)
  → JS redirect → SPA /wizard/r/<hash>
  → WizardPresetPage pobiera realizację → /wizard/recznik-premium?p=<base64>
  → useWizardInitialization dekoduje → wypełnia 4 sloty kreatora
  → Klient zmienia tekst i dodaje do koszyka
```

## Pozostało / TODO

- [ ] Uruchomić migrację: `docker compose exec php php artisan migrate`
- [ ] Sprawdzić czy `FRONTEND_URL` jest ustawiony w `.env` backendu (potrzebny do generowania linków w Filamencie i ShareController)
- [ ] Przetestować link multi-slot end-to-end (zestaw z 4 ręcznikami)
- [ ] Rozważyć Open Graph dla strony `/wizard/r/:hash` w SPA (meta tagi przez react-helmet — działa dla użytkowników, nie dla crawlerów)

## Pliki kluczowe

| Plik | Zmiana |
|---|---|
| `backend/database/migrations/2026_05_14_100000_*.php` | Nowa migracja — `configuration JSON` |
| `backend/app/Models/Realization.php` | fillable + cast |
| `backend/app/Http/Controllers/Api/V1/RealizationController.php` | Metoda `show()` |
| `backend/app/Http/Controllers/ShareController.php` | Nowy kontroler OG share |
| `backend/resources/views/share/realization.blade.php` | Widok OG |
| `backend/routes/api.php` | Route GET realizations/{id} |
| `backend/routes/web.php` | Route GET /share/r/{hash} |
| `backend/app/Http/Resources/RealizationResource.php` | Pole configuration |
| `backend/app/Filament/Resources/Realizations/RealizationResource.php` | Repeater + auto-slot |
| `frontend/src/lib/wizardRoutes.js` | Funkcje build/decode URL |
| `frontend/src/pages/WizardPresetPage.jsx` | Nowa strona |
| `frontend/src/hooks/useWizardInitialization.js` | Multi-slot preset |
| `frontend/src/components/products/RealizationModal.jsx` | Przycisk preset |
| `frontend/src/App.jsx` | Nowe trasy |
| `frontend/vite.config.js` | Proxy /share |
| `frontend/src/api/realizations.js` | getRealizationById |
