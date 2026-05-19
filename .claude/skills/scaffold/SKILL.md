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

### Krok 3 — Zapytaj najpierw o role agentów

Pokaż tylko role agentów (nie MCP) jako listę numerowaną i zapytaj:
*"Jakich agentów potrzebujesz w tym projekcie? Podaj numery lub nazwy."*

```
1. frontend-agent   — JS, React, HTML, CSS
2. backend-agent    — PHP, Python
3. database-agent   — MySQL, MariaDB
4. seo-agent        — SEO techniczne i contentowe
5. marketing-agent  — Google Ads, GA4
6. pm-agent         — Project Manager (Kanboard)
```

### Krok 3b — Zaproponuj wymagane MCP

Na podstawie wybranych ról wylicz potrzebne integracje MCP (deduplikuj):
- frontend → filesystem-mcp
- backend → filesystem-mcp, mysql-mcp
- database → mysql-mcp
- seo → gsc-mcp
- marketing → analytics-mcp
- pm → kanboard-mcp

Powiedz: *"Na podstawie tych ról potrzebujesz: [lista]. Zainstalować wszystkie? (tak/nie/wybierz)"*

Poczekaj na potwierdzenie przed instalacją.

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
→ "Jakich agentów potrzebujesz? (lista ról)"
Użytkownik: frontend, seo
→ "Na podstawie tych ról potrzebujesz: filesystem-mcp, gsc-mcp. Zainstalować wszystkie?"
Użytkownik: tak
→ Instaluje frontend-agent + seo-agent + filesystem-mcp + gsc-mcp

Agent:
→ Pobiera mcp_servers/kanboard/server.py, scripts/run-kanboard-mcp.sh itd.
→ Zapisuje pliki
→ Patchuje .claude/mcp.json, .cursor/mcp.json
→ "Zainstalowano kanboard-mcp i frontend-agent.
   Uruchom teraz: npm run init-kb"
```
