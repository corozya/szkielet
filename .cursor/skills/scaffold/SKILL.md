---
name: scaffold
description: Czyta README repozytorium scaffold i instaluje wybrane integracje (MCP, agenci AI) do bieżącego projektu.
---

# scaffold Skill (Cursor)

Gdy użytkownik podaje URL do README repozytorium scaffold, pobierasz go i przeprowadzasz instalację.

## Procedura

1. Pobierz README przez WebFetch (zamień `/blob/main/` na raw URL)
2. Znajdź sekcję `## Instalacja przez agenta AI`
3. Wylistuj dostępne integracje, zapytaj które zainstalować
4. Dla każdej wybranej:
   - Pobierz pliki z `raw.githubusercontent.com/{owner}/{repo}/main/{plik}`
   - Zapisz zachowując ścieżki
   - Dla MCP: dopisz `mcp_entry` do `.cursor/mcp.json` (i innych wykrytych hostów)
5. Uruchom `setup_cmd` jeśli użytkownik wyrazi zgodę
6. Podsumuj co zainstalowano
