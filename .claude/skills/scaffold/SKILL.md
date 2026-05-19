# Skill: scaffold

Uruchamiany gdy użytkownik poda URL do README repozytorium scaffold
(np. `https://github.com/corozya/szkielet/blob/main/README.md`
lub `https://github.com/corozya/szkielet/`).

**Po instalacji zapisz URL repo do `.scaffold-source` w katalogu projektu** — umożliwia późniejsze `/agent` bez podawania repo.

## Procedura

### Krok 1 — Pobierz i przeczytaj README

Pobierz README przez WebFetch. Jeśli URL wskazuje na blob GitHub, zmień na raw:
`https://raw.githubusercontent.com/corozya/szkielet/main/README.md`

Wyciągnij z README:
- listę agentów (sekcje `### *-agent`)
- listę MCP (sekcje `### *-mcp`)
- mapowanie agent → wymagane MCP

### Krok 2 — Zapytaj o role agentów

Pokaż numerowaną listę i poczekaj na wybór (multi-select):

```
Jakich agentów potrzebujesz? Podaj numery (np. 1 3 5) lub nazwy:

1. frontend-agent   — JS, React, HTML, CSS
2. backend-agent    — PHP, Python
3. database-agent   — MySQL, MariaDB
4. seo-agent        — SEO techniczne i contentowe
5. marketing-agent  — Google Ads, GA4
6. pm-agent         — Project Manager (Kanboard)
7. devops-agent     — serwery, deploy, CI/CD, monitoring
```

### Krok 3 — Zaproponuj wymagane MCP

Na podstawie wybranych ról deduplikuj MCP:
- frontend → filesystem-mcp
- backend → filesystem-mcp, mysql-mcp
- database → mysql-mcp
- seo → gsc-mcp
- marketing → analytics-mcp
- pm → kanboard-mcp
- devops → filesystem-mcp

Zapytaj: *"Na podstawie tych ról potrzebujesz: [lista]. Zainstalować wszystkie?"*

### Krok 4 — Instaluj wybrane pozycje

Dla każdego wybranego agenta i MCP:

1. Pobierz `INSTALL.md` przez WebFetch:
   - Agent: `{raw_base}/agents/{nazwa}/INSTALL.md`
   - MCP: `{raw_base}/mcp_servers/{nazwa}/INSTALL.md`

2. Pobierz każdy plik z listy `Pliki:` i zapisz przez Write, zachowując ścieżki.

3. Jeśli plik już istnieje — zapytaj czy nadpisać.

### Krok 5 — Zbierz wymagane dane konfiguracyjne

Dla każdego MCP który ma sekcję `Wymagane dane:` w INSTALL.md:
- Zapytaj użytkownika o każdą brakującą wartość **po kolei**
- Nie przechodź dalej dopóki wszystkie dane nie są uzupełnione
- Utwórz plik `.env` wskazany w `Setup:` z zebranymi wartościami

### Krok 6 — Dopisz MCP entry do hostów AI

Wykryj które hosty AI są aktywne (sprawdź czy katalogi istnieją):
- `.claude/` → dopisz do `.claude/mcp.json`
- `.cursor/` → dopisz do `.cursor/mcp.json`
- `.gemini/` → dopisz do `.gemini/settings.json`
- `.codex/` → dopisz do `mcp.json`

Użyj `mcp_entry` z INSTALL.md danego MCP.
Jeśli plik konfiguracyjny nie istnieje — utwórz go z odpowiednią strukturą JSON.

### Krok 7 — Zależności pip i finalizacja

Dla każdego zainstalowanego MCP z `Python deps:` — uruchom `pip install ...`.

Zapisz URL repo do `.scaffold-source`:
```
https://github.com/corozya/szkielet
```
Dzięki temu `/agent` będzie wiedział skąd instalować kolejne narzędzia.
