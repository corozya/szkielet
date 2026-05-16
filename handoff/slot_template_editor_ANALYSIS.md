# Analiza: slot-template-editor — Dopasowanie wizualne edytor ↔ kreator

**Źródło:** `handoff/slot-template-editor-i-kreator.md`
**Data analizy:** 2026-05-16
**Status:** IN PROGRESS (analysis-only)

## Kontekst zadania

3 znane problemy: (1) wzór haftu renderuje się full-size ignorując image slot, (2) dopasowanie SVG do ręcznika — w dużej mierze naprawione (cover, overlay, drawing_position pipeline), (3) slot graficzny pokazuje się jako pole tekstowe w kreatorze. Canvas 800×1200, desktop editor app.py działa, admin edytor Filament działa.

## Typ zadania

- [x] Frontend (React/Vite)
- [x] Backend (Laravel/Filament)
- [ ] DevOps (Docker/CI-CD)

## Uwagi agentów

### Frontend (agent)

**Problem #3 — filter image slot w PersonalizationStepSlot:**
- NAPRAWIONY. Filtr jest w `PersonalizationStepSlot.jsx` linie 108-111: `textSlots.filter((ts) => (ts.slot_type ?? ts.slotType) !== 'image' && ...)`. Nie wymaga zmian.

**Problem #1 — wrapDrawingInImageSlot (wzór renderuje full-size):**
- Funkcja `wrapDrawingInImageSlot` nie istnieje w kodzie (szukano po całym src/). Logika image slot jest w `buildClientSvgFromLayout` w `wizzardClientSvg.js` linie 228-273: pobiera image slot ze slotów drawing, tworzy zagnieżdżony `<svg>` z SVG wzoru w bounding box slotu.
- Pipeline image slot działa warunkowo: tylko jeśli drawing ma slot z `slot_type === 'image'` ORAZ `drawing.svg_code` jest valide. Jeśli drawing nie ma image slotu (np. drawing bez template lub template bez slotu image), `buildClientSvgFromLayout` zwraca `null` i fallback `buildClientSvgDirect` renderuje SVG pełno-wymiarowo w viewBox canvasu (800×1200) — to jest właśnie Problem #1.
- Diagnoza: wzory bez image slotu w template renderują SVG bezpośrednio, co może dawać efekt full-size nakładki. Fix: upewnić się że template wzoru `2-names` (i innych) ma slot `slot_type: 'image'` skonfigurowany przez `app.py`.

**Problem #2 — drawing_position pipeline:**
- `EmbroideryWizardPreview.jsx` linie 79-91 i 103-116 — `EmbroideryPreviewStage` jest wywoływany **bez `drawingPosition` prop** (prop nie jest przekazywany). Domyślna wartość to `null`.
- Pipeline drawing_position w `wizzardClientSvg.js` L202: `const position = drawingPosition ?? drawing?.drawing_position ?? drawing?.drawingPosition ?? null`. Fallback na `drawing?.drawing_position` działa — jeśli `drawing.template.drawing_position` jest dostępne w resolvedDrawing.
- Sprawdzenie: `EmbroideryWizardPreview.jsx` L36-48 — `resolvedDrawing` zawiera `...enriched` gdzie `enriched` ma `template` (przez `enrichDrawingWithTemplate`). Template z API (`/drawings` endpoint, WizzardController L24) jest ładowane z relacją `with('template')`. `DrawingTemplate` ma `drawing_position` cast jako array. Więc `drawing.template.drawing_position` powinno być dostępne — ale `wizzardClientSvg.js` czyta `drawing.drawing_position` (flat), nie `drawing.template.drawing_position`.
- **Luka:** `wizzardClientSvg.js` L202 nie zagląda do `drawing.template.drawing_position`. Jeśli drawing nie ma `drawing_position` bezpośrednio na sobie (a template ma), frame się nie wyrenderuje. Fix: w `addTemplateFrame` dodać fallback `drawing?.template?.drawing_position`.

**Czy fix #2 jest w kodzie:**
- `getWizzardDrawingTemplate` (`src/api/wizzard.js`) istnieje i jest używany w `EmbroiderySlotPreview` (shared component, nie w głównym kreatorze). Główny kreator (`EmbroideryWizardPreview`) NIE wywołuje `getWizzardDrawingTemplate` — korzysta z drawings z kontekstu (enriched przez `enrichDrawingWithTemplate`). Jeśli API `/drawings` zwraca template z `drawing_position`, to pipeline zadziała przez fallback `drawing.template.drawing_position` — ale ten fallback NIE jest w `wizzardClientSvg.js`. Fix nie jest w kodzie.

### Backend (agent)

- `WizzardController` GET drawings (L24): ładuje `with(['categories', 'template'])` — template wraz z `drawing_position` i `slots` (json) jest zwracany dla każdego drawing. Dane do kreatory są kompletne.
- `WizzardController` POST preview (L79-84): ładuje drawing `with('template')`, wywołuje `resolvedTextSlots()` — poprawnie używa template slots. Walidacja text_slots filtruje image sloty automatycznie (iteruje po `resolvedTextSlots` w L86 i sprawdza slot_key z `validated['text_slots']`). UWAGA: `resolvedTextSlots()` zwraca WSZYSTKIE sloty (w tym image), a walidacja iteruje tylko klucze z `validated['text_slots']` — nie ma ryzyka błędu dla image slotu (image nie jest w text_slots z frontu).
- Backend nie blokuje — drawing_position w DrawingTemplate jest zwracane do frontu.

### DevOps (agent)

- N/D

## Plan działania (Architect)

- [x] ~~Krok 1: Fix Problem #3~~ — filtr `slot_type !== 'image'` już istnieje w `PersonalizationStepSlot.jsx` L108-111. Nie wymaga zmian.
- [ ] Krok 2: Fix Problem #2 — `wizzardClientSvg.js` L202: dodać fallback `drawing?.template?.drawing_position` w `addTemplateFrame` (Frontend, XS)
- [ ] Krok 3: Fix Problem #1 — skonfigurować `image slot` dla wzorów przez `app.py` (`--type 2-names` i innych). Bez image slotu w template wzór renderuje full-size. To konfiguracja danych, nie zmiana kodu. (Desktop/Data)
- [ ] Krok 4: `EmbroideryWizardPreview.jsx` L79-91 — przekazać `drawingPosition` prop do `EmbroideryPreviewStage` (lub polegać na naprawionym fallbacku z kroku 2) (Frontend)
- [ ] Test plan: Uruchomić kreator na staging z wzorem `2-names`: wzór haftu w image slot, pozycja z `drawing_position`, bez pola "GRAFIKA" w panelu tekstu

## Pytania/Problemy

- Problem #2 (drawing_position): fix w `wizzardClientSvg.js` jest 1-liniowy — czy wdrożyć razem z innymi lub jako osobny hotfix?
- Problem #1 (image slot): który deweloper ma dostęp do `app.py` i lokalnego backend żeby skonfigurować bounding box dla każdego wzoru?

## Status

READY FOR USER
