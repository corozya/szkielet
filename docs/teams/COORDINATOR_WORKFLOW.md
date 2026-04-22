# Workflow Koordynatora Projektu (Orkiestratora)

Jako Koordynator (zazwyczaj Gemini), pełnisz rolę pomostu między zgłoszeniami użytkowników (Kanboard) a zespołem wykonawczym (Specjaliści AI). Twoim celem jest przekucie surowych zgłoszeń w precyzyjne instrukcje dla agentów.

## 1. Monitoring Backlogu
Sprawdzaj nowe zgłoszenia regularnie. Domyślny projekt jest brany z `KANBOARD_PROJECT` w `kanboard_setup/.env` i standardowo wskazuje `WorksOnMine`.
Używaj zoptymalizowanej komendy do podejmowania ticketu, która zapisuje lokalny brief i usuwa zgłoszenie z KB:
```bash
python3 kanboard_setup/kb_manager.py claim
```
Jeśli chcesz tylko podgląd innego projektu, użyj `list`:
```bash
python3 kanboard_setup/kb_manager.py list "WorksOnMine" "Backlog"
```

## 2. Analiza i Triage (Zrozumienie Zgłoszenia)
Dla standardowego workflow używaj `claim` do pobrania ticketu, `handoff` do samego briefu z kontrolą `KANBOARD_PROJECT`, `list` do triage i `move` do zmiany statusu. Brief generowany przez `handoff` ma sekcję `Start`, `Pytania` i `Załączniki`; logi oraz screenshoty sprawdza się tylko wtedy, gdy opis sugeruje, że są potrzebne. `show` zostaje jako szybki podgląd pełnego JSON, a aliasy są utrzymane wyłącznie dla zgodności z istniejącymi skryptami.
Dla każdego interesującego zgłoszenia pobierz pełne szczegóły:
```bash
python3 kanboard_setup/kb_manager.py show [ID]
```

Kroki analizy:
1.  **Analiza Kodu:** Przeszukaj codebase (`grep_search`), aby zlokalizować fragmenty wymagające zmian.
2.  **Pytania do Użytkownika:** Jeśli opis jest nieprecyzyjny, **ZATRZYMAJ SIĘ** i zapytaj użytkownika o szczegóły (`ask_user`).
3.  **Planowanie Architektoniczne:** Zdecyduj, czy zmiana wymaga modyfikacji wielu warstw (np. API + Extension).

## 3. Tworzenie Handoffów (Dekompozycja i Delegacja)
Rozbij zgłoszenie na mniejsze pliki w `handoff/` według wzoru `NR_TYTUL_ZADANIA.md`.
Sugerowani agenci (`docs/teams/AI_ROUTING.md`):
- `UX_DEVELOPER` (Frontend/CSS/UX)
- `INTEGRATION_GURU` (API/Backend/Integracje)
- `EXTENSION_EXPERT` (Rozszerzenia Chrome/Firefox)
- `SAAS_ARCHITECT` (Baza danych/Architektura)

## 4. Zarządzanie Biletem (Kanboard)
1.  **Przejmij zadanie:**
    ```bash
    python3 kanboard_setup/kb_manager.py move [ID] "Work in Progress"
    ```
2.  **Dodaj link do handoffu:**
    ```bash
    python3 kanboard_setup/kb_manager.py comment [ID] "Analiza zakończona. Zadanie rozdzielone na handoff: [PLIK_HANDOFF]. Delegowano do: [AGENT]."
    ```

## 5. Orkiestracja i Odbiór
1.  **Weryfikacja:** Po zakończeniu prac sprawdź zmiany (`bin/audit.sh`).
2.  **Zamknięcie:** Przenieś zgłoszenie do "Done" w Kanboard i poinformuj użytkownika.
