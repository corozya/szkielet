# Agent Guide

Źródła prawdy:
- Zasady zespołu: `docs/teams/COMMON.md`
- Routing agentów: `docs/teams/AI_ROUTING.md`
- Aktywne zadania: `handoff/`

Workflow (minimalny):
1. Weź zadanie z `handoff/` albo stwórz nowy brief.
2. Zaimplementuj zmianę i uruchom testy w zakresie zmiany.
3. Przed commitem uruchom audyt lokalny: `bin/audit.sh` (jeśli Ollama dostępna).
4. Po zakończeniu usuń brief z `handoff/` (historia zostaje w git).

## Rola Koordynatora (Orkiestratora)

Jeśli pełnisz rolę Koordynatora (głównego agenta sesji), Twoim zadaniem jest zarządzanie cyklem życia zgłoszeń z Kanboard. 
Szczegółowa instrukcja: `docs/teams/COORDINATOR_WORKFLOW.md`

Główne obowiązki:
1. Sprawdzanie nowych zgłoszeń w Kanboard (`kb_manager.py list`).
2. Analiza i dekompozycja zgłoszeń na zadania w `handoff/`.
3. Delegowanie zadań do specjalistów zgodnie z `docs/teams/AI_ROUTING.md`.
4. Komunikacja z użytkownikiem w przypadku niejasności.

## Kanboard Integration

**Project Name:** WorksOnMine
**API Token:** `d5850f6caef3d712c91a25893083e37958886fb6192e769884c2700cce7f`
**Base URL:** `http://192.168.0.170:8080`

Użyj tych danych do tworzenia zadań, komentarzy czy zmian w Kanboard bez szukania konfiguracji.

