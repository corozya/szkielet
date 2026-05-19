# Skill: agent

**Użycie:** `/agent <nazwa>` np. `/agent frontend`, `/agent kanboard`, `/agent seo`

**Wyzwalacze:** uruchamiaj ten skill gdy użytkownik mówi:
- "zainstaluj agenta", "dodaj agenta", "zainstaluj nowego agenta"
- "zainstaluj MCP", "dodaj MCP", "dodaj integrację"
- lub używa `/agent <nazwa>` bezpośrednio

**Nigdy nie twórz plików agenta ani MCP samodzielnie** — zawsze pobieraj je z repozytorium scaffold przez WebFetch. Wymyślanie zawartości AGENT.md lub tools.json jest błędem.

Instaluje pojedynczego agenta lub MCP z repozytorium scaffold do bieżącego projektu.

## Procedura

### Krok 1 — Ustal URL repozytorium scaffold

Sprawdź czy istnieje plik `.scaffold-source` w katalogu projektu:
- Jeśli tak — użyj zapisanego URL jako bazy (`raw_base`)
- Jeśli nie — zapytaj użytkownika o URL repo scaffold

Przekształć URL GitHub na raw: `https://raw.githubusercontent.com/{owner}/{repo}/main`

### Krok 2 — Pobierz INSTALL.md narzędzia

Ustal typ na podstawie nazwy (suffix `-agent` → agent, `-mcp` lub nazwa MCP → mcp).
Katalog = krótka nazwa **bez sufiksu**: `seo-agent` → `seo`, `kanboard-mcp` → `kanboard`.

WebFetch:
- Agent: `{raw_base}/agents/{krótka-nazwa}/INSTALL.md`
- MCP: `{raw_base}/mcp_servers/{krótka-nazwa}/INSTALL.md`

### Krok 3 — Potwierdź co instalujesz

Pokaż użytkownikowi z INSTALL.md:
- opis narzędzia
- listę plików do pobrania
- wymagane MCP (jeśli to agent)
- wymagane dane konfiguracyjne (jeśli MCP)

Zapytaj: *"Zainstalować?"* (tak/nie)

### Krok 4 — Zbierz wymagane dane konfiguracyjne (jeśli MCP)

Jeśli INSTALL.md zawiera sekcję `Wymagane dane:`:
- Zapytaj użytkownika o każdą wartość **po kolei**
- Nie przechodź dalej dopóki wszystkie dane nie są uzupełnione
- Utwórz plik `.env` wskazany w `Setup:`

### Krok 5 — Instaluj pliki

**Ważne:** Każdy plik pobierasz dokładnie raz i od razu zapisujesz. Nie sprawdzaj struktury projektu przed zapisem.

Dla każdego pliku z `Pliki:`:
```
WebFetch: {raw_base}/{plik}  →  Write: zapisz pod tą samą ścieżką
```
Jeśli Write zgłosi że plik istnieje — dopiero wtedy zapytaj czy nadpisać.

### Krok 5b — Zainstaluj wymagane MCP agenta (jeśli instalujesz agenta)

Po zapisaniu plików agenta sprawdź pole `Wymaga MCP:` z INSTALL.md.
Dla każdego wymaganego MCP które **nie jest jeszcze skonfigurowane** w projekcie:

1. Zapytaj: *"Agent wymaga [nazwa-mcp]. Zainstalować?"*
2. Jeśli tak — wykonaj pełną procedurę instalacji MCP (kroki 4→7 dla tego MCP):
   - Pobierz `mcp_servers/{nazwa}/INSTALL.md`
   - Zbierz wymagane dane konfiguracyjne
   - Zapisz pliki
   - Dopisz MCP entry do hostów AI
   - Zainstaluj pip deps

Nie pomijaj tego kroku — agent bez wymaganego MCP nie będzie działał poprawnie.

### Krok 6 — Dopisz MCP entry (tylko dla MCP)

Wykryj aktywne hosty AI i dopisz `mcp_entry` z INSTALL.md:
- `.claude/` → `.claude/mcp.json`
- `.cursor/` → `.cursor/mcp.json`
- `.gemini/` → `.gemini/settings.json`
- `.codex/` → `mcp.json`

### Krok 7 — Zależności pip

Jeśli INSTALL.md zawiera `Python deps:` — uruchom `pip install ...`.
