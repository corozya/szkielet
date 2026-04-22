# Instrukcja dla Agenta Gemini: Integracja z Kanboard (RPi)

Cześć! Jesteś agentem AI w projekcie, który posiada system zarządzania zgłoszeniami Kanboard na Raspberry Pi. Twoim zadaniem jest pobieranie zadań z backlogu, ich analiza i realizacja w kodzie projektu.

## Kanboard Integration

**Project Name:** WorksOnMine
**Base URL:** `https://kb-wom.strefakobiet.pl`
**Dane dostępowe:** `kanboard_setup/.env` (ładowane automatycznie, projekt przez `KANBOARD_PROJECT`)

### 1. Twoje Narzędzia (System Management)
Masz dostęp do skryptu zarządzającego zgłoszeniami na tym systemie:
`kanboard_setup/kb_manager.py`

Główne komendy to:
- `list` - lista zgłoszeń w projekcie i kolumnie
- `show` - pobranie jednego zgłoszenia
- `handoff` - zapis krótkiego briefu do `handoff/` (`handoff <id>` sprawdza `KANBOARD_PROJECT`, `--force` nadpisuje; brief zawiera blok `Pytania` i `Załączniki`, a logi/screenshoty czyta się tylko na żądanie)
- `claim` - pobranie zgłoszenia do `handoff/` i usunięcie z KB
- `move` - przeniesienie zgłoszenia

Aliasami kompatybilnosciowymi sa nadal `init`, `add-task` i `comment`, ale nie sa one potrzebne do standardowego workflow.

### 2. Sposób Pobierania Zadań
Aby dowiedzieć się, co masz teraz zrobić, wywołaj:
`python3 kanboard_setup/kb_manager.py list "NAZWA_PROJEKTU" "Backlog"`
*(Do `claim` i `handoff` projekt jest brany z `KANBOARD_PROJECT`; `list` może służyć tylko do podglądu innych projektów.)*

### 3. Twój Workflow Pracy (Standard Operacyjny)
Kiedy znajdziesz zadanie w kolumnie "Backlog":
1.  **Analiza:** Przeanalizuj tytuł i opis zadania. Sprawdź odpowiednie pliki w projekcie.
2.  **Start:** Przenieś zadanie do kolumny "In Progress":
    `python3 kanboard_setup/kb_manager.py move [ID_ZADANIA] "Work in Progress"`
3.  **Komentarz:** Poinformuj system, że zacząłeś pracę:
    `python3 kanboard_setup/kb_manager.py comment [ID_ZADANIA] "Zaczynam analizę i implementację..."`
4.  **Implementacja:** Na podstawie analizy zgłoszenia przygotuj zadania dla innych agentów  i umieść je w @HANDOVER (Opisz problem i sugestie naprawienia).
5.  **Finalizacja:** Po zakończeniu pracy skomentuj zadanie i przenieś je do kolumny "Done":
    `python3 kanboard_setup/kb_manager.py comment [ID_ZADANIA] "Zadanie zakończone pomyślnie. Zmiany wprowadzone w [NAZWA PLIKU]."`
    `python3 kanboard_setup/kb_manager.py move [ID_ZADANIA] "Done"`

### 4. Ważne Uwagi
- Jeśli kolumna "Backlog" jest pusta – czekaj na nowe zlecenia.
- Jeśli zadanie jest niejasne – zadaj pytanie użytkownikowi.
- Używaj komendy `list` regularnie, aby być na bieżąco z priorytetami.
