# Skill: agent

**Użycie:** `/agent <nazwa>` np. `/agent frontend`, `/agent kanboard`, `/agent seo`

Instaluje pojedynczego agenta lub MCP z repozytorium scaffold do bieżącego projektu.

## Procedura

### Krok 1 — Ustal URL repozytorium scaffold

Sprawdź czy istnieje plik `.scaffold-source` w katalogu projektu:
- Jeśli tak — użyj zapisanego URL jako bazy (`raw_base`)
- Jeśli nie — zapytaj użytkownika o URL repo scaffold

Przekształć URL GitHub na raw: `https://raw.githubusercontent.com/{owner}/{repo}/main`

### Krok 2 — Pobierz INSTALL.md narzędzia

Ustal typ na podstawie nazwy (suffix `-agent` → agent, `-mcp` lub nazwa MCP → mcp).

WebFetch:
- Agent: `{raw_base}/agents/{nazwa}/INSTALL.md`
- MCP: `{raw_base}/mcp_servers/{nazwa}/INSTALL.md`

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

Dla każdego pliku z `Pliki:`:
```
WebFetch: {raw_base}/{plik}
Write: zapisz pod tą samą ścieżką w projekcie
```
Jeśli plik istnieje — zapytaj czy nadpisać.

### Krok 6 — Dopisz MCP entry (tylko dla MCP)

Wykryj aktywne hosty AI i dopisz `mcp_entry` z INSTALL.md:
- `.claude/` → `.claude/mcp.json`
- `.cursor/` → `.cursor/mcp.json`
- `.gemini/` → `.gemini/settings.json`
- `.codex/` → `mcp.json`

### Krok 7 — Zależności pip

Jeśli INSTALL.md zawiera `Python deps:` — uruchom `pip install ...`.
