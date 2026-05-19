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

### Krok 3 — Pokaż listę i pozwól wybrać kilka

Wyświetl wszystkie dostępne integracje jako listę numerowaną z opisem, np.:

```
1. kanboard-mcp     — zarządzanie zadaniami (backlog, handoff)
2. mysql-mcp        — dostęp read-only do bazy MySQL
3. filesystem-mcp   — dostęp do plików projektu
4. memory-mcp       — trwała pamięć między sesjami
5. frontend-agent   — agent React/Next.js/Vue
6. backend-agent    — agent PHP/Node/Python
```

Następnie zadaj jedno pytanie:
*"Które chcesz zainstalować? Podaj numery (np. 1, 3) lub nazwy."*

Poczekaj na odpowiedź, dopiero potem instaluj.

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
→ Wyświetla listę 6 integracji z opisami
→ "Które chcesz zainstalować? Podaj numery lub nazwy."
Użytkownik: 1, 5
→ Instaluje kanboard-mcp i frontend-agent

Agent:
→ Pobiera mcp_servers/kanboard/server.py, scripts/run-kanboard-mcp.sh itd.
→ Zapisuje pliki
→ Patchuje .claude/mcp.json, .cursor/mcp.json
→ "Zainstalowano kanboard-mcp i frontend-agent.
   Uruchom teraz: npm run init-kb"
```
