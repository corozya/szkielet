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
