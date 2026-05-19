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
   7. devops-agent     — serwery, deploy, CI/CD, monitoring
   ```
   *"Jakich agentów potrzebujesz? Podaj numery lub nazwy."*

2. **Zaproponuj wymagane MCP** na podstawie wybranych ról (deduplikuj):
   - frontend → **filesystem-mcp**
   - backend → **filesystem-mcp**, **mysql-mcp**
   - database → **mysql-mcp**
   - seo → **gsc-mcp**
   - marketing → **analytics-mcp**
   - pm → **kanboard-mcp**
   - devops → **filesystem-mcp**

   *"Na podstawie tych ról potrzebujesz: [lista]. Zainstalować wszystkie?"*

3. **Instaluj** każdą wybraną pozycję:
   - Pobierz `INSTALL.md` narzędzia przez WebFetch.
     Nazwa katalogu to **krótka nazwa bez sufiksu** `-agent` lub `-mcp`:
     - Agent `seo-agent` → `agents/seo/INSTALL.md`
     - MCP `kanboard-mcp` → `mcp_servers/kanboard/INSTALL.md`
     - Agent: `https://raw.githubusercontent.com/corozya/szkielet/main/agents/{krótka-nazwa}/INSTALL.md`
     - MCP: `https://raw.githubusercontent.com/corozya/szkielet/main/mcp_servers/{krótka-nazwa}/INSTALL.md`
   - Pobierz wymienione w `Pliki:` pliki i zapisz przez Write
   - Jeśli plik istnieje — zapytaj czy nadpisać
   - Sprawdź pole `Setup:` i **przeprowadź użytkownika** przez konfigurację (zbierz brakujące dane)

4. **Dla MCP** — dopisz `mcp_entry` do wykrytych hostów AI:
   - `.claude/` → `.claude/mcp.json`
   - `.cursor/` → `.cursor/mcp.json`
   - `.gemini/` → `.gemini/settings.json`
   - `.codex/` → `mcp.json`

5. **Zależności** — jeśli `INSTALL.md` zawiera `Python deps:`, uruchom `pip install ...`

---

## Setup (ręczny)

```bash
npm install          # zależności Node.js
npm run init-kb      # konfiguracja Kanboard (URL, token)
npm run init-mcp     # kreator integracji MCP
npm run start-project  # onboarding — klonuje repo do apps/, odpala init-kb
```
