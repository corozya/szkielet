---
name: start-project
description: One-command project initialization (clones app repos into apps/, adds .gitignore, runs init-kb).
triggers: ["start", "setup", "init", "start-project"]
---

# start-project — Project Initialization

Automatycznie ustawia całe środowisko: klonuje repozytoria, konfiguruje Kanboard, przygotowuje strukturę.

## Procedura

### Krok 1 — Sprawdzenie Wstępne

1. Sprawdź czy npm dependencies są zainstalowane:
   ```bash
   npm list --depth=0
   ```
   Jeśli brakuje → uruchom:
   ```bash
   npm install
   ```

2. Sprawdź czy katalog `apps/` już istnieje:
   ```bash
   ls -la apps/
   ```
   Jeśli istnieje i zawiera projekty → pomijaj Krok 2, przejdź do Kroku 3

### Krok 2 — Inicjalizacja Projektów

Uruchom setup script:

```bash
npm run start-project
```

Script będzie prosić o:
1. Git URLs repozytoriów do pobrania (jeden URL na linijkę)
2. Aby skończyć — wcisnąć Enter na pustej linii

Każde repozytorium będzie:
- ✅ Sklonowane do `apps/<nazwa-repo>/`
- ✅ Dodane do `.gitignore`
- ✅ Zarejestrowane w `apps/PROJECTS.json`

### Krok 3 — Konfiguracja Kanboard

Po pobraniu repozytoriów, automatycznie uruchomi się `/init-kb`:

1. Podaj dane dostępu Kanboard:
   - `KANBOARD_URL` — np. `https://kb-wom.strefakobiet.pl/jsonrpc.php`
   - `KANBOARD_USER` — użytkownik API
   - `KANBOARD_TOKEN` — token dostępu
   - `KANBOARD_PROJECT` — nazwa projektu w Kanboard

2. Script testuje połączenie i zapisuje do `kanboard_setup/.env`

### Krok 4 — Weryfikacja Wyniku

Sprawdź czy struktura została utworzona:

```bash
# Czy katalogi istnieją?
ls -la apps/
ls -la kanboard_setup/

# Czy PROJECTS.json zawiera repozytoria?
cat apps/PROJECTS.json

# Czy Kanboard config istnieje?
cat kanboard_setup/.env
```

Powinni Ci widnieć:
- ✅ Katalog `apps/` z podkatalogami projektów
- ✅ Plik `apps/PROJECTS.json` z listą projektów
- ✅ Plik `kanboard_setup/.env` z konfiguracją (NIE COMMITUJ!)

## Output Struktura

```
projekt-root/
├── apps/
│   ├── PROJECTS.json          (metadata projektów)
│   ├── reczniki-haftowane/    (klonowany projekt)
│   ├── inna-aplikacja/        (jeśli byla urlami)
│   └── ...
├── kanboard_setup/
│   ├── .env                   (sekrety — .gitignore)
│   └── .env.example           (template bez sekretów)
├── handoff/                   (tutaj przychodzą zadania)
├── node_modules/
└── ...
```

## apps/PROJECTS.json

Struktura pliku metadanych:

```json
[
  {
    "name": "reczniki-haftowane",
    "url": "https://github.com/user/reczniki-haftowane.git",
    "path": "apps/reczniki-haftowane",
    "fullPath": "/home/user/www/projekt/apps/reczniki-haftowane"
  }
]
```

**Dla agentów:** Wczytaj ten plik aby znać ścieżki do projektów:
```bash
cat apps/PROJECTS.json | jq '.[0].fullPath'
```

## Narzędzia do użycia

- `Bash` — uruchamianie npm scripts
- `Read` — czytanie PROJECTS.json i .env
- Link do `/init-kb` skill — jeśli Kanboard config wymaga ustawienia
