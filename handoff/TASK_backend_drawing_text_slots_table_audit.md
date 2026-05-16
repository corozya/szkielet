# TASK: Weryfikacja schematu bazy — tabele drawings, drawing_templates, drawing_text_slots

## Cel
Zidentyfikować, które z tabel `drawings`, `drawing_templates`, `drawing_text_slots` wymagają migracji na produkcję po ostatnich zmianach. Sprawdzić stan każdej tabeli (czy istnieje, czy ma migrację, czy jest zsynchronizowana między środowiskami).

## Kontekst
Kreator haftu obsługuje personalizację z textami przypisanymi do slotów wzoru (pola tekstowe wpisywane przez klienta). W konfiguracji produktu istnieje struktura `texts: { slot_key: value }`. Pytanie: czy mapping pól tekstowych wzoru (drawing → text slots) jest lub powinien być przechowywany w oddzielnej tabeli `drawing_text_slots`.

## Tabele do weryfikacji

### `drawings`
- Czy tabela istnieje na produkcji?
- Czy ostatnie migracje (nowe kolumny, zmiany struktury) zostały wgrane na prod?
- Czy dane są zsynchronizowane (staging → prod)?

### `drawing_templates`
- Czy tabela istnieje na produkcji?
- Czy jest objęta migracją czy była tworzona ręcznie?
- Czy zawiera dane potrzebne do działania kreatora na prod?

### `drawing_text_slots`
- Czy tabela w ogóle istnieje w schemacie (migrations, schema.sql, DB dump)?
- Czy jest używana w kodzie backendu?
- Jak działa obsługa pól tekstowych — skąd frontend wie, jakie pola tekstowe pokazać dla danego wzoru?
- Jeśli tabela nie istnieje — czy jej brak powoduje problemy (brak walidacji, hardkodowane slot_keys)?

## Zakres weryfikacji

1. Sprawdź stan migracji (`php artisan migrate:status`) na staging i prod
2. Porównaj schemat tabel między środowiskami
3. Sprawdź czy dane (drawings, drawing_templates) są na produkcji lub wymagają seeda/importu
4. Oceń, czy `drawing_text_slots` powinna być dodana do schematu

## Oczekiwany wynik

Raport w formacie tabeli:

| Tabela | Staging | Prod | Wymaga migracji? | Uwagi |
|---|---|---|---|---|
| drawings | ✓ | ? | ? | |
| drawing_templates | ✓ | ? | ? | |
| drawing_text_slots | ? | ? | ? | |

Plus rekomendacja kolejności działań przed/po deployu.

## Priorytet
Niski — weryfikacja, nie blokuje produkcji.

## Agent
Backend

## Audit result

Źródła weryfikacji:
- `php artisan migrate:status --no-ansi` na staging i prod
- `Schema::hasTable(...)`
- `Schema::getColumnListing(...)`
- kod backendu: [`Drawing::resolvedTextSlots()`](../apps/reczniki-haftowane/backend/app/Models/Drawing.php), [`DrawingTemplate`](../apps/reczniki-haftowane/backend/app/Models/DrawingTemplate.php)

### Stan środowisk

| Tabela | Staging | Prod | Wymaga migracji? | Uwagi |
|---|---|---|---|---|
| `drawings` | ✓ | ✓ | Nie dla aktualnego legacy schema | Oba środowiska mają `slot_template_key`, ale nie mają `template_id`. |
| `drawing_templates` | ✗ | ✗ | Tak, jeśli wdrażamy template source of truth | Migracje `2026_05_15_120000_create_drawing_templates_tables.php` i `2026_05_15_130000_merge_drawing_template_slots_into_json.php` nie są wdrożone. |
| `drawing_text_slots` | ✓ | ✓ | Nie dla samej tabeli; tak dla `slot_type`, jeśli potrzeba nowych typów slotów | Oba środowiska mają legacy tabelę bez kolumny `slot_type`. |

### Wnioski

1. `drawing_text_slots` jest nadal używana w backendzie jako fallback:
   - [`Drawing::resolvedTextSlots()`](/home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane/backend/app/Models/Drawing.php#L43)
   - walidacja preview: [`WizzardController`](../apps/reczniki-haftowane/backend/app/Http/Controllers/Api/V1/WizzardController.php#L83)
   - walidacja koszyka: [`AddCartItemRequest`](../apps/reczniki-haftowane/backend/app/Http/Requests/Cart/AddCartItemRequest.php#L142)
2. Nowy stack `drawing_templates` / `drawing_template_slots` istnieje w kodzie, ale nie jest jeszcze obecny na staging ani prod.
3. Staging jest ogólnie starszy od prod:
   - prod kończy się na migracji `2026_05_14_100000_add_configuration_json_to_realizations_table`
   - staging kończy się na `2026_04_16_120000_add_sort_order_to_physical_assets`

### Rekomendacja kolejności

1. Jeśli celem jest tylko utrzymanie obecnego działania, nic nie migruj dla tych tabel.
2. Jeśli celem jest rollout template source of truth:
   - najpierw `2026_05_15_100000_add_slot_type_to_drawing_text_slots.php` tylko jeśli chcesz zachować/rozszerzyć legacy mapping,
   - potem `2026_05_15_120000_create_drawing_templates_tables.php`,
   - potem `2026_05_15_130000_merge_drawing_template_slots_into_json.php`.
3. Po deployu zweryfikować, że `drawings.template_id` istnieje i że `resolvedTextSlots()` zwraca sloty z template, a nie fallback.
