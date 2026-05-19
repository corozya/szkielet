---
name: agent
description: Instaluje agenta AI lub integrację MCP do bieżącego projektu z repozytorium scaffold. Użyj /agent <nazwa> np. /agent frontend, /agent kanboard, /agent seo.
triggers: ["agent", "install-agent", "dodaj agenta", "zainstaluj agenta", "dodaj mcp", "zainstaluj integrację"]
---

# agent — Instalator integracji i agentów AI

Instaluje wybranego agenta lub integrację MCP do bieżącego projektu, pobierając konfigurację z repozytorium scaffold bez klonowania całego repo.

## Procedura

### Krok 1 — Rozpoznaj żądanie

Użytkownik wywołuje skill z nazwą: `/agent frontend`, `/agent kanboard`, `/agent seo`, `/agent backend` itp.

Wyodrębnij nazwę integracji z polecenia użytkownika.

### Krok 2 — Sprawdź lokalny manifest

```bash
cat scaffold-manifest.json 2>/dev/null || echo "brak lokalnego manifestu"
```

Jeśli plik istnieje → użyj go. Jeśli nie → przejdź do Kroku 3.

### Krok 3 — Ustal źródło scaffold (jeśli brak lokalnego manifestu)

```bash
grep SCAFFOLD_REPO .env 2>/dev/null || echo "brak SCAFFOLD_REPO"
```

Jeśli `SCAFFOLD_REPO` jest w `.env` → zostanie użyty automatycznie.
Jeśli nie → zapytaj użytkownika o URL repozytorium scaffold.

### Krok 4 — Uruchom instalację

Tryb automatyczny (gdy znamy ID integracji):
```bash
node bin/install-from-repo.js --id <nazwa>
```

Tryb interaktywny (gdy użytkownik nie podał nazwy lub chce wybrać):
```bash
npm run install-from-repo
```

### Krok 5 — Weryfikacja

Po instalacji sprawdź:

```bash
cat .claude/mcp.json
```

Dla agentów — sprawdź czy pliki zostały skopiowane:
```bash
ls agents/
```

Poinformuj użytkownika co zostało zainstalowane i jakie komendy uruchomić (np. `npm run init-kb` dla Kanboard).

## Dostępne integracje (przykłady)

| Nazwa | Typ | Opis |
|-------|-----|------|
| `frontend` | agent | React/Next.js/Vue — komponenty, UX, testy |
| `backend` | agent | PHP/Node/Python — API, baza, testy |
| `kanboard` | mcp | Zarządzanie zadaniami |
| `mysql-mcp` | mcp | Dostęp do bazy MySQL |
| `filesystem-mcp` | mcp | Dostęp do plików projektu |
| `memory-mcp` | mcp | Trwała pamięć agentów |

Lista dostępna w `scaffold-manifest.json` lub zdalnie w repo scaffold.

## Konfiguracja SCAFFOLD_REPO

Ustaw raz w `.env` żeby nie podawać URL przy każdej instalacji:
```
SCAFFOLD_REPO=twoj-github/szkielet-workflow
```

## Narzędzia

- `Bash` — uruchamianie `node bin/install-from-repo.js`
- `Read` — czytanie wyników instalacji
