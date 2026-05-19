---
name: scaffold
description: Czyta README repozytorium scaffold i instaluje wybrane integracje MCP lub agentów AI do bieżącego projektu.
---

# scaffold Skill (Gemini)

Gdy użytkownik mówi "zapoznaj się z [URL README]" lub podaje link do README repozytorium scaffold — pobierasz README i przeprowadzasz instalację wybranych integracji.

## Procedura

1. **Pobierz README** przez WebFetch. Jeśli URL zawiera `/blob/`, zamień na raw: `raw.githubusercontent.com/{owner}/{repo}/main/README.md`
2. **Znajdź** sekcję `## Instalacja przez agenta AI`
3. **Zapytaj** użytkownika które integracje instalować (pokaż listę z opisami)
4. **Instaluj** każdą wybraną:
   - Pobierz pliki z `raw.githubusercontent.com`
   - Zapisz w projekcie
   - MCP: dopisz konfigurację do `.gemini/settings.json` i innych wykrytych hostów
5. **Zakończ** — poinformuj o zależnościach i krokach setup
