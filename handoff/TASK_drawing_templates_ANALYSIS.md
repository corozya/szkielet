# Analiza: TASK_drawing_templates — Source of truth migracja

**Źródło:** `handoff/TASK_drawing_templates_source_of_truth.md`
**Data analizy:** 2026-05-16
**Status:** IN PROGRESS (analysis-only)

## Kontekst zadania

Model danych kreatora haftu: tabele `drawing_templates` i `drawing_template_slots` jako source of truth. Backend, frontend i `app.py` przepięte — większość pracy zrobiona. Pozostałe: `app.py` bez legacy settings, usunięcie martwego fallback w frontend, cleanup legacy cache helper. Uwaga: na PROD brakuje tabel (migracja tylko lokalnie).

## Typ zadania

- [x] Frontend (React/Vite)
- [x] Backend (Laravel/Filament)
- [ ] DevOps (Docker/CI-CD)

## Uwagi agentów

### Frontend (agent)

- `resolveDrawingTextSlots.js` — brak legacy kodu do usunięcia; plik jest już przepisany. `pickSlots()` czyta `drawing.template.slots` jako priorytet, a dopiero potem `drawing.text_slots` (legacy fallback). Fallback **jest nadal aktywny** w liniach 22-25 — można go usunąć gdy `drawing_text_slots` nie będzie używane produkcyjnie.
- `resolveDrawingTextOnlySlots()` (linia 84) filtruje image sloty — jest prawidłowo zaimplementowane.
- Brak wywołania `settings.drawing_slot_templates` ani `settings.drawing_positions` w `src/api/`. Frontend używa już `/api/v1/slot-template/{type}` (plik `src/api/wizzard.js` L32). Legacy settings jako źródło zostały usunięte po stronie frontendu.
- `EmbroideryWizardPreview.jsx` L36-48 — `resolveDrawingTextSlots(enriched)` zwraca **wszystkie** sloty (w tym image), a `text_slots` na resolvedDrawing zawiera je wszystkie. Kroki wizarda korzystają z `resolveDrawingTextOnlySlots` (L52) — prawidłowe.

### Backend (agent)

- Migracja `2026_05_15_120000_create_drawing_templates_tables.php` jest **additive** — tworzy dwie nowe tabele (`drawing_templates`, `drawing_template_slots`) i dodaje nullable kolumnę `template_id` do `drawings`. Nie usuwa żadnych danych. Bezpieczna do uruchomienia na prod bez okna maintenance.
- Migracja zawiera sekcję data migration — czyta `settings.drawing_slot_templates` i `drawing_text_slots` per drawing, wypełnia nowe tabele. Na prod: jeśli te settings nie istnieją lub `drawing_text_slots` są puste, templates zostaną utworzone z pustymi slotami — **wymaga weryfikacji czy dane na prod istnieją**.
- `Drawing::resolvedTextSlots()` — fallback na `drawing_text_slots` (linie 58-64 `Drawing.php`) jest nadal aktywny. Można usunąć dopiero po weryfikacji że wszystkie drawings mają `template_id` i template ma niepuste sloty.
- `SlotTemplateController::show()` GET — zwraca template z `slots` (JSON kolumna w `drawing_templates`) i `drawing_position`. Migracja `_130000_merge_drawing_template_slots_into_json` przenosi sloty z tabeli relacyjnej `drawing_template_slots` do JSON kolumny `drawing_templates.slots` i **usuwa tabelę** `drawing_template_slots`. Architektura celowa i spójna.
- `WizzardController` — `resolvedTextSlots()` używane w POST validate (linia 84) jest prawidłowe — czyta ze zrelacjonowanego template.
- Brak seedera dla `drawing_templates` — dane tworzą się przez migrację lub `app.py`.

### DevOps (agent)

- N/D

## Plan działania (Architect)

- [ ] Krok 1 (Backend): Uruchomić migrację na staging i prod (`php artisan migrate`) — weryfikacja `migrate:status` (Backend/DevOps)
- [ ] Krok 2 (Backend): Usunąć legacy fallback `drawing_text_slots` z `Drawing::resolvedTextSlots()` po stabilizacji (Backend)
- [ ] Krok 3 (Frontend): Usunąć fallback L22-25 w `resolveDrawingTextSlots.js` (`drawing.text_slots` jako secondary source) — dopiero po weryfikacji prod (Frontend)
- [ ] Krok 4 (Backend): Usunąć fallback L58-64 w `Drawing::resolvedTextSlots()` na `drawing_text_slots` — dopiero po Kroku 1+3 (Backend)
- [x] ~~Krok 5 (Desktop): `app.py` bez legacy settings~~ — agenci wskazują że `app.py` już zapisuje przez API do nowych tabel. Weryfikacja przez faktyczne uruchomienie.
- [ ] Test plan: `migrate:status` na prod → `php artisan migrate` → kreator z wzorem → weryfikacja template slots

## Pytania/Problemy

- **Migracja bezpieczna bez maintenance** — `_120000` additive, nullable kolumna, żadnych danych nie usuwa.
- **Decyzja użytkownika:** `settings.drawing_slot_templates` NIE istnieje na prod. Data migration `_120000` stworzy puste szablony. **Przed `php artisan migrate` na prod: przenieść dane z lokalnej instancji** (export JSON z lokala → import przez `app.py` lub SQL dump tabeli `settings` z tym kluczem).

## Status

READY FOR USER
