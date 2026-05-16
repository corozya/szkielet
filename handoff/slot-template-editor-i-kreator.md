# Handoff: Edytor szablonu slotów + integracja z kreatorem

**Data:** 2026-05-15  
**Aktualizacja:** 2026-05-16 (sprint 3)  
**Status:** Zamknięty — wszystkie problemy rozwiązane; prod wymaga `php artisan migrate`

---

## Kontekst i cel

Kreator haftu (frontend React) pozwala użytkownikowi wybrać wzór haftu (`drawing_type`) i spersonalizować go tekstem. Każdy `drawing_type` ma **szablon slotów** (`drawing_slot_templates` w tabeli `settings`) definiujący:

- **Slot graficzny** (`slot_type: 'image'`) — gdzie na polu produktu pojawia się wzór haftu (SVG)
- **Slot tekstowy** (`slot_type: 'text'`) — gdzie użytkownik wpisuje tekst (imię, data itp.)

Pole produktu (canvas) = **800×1200 px** (proporcje ręcznika portrait).

---

## Architektura

### Dane
- `drawing_slot_templates` (settings JSON) — szablony slotów per `drawing_type`
  - Format: `{ "1-name": [ { slot_key, slot_type, label, x, y, width, height, text_anchor, max_chars, sort_order } ] }`
- `drawing_positions` (settings JSON) — viewBox per `drawing_type`: `{ x, y, width, height }` w przestrzeni 800×1200. Gdy ustawione, SVG "zoomuje" do tego obszaru. Zapisywane przez `PUT /api/v1/slot-template/{type}` i przez desktopowy edytor `tools/desktop_slot_editor/app.py`.

### Backend
- `Drawing.resolvedTextSlots()` — zwraca sloty: najpierw per-drawing z DB, fallback na template
- `GET /api/v1/slot-template/{type}` — zwraca template + SVG wzoru (dla edytora admin)
- `PUT /api/v1/slot-template/{type}` — zapisuje template (bez auth na razie)

### Frontend kreator
- `resolveDrawingTextSlots(drawing, templates)` — source of truth: `drawing_slot_templates[drawing_type]`
- `wizzardClientSvg.js` — buduje SVG podglądu:
  - `CANVAS_W = 800`, `CANVAS_H = 1200` (proporcje ręcznika portrait — przestrzeń współrzędnych app.py i slotów)
  - Szkielety SVG (`/wizzard-templates/*.svg`) mogą mieć własny `viewBox` (np. `0 0 800 800`) — ignorowany, nadpisywany przez buildera
  - Gdy `drawing_position` ustawione → SVG `viewBox` = `"${dp.x} ${dp.y} ${dp.width} ${dp.height}"` (zoom do obszaru haftu)
  - Gdy brak `drawing_position` → fallback `viewBox="0 0 800 1200"` (cały canvas)
  - `buildClientSvgFromSkeleton()` — tryb szkieletowy (szkielet SVG jako tło layoutu)
  - `buildClientSvgDirect()` — tryb bezpośredni (wzór SVG + teksty z pozycji slotów)
  - `showSlots = true` domyślnie — ramki slotów widoczne w kreatorze
  - Slot tekstowy: niebieska ramka (`.slot-outline`)
  - Slot graficzny: zielona przerywana ramka (`.slot-outline-image`)
- **Pipeline `drawing_position`**: `api/settings.js` → `WizardPage.jsx` → `WizardProvider` (ctx) → `EmbroideryWizardPreview` → `EmbroideryPreviewStage` → `WizzardClientPreview` → `buildClientPreviewSvg`
- **Overlay CSS**: `overlayClassName="h-full w-full"` — nakładka SVG pokrywa całe zdjęcie ręcznika
- **Tło ręcznika**: `imageFit="cover"` w `EmbroideryPreviewStage` — zdjęcie wypełnia kontener bez letterboxingu

### Desktop edytor (`tools/desktop_slot_editor/app.py`)
- Tkinter GUI, uruchamia się lokalnie: `python3 tools/desktop_slot_editor/app.py --base-url http://127.0.0.1:8080 --type 2-names`
- Przestrzeń robocza: **800×1200** (portrait canvas)
- Wczytuje szablon z API (`GET /api/v1/slot-template/{type}`), wyświetla sloty jako przeciągalne/skalowalne prostokąty
- Zapisuje przez `PUT /api/v1/slot-template/{type}` — zarówno `slots` jak i `drawing_position`
- `drawing_position` = bounding box zaznaczonego obszaru haftu (używany przez frontend do viewBox SVG)
- **Nie modyfikować** — działa prawidłowo

### Admin edytor (`/admin/edit-slot-template?type=X`)
- Filament + Alpine.js
- Canvas 800×1200 (kremowe tło, proporcje ręcznika)
- Sloty drag & resize na canvasie
- Podgląd SVG wzoru wewnątrz image slotu (opacity 55%)

---

## Problemy — status

### 1. Wzór haftu w image slocie ✅ GOTOWE
`buildClientSvgDirect` poprawnie osadza drawing SVG w nested `<svg>` z pozycją image slotu gdy `getImageSlot(drawing)` zwraca slot. Pipeline: `resolveDrawingTextSlots` → `drawing.text_slots` (zawiera image slot) → `getImageSlot` → nested svg z `x/y/width/height`.

### 2. Dopasowanie SVG do ręcznika ✅ GOTOWE
Fixes zastosowane: `overlayClassName="h-full w-full"`, `imageFit="cover"`, dynamiczny `viewBox` z `drawing_position`. Pipeline kompletny.

### 3. Slot graficzny jako pole tekstowe ✅ GOTOWE
`PersonalizationStepSlot.jsx:109` filtruje `slot_type !== 'image'`.

---

## Pliki krytyczne

| Plik | Rola |
|------|------|
| `backend/resources/views/filament/pages/edit-slot-template.blade.php` | Admin edytor canvas + Alpine.js drag |
| `backend/app/Filament/Pages/EditSlotTemplate.php` | Filament page, load/save szablonu |
| `backend/app/Http/Controllers/Api/V1/SlotTemplateController.php` | API endpoint GET/PUT |
| `frontend/src/lib/wizzard/wizzardClientSvg.js` | SVG builder — `buildClientSvgDirect`, `CANVAS_W/H`, `getImageSlot` |
| `frontend/src/lib/wizzard/resolveDrawingTextSlots.js` | Resolver szablonu → sloty |
| `frontend/src/components/wizzard/EmbroideryWizardPreview.jsx` | Injectuje resolved slots do drawing |
| `frontend/src/components/personalization/PersonalizationStepSlot.jsx` | UI pól tekstowych (`showSlotFrames = true`) |

---

## Deploy na prod

```bash
php artisan migrate
```

Migracje uruchomią się w kolejności timestamps:
1. `2026_05_16_000000_seed_drawing_slot_templates_settings` — wgrywa settings (źródło danych)
2. `2026_05_15_120000_create_drawing_templates_tables` — tworzy tabele i wypełnia z settings
3. `2026_05_15_130000_merge_drawing_template_slots_into_json` — merge slots do JSON w tabeli
