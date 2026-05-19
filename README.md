# Szkielet Workflow

Repozytorium narzędziowe do zarządzania projektami z agentami AI.

- `agents/` — definicje ról agentów AI
- `mcp_servers/` — lokalne serwery MCP (Kanboard, MySQL)
- `handoff/` — aktywne briefy zadań
- `docs/teams/` — instrukcje i workflow agentów
- `kanboard_setup/` — konfiguracja Kanboard

---

## Instalacja przez agenta AI

> Jesteś agentem AI (Claude, Cursor, Codex, Gemini). Użytkownik wskazał Ci ten plik.
> Postępuj zgodnie z poniższą procedurą — instaluj samodzielnie używając swoich narzędzi
> (WebFetch, Read, Write, Edit, Bash).

### Procedura

1. **Zapytaj o role agentów.** Pokaż listę i poczekaj na wybór:
   ```
   1. frontend-agent   — JS, React, HTML, CSS
   2. backend-agent    — PHP, Python
   3. database-agent   — MySQL, MariaDB
   4. seo-agent        — SEO techniczne i contentowe
   5. marketing-agent  — Google Ads, GA4
   6. pm-agent         — Project Manager (Kanboard)
   ```
   *"Jakich agentów potrzebujesz? Podaj numery lub nazwy."*

2. **Zaproponuj wymagane MCP** na podstawie wybranych ról (deduplikuj):
   - frontend → **filesystem-mcp**
   - backend → **filesystem-mcp**, **mysql-mcp**
   - database → **mysql-mcp**
   - seo → **gsc-mcp**
   - marketing → **analytics-mcp**
   - pm → **kanboard-mcp**

   *"Na podstawie tych ról potrzebujesz: [lista]. Zainstalować wszystkie?"*

3. **Instaluj** każdą wybraną pozycję:
   - Pobierz pliki przez WebFetch z `https://raw.githubusercontent.com/corozya/szkielet/main/{plik}`
   - Zapisz przez Write zachowując ścieżki
   - Jeśli plik istnieje — zapytaj czy nadpisać

4. **Dla MCP** — dopisz `mcp_entry` do wykrytych hostów AI:
   - `.claude/` → `.claude/mcp.json`
   - `.cursor/` → `.cursor/mcp.json`
   - `.gemini/` → `.gemini/settings.json`
   - `.codex/` → `mcp.json`

5. **Zależności i setup** — poinformuj o `pip install` jeśli potrzebne, zapytaj czy uruchomić `setup_cmd`.

---

### kanboard-mcp

**Typ:** MCP | **Opis:** Zarządzanie zadaniami — backlog, tworzenie, edycja, handoff briefy

**Pliki:**
- `mcp_servers/kanboard/server.py`
- `mcp_servers/kanboard/__init__.py`
- `kanboard_setup/.env.example`
- `scripts/run-kanboard-mcp.sh`
- `scripts/load-env.sh`

**MCP entry:**
```json
{ "command": "python3", "args": ["mcp_servers/kanboard/server.py"], "cwd": "." }
```
**Python deps:** `pip install fastmcp requests python-dotenv`
**Setup:** `npm run init-kb`

---

### mysql-mcp

**Typ:** MCP | **Opis:** Dostęp read-only do bazy MySQL — zapytania, schemat, diagnostyka

**Pliki:**
- `mcp_servers/mysql/server.py`
- `mcp_servers/mysql/__init__.py`
- `scripts/run-mysql-mcp.sh`
- `scripts/load-env.sh`

**MCP entry:**
```json
{ "command": "bash", "args": ["scripts/run-mysql-mcp.sh"], "cwd": "." }
```
**Python deps:** `pip install fastmcp pymysql python-dotenv`
**Setup:** uzupełnij `.env.mysql` (host, user, password, database)

---

### filesystem-mcp

**Typ:** MCP | **Opis:** Dostęp do plików projektu dla agentów AI

**Pliki:** `scripts/run-filesystem-mcp.sh`

**MCP entry:**
```json
{ "command": "bash", "args": ["scripts/run-filesystem-mcp.sh"], "cwd": "." }
```
**Setup:** brak

---

### memory-mcp

**Typ:** MCP | **Opis:** Trwała pamięć dla agentów AI między sesjami

**Pliki:** `scripts/run-memory-mcp.sh`

**MCP entry:**
```json
{ "command": "bash", "args": ["scripts/run-memory-mcp.sh"], "cwd": "." }
```
**Setup:** brak — zapisuje do `.memory/memory.jsonl`

---

### frontend-agent

**Typ:** Agent | **Opis:** JS, React, HTML, CSS — komponenty, UX, wydajność, testy E2E
**Pliki:** `agents/frontend/AGENT.md`, `agents/frontend/tools.json`
**Wymaga MCP:** filesystem-mcp

---

### backend-agent

**Typ:** Agent | **Opis:** PHP, Python — API, logika biznesowa, integracje, testy
**Pliki:** `agents/backend/AGENT.md`, `agents/backend/tools.json`
**Wymaga MCP:** filesystem-mcp, mysql-mcp

---

### database-agent

**Typ:** Agent | **Opis:** MySQL, MariaDB — schemat, zapytania, wydajność, migracje
**Pliki:** `agents/database/AGENT.md`, `agents/database/tools.json`
**Wymaga MCP:** mysql-mcp

---

### seo-agent

**Typ:** Agent | **Opis:** SEO techniczne i contentowe — GSC, indeksowanie, Core Web Vitals
**Pliki:** `agents/seo/AGENT.md`, `agents/seo/tools.json`
**Wymaga MCP:** gsc-mcp

---

### marketing-agent

**Typ:** Agent | **Opis:** Google Ads, kampanie, GA4 — planowanie, optymalizacja, raportowanie
**Pliki:** `agents/marketing/AGENT.md`, `agents/marketing/tools.json`
**Wymaga MCP:** analytics-mcp

---

### pm-agent

**Typ:** Agent | **Opis:** Project Manager — backlog, priorytety, briefy handoff, delegowanie
**Pliki:** `agents/pm/AGENT.md`, `agents/pm/tools.json`
**Wymaga MCP:** kanboard-mcp

---

## Setup (ręczny)

```bash
npm install          # zależności Node.js
npm run init-kb      # konfiguracja Kanboard (URL, token)
npm run init-mcp     # kreator integracji MCP
npm run start-project  # onboarding — klonuje repo do apps/, odpala init-kb
```
