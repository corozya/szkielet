# Handoff: Edytor szablonu slotów + integracja z kreatorem

**Data:** 2026-05-15  
**Aktualizacja:** 2026-05-15 (sesja 2)  
**Status:** W toku — dopasowanie wizualne w toku

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

## Znane problemy do rozwiązania

### 1. Wzór haftu nie jest w slocie w kreatorze
**Objaw:** Serce renderuje się full-size na ręczniku, ignorując pozycję image slotu z szablonu.  
**Przyczyna:** Kreator używa `buildClientSvgDirect` który nakłada SVG wzoru na `0 0 800 1200` bez uwzględnienia image slotu. Kod `wrapDrawingInImageSlot()` jest zaimplementowany ale efekt na screenshotach nie widać poprawnie.  
**Do zbadania:** Czy `resolveDrawingTextSlots` poprawnie przekazuje image slot do `drawing.text_slots` przed wywołaniem SVG buildera? Sprawdzić w `EmbroideryWizardPreview.jsx` linia 35-36.

### 2. Dopasowanie SVG do ręcznika — w toku
**Objaw:** Szablon haftu pojawia się jako mała grafika w lewym-górnym rogu zdjęcia ręcznika zamiast być wyśrodkowany i dopasowany szerokością.  
**Przyczyna (zdiagnozowana):** Nakładka CSS była `w-[82%]` zamiast `w-full`, tło ręcznika używało `imageFit="contain"` (letterboxing), a SVG `viewBox` był statyczny `0 0 800 1200` zamiast zoomować do obszaru haftu.  
**Zastosowane fixes:**
- `overlayClassName="h-full w-full"` w `EmbroideryWizardPreview.jsx`
- `imageFit="cover"` w `EmbroideryPreviewStage.jsx`
- Dynamiczny `viewBox` z `drawing_position` w `wizzardClientSvg.js`
- Cały pipeline `drawing_position` od API do SVG buildera dodany
**Do weryfikacji:** Uruchomić kreator, wybrać wzór `2-names` i potwierdzić wizualnie że szablon pokrywa ręcznik.

### 3. Slot graficzny wyświetla się jako pole tekstowe w kreatorze
**Objaw:** W panelu "TREŚĆ HAFTU" pojawia się pole "GRAFIKA" z inputem tekstowym.  
**Przyczyna:** `PersonalizationStepSlot.jsx` iteruje po wszystkich slotach (w tym image) i pokazuje input dla każdego.  
**Fix:** Filtrować sloty `slot_type !== 'image'` przy renderowaniu pól tekstowych.

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

## Następne kroki (priorytet)

1. **Zweryfikować wizualnie** dopasowanie haftu do ręcznika po ostatnich fixach (problem #2 powinien być naprawiony)
2. **Skonfigurować `drawing_position`** dla `2-names` przez `app.py` — ustawić bounding box obszaru haftu (np. `x=50, y=100, w=700, h=800`) żeby SVG zoomował do właściwego miejsca
3. **Naprawić** filtrowanie image slotów w `PersonalizationStepSlot.jsx` (problem #3 — prosty fix: `slot_type !== 'image'`)
4. **Zbadać** dlaczego wzór haftu nie trafia do image slotu (`buildClientSvgDirect` + `wrapDrawingInImageSlot`) (problem #1)
5. **Przetestować** pełny flow: `app.py` → zapisz szablon+drawing_position → kreator → weryfikacja pozycji wzoru i tekstu
