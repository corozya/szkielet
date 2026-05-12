# TASK: PayU — osobne credentials dla trybu sandbox

**Status**: todo  
**Priorytet**: wysoki  
**Zgłoszone**: 2026-05-12

## Problem

Obecna konfiguracja PayU (`config/payu.php`) ma **jeden** zestaw kluczy API (POS_ID, CLIENT_ID, CLIENT_SECRET, SECOND_KEY). Przełącznik `PAYU_SANDBOX=true/false` zmienia tylko endpoint, ale używa tych samych credentials.

Chcemy móc utrzymywać **osobne klucze dla sandbox i produkcji** — tak żeby środowisko stagingowe mogło działać z sandboxem bez ryzyka użycia produkcyjnych kluczy.

## Zakres zmian

### Backend

1. **`config/payu.php`** — rozszerzyć o osobną sekcję sandbox:
   ```php
   'sandbox' => env('PAYU_SANDBOX', true),
   // Produkcyjne credentials
   'pos_id'        => env('PAYU_POS_ID', ''),
   'client_id'     => env('PAYU_CLIENT_ID', ''),
   'client_secret' => env('PAYU_CLIENT_SECRET', ''),
   'second_key'    => env('PAYU_SECOND_KEY', ''),
   // Sandbox credentials (używane gdy PAYU_SANDBOX=true)
   'sandbox_pos_id'        => env('PAYU_SANDBOX_POS_ID', ''),
   'sandbox_client_id'     => env('PAYU_SANDBOX_CLIENT_ID', ''),
   'sandbox_client_secret' => env('PAYU_SANDBOX_CLIENT_SECRET', ''),
   'sandbox_second_key'    => env('PAYU_SANDBOX_SECOND_KEY', ''),
   ```

2. **Serwis PayU** — logika wyboru credentials na podstawie flagi `sandbox`:
   - Znaleźć w kodzie gdzie odczytywane są `config('payu.pos_id')` itp.
   - Dodać helper lub warunek: `if (config('payu.sandbox')) { use sandbox_* }` 

3. **`.env.example`** — dodać nowe zmienne:
   ```
   PAYU_SANDBOX_POS_ID=
   PAYU_SANDBOX_CLIENT_ID=
   PAYU_SANDBOX_CLIENT_SECRET=
   PAYU_SANDBOX_SECOND_KEY=
   ```

### Opcjonalnie: panel admina

- Jeśli istnieje panel z ustawieniami płatności — dodać widoczny indicator czy sandbox jest aktywny
- Nie dodawać możliwości włączania sandbox z panelu (to ryzykowne) — tylko wyświetlanie stanu

## Weryfikacja

- [ ] `PAYU_SANDBOX=true` + `PAYU_SANDBOX_*` ustawione → płatność testowa przechodzi przez sandbox
- [ ] `PAYU_SANDBOX=false` + `PAYU_*` ustawione → produkcja
- [ ] Brak `PAYU_SANDBOX_*` przy `PAYU_SANDBOX=true` → czytelny błąd w logach
- [ ] Logi PayU nie ujawniają produkcyjnych kluczy w trybie sandbox

## Uwagi

- Nie commitować kluczy — tylko `.env.example` z pustymi wartościami
- Staging/RPi powinien mieć `PAYU_SANDBOX=true` z sandboxowymi kluczami
- Produkcja OVH: `PAYU_SANDBOX=false` z produkcyjnymi kluczami
