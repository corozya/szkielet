---
name: zgloszenia
description: Pobiera zgłoszenia z Kanboard i tworzy zadania w handoff/ do przeanalizowania
triggers: ["pobierz", "issues", "tickets", "zgłoszenia"]
---

# Zgłoszenia — Kanboard

Pobiera wszystkie aktywne zgłoszenia (tasks) z bieżącego projektu Kanboard, wyświetla je i tworzy zadania w `handoff/` do przeanalizowania.

## Użycie

```bash
/zgloszenia
```

Wymagane:
- Zainstalowana konfiguracja: `npm run init-kb`
- Zmienna `KANBOARD_PROJECT` ustawiona w `kanboard_setup/.env`

## Przykład wyjścia

```
📋 Pobieranie zgłoszeń z projektu: RecznikiHaftowane

✓ Projekt: RechnikiHaftowane (ID: 42)
✓ Kolumny: Backlog, Ready, In Progress, Done
✓ Zgłoszeń: 12

📌 Backlog
   [1] Zaimplementować autentykację
       Przypisane: Anna Kowalska
   [2] Dodać dokumentację API
       Przypisane: Nie przypisane

📌 In Progress
   [3] Refactor bazy danych
       Przypisane: Piotr Nowak
```

## Konfiguracja

Skill automatycznie czyta z `kanboard_setup/.env`:
- `KANBOARD_URL` — endpoint JSON-RPC
- `KANBOARD_USER` — użytkownik API
- `KANBOARD_TOKEN` — token dostępu
- `KANBOARD_PROJECT` — nazwa projektu
