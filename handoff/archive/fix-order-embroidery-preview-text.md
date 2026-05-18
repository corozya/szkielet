# Fix: Podgląd haftu w zamówieniu — brak tekstu na wygenerowanym PNG

## Status
W trakcie — przerwane przez użytkownika. Częściowo naprawione, wymaga weryfikacji na aktualnej bazie.

## Problem
W panelu admina, widok edycji zamówienia → przycisk „Wygeneruj/odśwież podglądy haftu" generuje PNG bez tekstu (tylko grafika wzoru). Tekst (imiona, daty) nie pojawia się na podglądzie.

## Przyczyna
Dwa niezależne problemy:

### 1. `buildSvgFromSkeleton` nie fallbackuje do ścieżki koordynatowej
Stare wzory mają `drawing_type` w SVG, ale nie mają `<text id="...">` placeholderów (pliki szablonów SVG usunięte w commit `889e023`). Metoda budowała SVG bez tekstu zamiast zwrócić `null` i oddać renderowanie do ścieżki koordynatowej.

**Naprawiono** w `SvgBuilderService::buildSvgFromSkeleton()` (dodany early-return null gdy brak pasujących elementów `<text id>` dla niepustych slotów).

### 2. `resolvedTextSlots()` zwraca pustą kolekcję dla wzorów bez `drawing_text_slots`
Większość wzorów (np. `2-names`: #1, #2, #3, #128 itd.) nie ma rekordów w `drawing_text_slots`. Tabela `drawing_templates` jeszcze nie istnieje (migracja nie uruchomiona). Ścieżka koordynatowa nie miała skąd wziąć współrzędnych slotów.

**Częściowo naprawiono** — dodano fallback w `Drawing::resolvedTextSlots()` do odczytu z ustawienia `drawing_slot_templates` (baza Settings) wg `drawing_type`. ALE: weryfikacja przerwana — użytkownik zgłosił, że mamy starą bazę danych.

## Co zostało zrobione

### Plik: `app/Services/Wizzard/SvgBuilderService.php`
Dodano sprawdzenie w `buildSvgFromSkeleton()` (ok. linia 252):
```php
$nonEmptyTextSlots = array_filter($textSlots, fn ($t) => trim((string) $t) !== '');
if ($nonEmptyTextSlots !== []) {
    $hasAnyMatchingElement = false;
    foreach (array_keys($nonEmptyTextSlots) as $key) {
        $nl = $xpath->query('//*[@id="' . addslashes((string) $key) . '"]');
        if ($nl !== false && $nl->length > 0) {
            $hasAnyMatchingElement = true;
            break;
        }
    }
    if (! $hasAnyMatchingElement) {
        return null;
    }
}
```

### Plik: `app/Models/Drawing.php`
Dodano import `use App\Models\Setting;` oraz trzeci fallback w `resolvedTextSlots()`:
```php
// Fallback: type-based slot templates from the drawing_slot_templates setting.
// These use the same 800×1200 coordinate space as the per-drawing slot path.
if ($this->drawing_type) {
    $all = Setting::getValue('drawing_slot_templates', []);
    $rawSlots = $all[$this->drawing_type] ?? [];
    if (!empty($rawSlots)) {
        return collect($rawSlots)
            ->map(fn (array $s) => (new DrawingTextSlot)->forceFill($s))
            ->values();
    }
}
```

## Co należy zweryfikować

1. **Czy baza zawiera rekord `drawing_slot_templates` w tabeli `settings`?**
   ```sql
   SELECT `key`, LEFT(value, 100) FROM settings WHERE `key` = 'drawing_slot_templates';
   ```
   Jeśli nie ma — sprawdź migrację `2026_05_16_000000_seed_drawing_slot_templates_settings.php` i uruchom ją.

2. **Czy kolumna `template_id` istnieje w tabeli `drawings`?**
   Jeśli nie — to normalne (migracja `drawing_templates` nie uruchomiona). Fallback do Settings działa niezależnie.

3. **Test end-to-end:**
   - Wejdź w panel admina → zamówienie z haftem → „Wygeneruj podglądy haftu"
   - Sprawdź czy wygenerowany PNG zawiera tekst + grafikę

4. **Wzory z `drawing_type: name` lub `custom`** — nie mają definicji w `drawing_slot_templates`. Wzory z `custom` mają zazwyczaj własne wpisy w `drawing_text_slots` (np. #4, #26, #132, #136). Wzory `name` mogą wymagać dodania do settings lub per-drawing slotów.

## Kontekst techniczny

- Stack: Laravel + Filament, renderowanie PNG via Imagick/librsvg
- Ścieżka: `EditOrder.php` → `OrderEmbroiderySvgExportService` → `WizzardPreviewService` → `SvgBuilderService`
- Konwersja: logi błędów z `buildSvgFromSkeleton` widoczne w laravel.log
- Tabela `drawing_text_slots` ma wpisy tylko dla: #4, #12, #26, #45, #76, #93, #94, #95, #132, #137, #141, #142
- Setting `drawing_slot_templates` zawiera szablony dla: `2-names`, `image-right`, `image-left`, `1-name`, `monogram-center`
