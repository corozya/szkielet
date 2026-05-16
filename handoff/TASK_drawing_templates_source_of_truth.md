# TASK: Drawing templates as source of truth

## Status
- **Priority:** High
- **Type:** Backend / Frontend / Wizard / Data Model
- **Created:** 2026-05-15
- **State:** In progress

## Goal
Ustawić poprawny model danych dla kreatora haftu:
- template przechowuje sloty i układ,
- wzór haftu przechowuje tylko grafikę SVG,
- `drawing` wskazuje na `template_id`,
- frontend i `app.py` korzystają z template jako jedynego źródła slotów i pozycji.

## Problem
Obecny model miesza odpowiedzialności:
- legacy sloty siedzą w `drawing_text_slots`,
- część układu siedzi w `settings.drawing_slot_templates` i `settings.drawing_positions`,
- `slot-template/{type}` był używany jako hybryda template + svg,
- frontend potrafił pobierać sloty z niewłaściwego miejsca,
- template nie był rozdzielony od grafiki wzoru.

To powodowało rozjazdy między:
- desktopowym edytorem `tools/desktop_slot_editor/app.py`,
- backendem,
- frontendowym preview.

## Docelowy model
- `drawing_templates` trzymają układ, canvas i pozycję całego bloku.
- `drawing_template_slots` trzymają sloty per template.
- `drawings.template_id` wskazuje na template.
- `drawings.svg_code` zostaje wyłącznie grafiką wzoru.
- `settings.drawing_slot_templates` i `settings.drawing_positions` nie są już źródłem prawdy.

## Aktualny mechanizm

### 1. Desktop editor `app.py`
- `app.py` projektuje układ na canvasie i zapisuje go przez `PUT /api/v1/slot-template/{type}`.
- Zapisuje:
  - `drawing_position` jako pozycję całego bloku/template,
  - `canvas_width` / `canvas_height`,
  - `slots` jako listę placeholderów.
- Slot graficzny ma być tylko placeholderem layoutu:
  - `slot_key`
  - `slot_type`
  - `x`, `y`, `width`, `height`
  - `text_anchor`, `text_vanchor`
  - `max_chars`
  - `sort_order`
  - opcjonalne `meta`
- `app.py` nie zapisuje pełnej grafiki wzoru w template. Grafika należy do `Drawing.svg_code`.

### 2. Backend data model
- `drawing_templates`:
  - identyfikują template po `drawing_type`,
  - trzymają `name`, `canvas_width`, `canvas_height`, `drawing_position`.
- `drawing_template_slots`:
  - trzymają sloty template,
  - są powiązane przez `template_id`.
- `drawings`:
  - mają `template_id`,
  - trzymają `svg_code` jako samą grafikę wzoru,
  - nie trzymają layoutu slotów jako źródła prawdy.

### 3. API
- `GET /api/v1/slot-template/{type}` zwraca template + sloty z bazy.
- `PUT /api/v1/slot-template/{type}` zapisuje template do bazy.
- `GET /api/v1/wizzard/options` zwraca `drawings` z relacją `template.slots`.
- `GET /api/v1/wizzard/drawing/{drawing}` zwraca `drawing` z `template.slots`.

### 4. Frontend preview
- frontend wybiera konkretny rekord `drawing` z listy wzorów,
- preview renderuje:
  - `drawing.svg_code` jako samą grafikę,
  - sloty z `drawing.template.slots`,
  - bez dodatkowego składania slotów z `settings`,
  - bez pobierania template SVG jako osobnego źródła grafiki.

### 5. Render / eksport
- generator SVG/PDF używa `drawing.resolvedTextSlots()` jako wejścia do layoutu,
- `resolvedTextSlots()` preferuje `drawing.template.slots`,
- legacy `drawing_text_slots` może istnieć tylko jako awaryjny fallback podczas migracji.

## Scope of work
### Backend
- [x] Dodać migracje dla `drawing_templates` i `drawing_template_slots`.
- [x] Dodać `template_id` do `drawings`.
- [x] Przenieść dane z legacy settings / `drawing_text_slots` do nowych tabel podczas migracji.
- [x] Przepiąć `SlotTemplateController` na nowe tabele.
- [x] Przepiąć `Drawing::resolvedTextSlots()` na template slots.
- [x] Zmienić `DrawingSvgParser`, żeby nie traktował SVG wzoru jako źródła slotów.
- [x] Przepiąć `WizzardController`, `OrderResource` i pozostałe miejsca na template-based slots.
- [x] Wyciąć request frontendowy do `settings.drawing_slot_templates` / `settings.drawing_positions`.

### Desktop editor
- [ ] `tools/desktop_slot_editor/app.py` ma dalej zapisywać template przez API, bez zakładania legacy `settings` jako storage.
- [ ] Slot graficzny ma być tylko placeholderem layoutu, bez mieszania z `svg_code`.

### Frontend
- [x] Frontend renderuje wybrany `drawing.svg_code` + sloty z template.
- [x] Usunięto zależność od `settings.drawing_slot_templates` / `settings.drawing_positions` w kreatorze.
- [x] Zostawiono tylko `wizard_default_config` w settings query.
- [ ] Usunąć martwy fallback / helpery związane z legacy slot-template cache.

## Done already
- Migracja `2026_05_15_120000_create_drawing_templates_tables.php` została uruchomiona lokalnie i utworzyła tabele.
- Frontend przestał pobierać `drawing_slot_templates` i `drawing_positions` z `/api/v1/settings`.
- Backend `/api/v1/slot-template/{type}` zapisuje do tabel template.
- `DrawingSvgParser` wiąże `drawing` z `template_id`.

## Verification
- [x] W `app.py` zapis template trafia do tabel template przez API.
- [x] Kreator pokazuje poprawny wzór po zmianie `drawing`.
- [x] Preview pobiera sloty z template, nie z legacy settings.
- [x] `drawing.svg_code` nie jest pobierany jako część template layoutu.
- [x] Migracja utworzyła tabelę lokalnie na aktywnej instancji.

## Notes
- `drawing_text_slots` może zostać tylko jako historyczny fallback do usunięcia po stabilizacji.
- Po pełnym przejściu należy usunąć stare ścieżki i uprościć API, w tym martwe helpery typu legacy cache dla `slot-template`.
