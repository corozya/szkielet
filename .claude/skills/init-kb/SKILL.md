---
name: init-kb
description: Initializes Kanboard config for this repo (prompts for host/user/token/project, writes kanboard_setup/.env, tests JSON-RPC).
triggers: ["init-kb", "kanboard", "init-kanboard", "configure-kb"]
---

# init-kb — Kanboard Configuration

Interaktywnie zbiera dane dostępu do Kanboard i testuje połączenie.

## Procedura

### Krok 1 — Sprawdzenie Wstępne

1. Sprawdź czy npm dependencies zainstalowane:
   ```bash
   npm list --depth=0
   ```
   Jeśli brakuje:
   ```bash
   npm install
   ```

2. Sprawdź czy `kanboard_setup/` katalog istnieje:
   ```bash
   ls -la kanboard_setup/
   ```
   Jeśli istnieje `.env` → config już istnieje, przejdź do Kroku 4

### Krok 2 — Zbieranie Danych (Tryb Interaktywny)

Uruchom skrypt:

```bash
npm run init-kb
```

Skrypt będzie pytać o:

| Parametr | Przyk. wartość | Opis |
|----------|---|---|
| **KANBOARD_URL** | `https://kb-wom.strefakobiet.pl/jsonrpc.php` | JSON-RPC endpoint Kanboard |
| **KANBOARD_USER** | `jsonrpc` | Użytkownik API |
| **KANBOARD_TOKEN** | `abc123...xyz` | Token dostępu (sekrety!) |
| **KANBOARD_PROJECT** | `RecznikiHaftowane` | Nazwa projektu (opcjonalnie) |

### Krok 3 — Testowanie Połączenia

Script automatycznie testuje JSON-RPC:

```
Test połączenia...
OK: Kanboard getVersion = v1.2.52
Zapisano: kanboard_setup/.env
```

Jeśli błąd → sprawdź czy URL, user, token są poprawne.

### Krok 4 — Weryfikacja Wyniku

Sprawdź czy config został zapisany:

```bash
cat kanboard_setup/.env
```

Powinny być widoczne:
```
KANBOARD_URL=...
KANBOARD_USER=...
KANBOARD_TOKEN=...
KANBOARD_PROJECT=...
```

✅ **Gotowe!** Config jest dostępny dla innych skillów (`/zgloszenia`, `/analiza-zadan`)

## Tryb Non-Interactive (CI/CD)

Jeśli potrzebujesz automatyzacji bez promptów:

```bash
# Opcja 1 — z hostname
node ./bin/init-kb.js \
  --host kb.example.com \
  --user jsonrpc \
  --token abc123xyz \
  --project MyProject

# Opcja 2 — z pełnym URL
node ./bin/init-kb.js \
  --url https://kb.example.com/jsonrpc.php \
  --user jsonrpc \
  --token abc123xyz

# Bez testowania połączenia
node ./bin/init-kb.js ... --no-test
```

## Bezpieczeństwo

⚠️ **WAŻNE:**

- `kanboard_setup/.env` zawiera **sekrety** — nigdy nie commituj!
- Dodaj do `.gitignore`:
  ```
  kanboard_setup/.env
  ```
- Jeśli chcesz sharować defaults (bez sekretów):
  ```bash
  cp kanboard_setup/.env kanboard_setup/.env.example
  # Usuń sekrety z .example, commituj go
  ```

## Zmienne Środowiskowe

Po skrypcie dostępne są:

```bash
source kanboard_setup/.env
echo $KANBOARD_URL
echo $KANBOARD_PROJECT
```

## Narzędzia do użycia

- `Bash` — uruchamianie `npm run init-kb`
- `Read` — czytanie `kanboard_setup/.env`
- Brak innych dependencies
