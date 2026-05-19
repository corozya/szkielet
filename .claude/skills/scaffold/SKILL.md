---
name: scaffold
description: Czyta README repozytorium scaffold podanego przez użytkownika i przeprowadza instalację wybranych integracji (MCP, agentów AI) do bieżącego projektu.
triggers: ["scaffold", "zapoznaj się z", "przeczytaj repo", "zainstaluj ze szkieletu", "setup from repo"]
---

# scaffold — Instalacja z repozytorium scaffold

Gdy użytkownik podaje URL do README repozytorium scaffold (np. `https://github.com/corozya/szkielet/blob/main/README.md`), pobierasz ten plik i postępujesz zgodnie z instrukcjami w sekcji `## Instalacja przez agenta AI`.

## Procedura

### Krok 1 — Pobierz README

Użytkownik podał URL do README. Pobierz go przez WebFetch.

Jeśli URL jest w formacie `github.com/.../blob/main/README.md`, zamień na raw:
`https://raw.githubusercontent.com/{owner}/{repo}/main/README.md`

### Krok 2 — Znajdź sekcję instalacji

W pobranym README znajdź sekcję `## Instalacja przez agenta AI`.
Ta sekcja zawiera listę dostępnych integracji z instrukcjami dla Ciebie.

### Krok 3 — Przedstaw integracje i zapytaj

Wypisz dostępne integracje z krótkim opisem i zapytaj użytkownika:
*"Które integracje chcesz zainstalować? Dostępne: [lista]"*

### Krok 4 — Zainstaluj wybrane

Dla każdej wybranej integracji postępuj dokładnie według instrukcji z README:
- Pobierz pliki przez WebFetch z raw.githubusercontent.com
- Zapisz przez Write zachowując ścieżki
- Patchuj konfiguracje MCP przez Edit (jeśli typ MCP)
- Uruchom setup_cmd przez Bash jeśli użytkownik wyrazi zgodę

### Krok 5 — Podsumuj

Powiedz co zainstalowano, które hosty AI skonfigurowano i co jeszcze trzeba zrobić.

## Przykład

```
Użytkownik: zapoznaj się z https://github.com/corozya/szkielet/blob/main/README.md

Agent:
→ WebFetch README
→ "Znalazłem 6 integracji: kanboard-mcp, mysql-mcp, filesystem-mcp,
   memory-mcp, frontend-agent, backend-agent.
   Które chcesz zainstalować?"

Użytkownik: kanboard i frontend-agent

Agent:
→ Pobiera mcp_servers/kanboard/server.py, scripts/run-kanboard-mcp.sh itd.
→ Zapisuje pliki
→ Patchuje .claude/mcp.json, .cursor/mcp.json
→ "Zainstalowano kanboard-mcp i frontend-agent.
   Uruchom teraz: npm run init-kb"
```
