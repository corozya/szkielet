---
name: zgloszenia
description: Pobiera zgłoszenia z Kanboard i tworzy zadania w handoff/ do przeanalizowania
triggers: ["pobierz", "issues", "tickets", "zgłoszenia"]
---

# Zgłoszenia — Kanboard

Skill automatycznie pobiera wszystkie aktywne zgłoszenia (tasks) z Kanboard, wyświetla je i tworzy zadania w `handoff/` do przeanalizowania.

## Procedura

### Krok 1 — Sprawdzenie konfiguracji Kanboard

1. Sprawdź czy `kanboard_setup/.env` istnieje:
   ```bash
   ls -la kanboard_setup/.env
   ```

2. Jeśli nie istnieje → uruchom inicjalizację:
   ```bash
   npm run init-kb
   ```
   (Skill `init-kb` pobiera dane: URL, user, token, nazwa projektu)

3. Jeśli istnieje → przejdź do Kroku 2

### Krok 2 — Pobranie zgłoszeń z Kanboard

Uruchom script pobierający zgłoszenia:

```bash
npm run zgloszenia
```

Script `bin/fetch-issues.js`:
- ✅ Łączy się z Kanboard API
- ✅ Pobiera wszystkie zadania z projektu
- ✅ Wyświetla je grupując po swimlane/kolumnach
- ✅ Tworzy pliki `handoff/TASK_*.md` dla każdego zadania
- ✅ Zamyka zadania w Kanboard (jako przetworzone)

### Krok 3 — Weryfikacja wyniku

1. Sprawdź logi — czy wszystkie zadania się przechowały:
   ```bash
   ls -la handoff/TASK_*.md
   ```

2. Zwróć uwagę na output:
   - Ile zadań utworzono: `Utworzono N zadań w 'handoff/' do przeanalizowania`
   - Ile zamknięto w Kanboard: `Zamknięto N zgłoszeń w Kanboard`

3. Jeśli 0 zadań utworzono → wszystkie już istnieją w `handoff/` (nic do roboty)

### Krok 4 — Dalsze działania

Po pobraniu zgłoszeń:

- **Analiza zadań**: Uruchom `/analiza-zadan` do rozpoczynania pracy nad zadaniami
- **Tylko przegląd**: Przeczytaj pliki `TASK_*.md` ręcznie

## Konfiguracja

Skill automatycznie czyta z `kanboard_setup/.env`:
- `KANBOARD_URL` — endpoint JSON-RPC Kanboard
- `KANBOARD_USER` — login API
- `KANBOARD_TOKEN` — token dostępu
- `KANBOARD_PROJECT` — nazwa projektu do synchronizacji

**Plik nigdy nie commituj!** `kanboard_setup/.env` zawiera sekrety.

## Przykład wyjścia

```
📋 Pobieranie zgłoszeń z projektu: RecznikiHaftowane

✓ Projekt: RechnikiHaftowane (ID: 1)
✓ Swimlanes: 1
✓ Zgłoszeń: 5

  📌 Backlog (5)
   [2] [BUG] [BUG] beta.strefakobiet.pl ⚪
   [5] [OTHER] [OTHER] Nasze Realizacje — Galeria Haftów ⚪
   [9] test ⚪
   [10] [BUG] Mały ale własny — Ręczniki haftowane ⚪
   [11] [BUG] Mały ale własny — Ręczniki haftowane ⚪

✅ Utworzono 5 zadań w `handoff/` do przeanalizowania
🔒 Zamknięto 5 zgłoszeń w Kanboard
```

## Narzędzia do użycia

- `Bash` — uruchamianie npm scripts
- `Read` — sprawdzenie istniejących plików
- Link do `init-kb` skill — jeśli konfiguracja nie istnieje
