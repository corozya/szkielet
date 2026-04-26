# Skill Design Guide — Procedury dla Agentów

**Każdy skill MUSI mieć procedury krok-po-kroku w SKILL.md**, nie tylko dokumentację.

## Problem

❌ **Niedostateczny SKILL.md:**
```markdown
# Mój Skill

Robi X, Y, Z.

## Użycie
/moj-skill
```

Konsekwencja: Agent musi ręcznie interpretować co robić → nieefektywny flow

---

## Rozwiązanie: 4-Krokowa Procedura

✅ **Prawidłowy SKILL.md** (wzór):

```markdown
---
name: nazwa-skilla
description: Krótki opis (1 linijka)
triggers: ["alias1", "alias2"]
---

# Tytuł Skilla

Wstępne wyjaśnienie co robi.

## Procedura

### Krok 1 — Sprawdzenie Wstępne

- Co sprawdzić (plik, config, dependencje)?
- Konkretny bash command:
  ```bash
  ls -la path/to/file
  ```
- Co zrobić jeśli nie istnieje?

### Krok 2 — Wykonanie Główne

- Jaki script uruchomić?
  ```bash
  npm run moj-script
  ```
- Co się powinno stać?
- Czego szukać w output?

### Krok 3 — Weryfikacja Wyniku

- Jak sprawdzić że operacja się powiodła?
  ```bash
  ls -la output/
  ```
- Co to znaczy "sukces"?
- Jakie błędy mogą być?

### Krok 4 — Dalsze Działania

- Co robić z wynikiem?
- Jaki następny skill uruchomić?
- Czy pushować kod do git?

## Konfiguracja

- Gdzie są zmienne (jeśli są)?
- Jakie sekrety (.env)?

## Narzędzia do użycia

- `Bash` — dla bash commandów
- `Read` — do czytania plików
- Inne tools...
```

---

## Przykład: /zgloszenia

**Stary format (❌ niedostateczny):**
```markdown
# Zgłoszenia — Kanboard

Pobiera zgłoszenia...

## Użycie
/zgloszenia

## Konfiguracja
...
```

**Nowy format (✅ procedury):**
```markdown
# Zgłoszenia — Kanboard

Skill automatycznie pobiera wszystkie zgłoszenia z Kanboard.

## Procedura

### Krok 1 — Sprawdzenie konfiguracji Kanboard

1. Sprawdź czy `kanboard_setup/.env` istnieje
2. Jeśli nie → uruchom `/init-kb`
3. Jeśli istnieje → przejdź do Kroku 2

### Krok 2 — Pobranie zgłoszeń
```bash
npm run zgloszenia
```

### Krok 3 — Weryfikacja wyniku

Sprawdź logi:
- Ile zadań utworzono?
- Ile zamknięto w Kanboard?

### Krok 4 — Dalsze działania

Uruchom `/analiza-zadan` do pracy nad zadaniami.
```

---

## Checklist: Czy Twój SKILL.md Jest Poprawny?

- [ ] Sekcja "## Procedura" istnieje
- [ ] Krok 1 — Sprawdzenie wstępne (config, dependencje)
- [ ] Krok 2 — Główna logika (scripts, API calls)
- [ ] Krok 3 — Weryfikacja (jak sprawdzić sukces)
- [ ] Krok 4 — Co dalej (następne kroki)
- [ ] Każdy krok ma konkretne bash commande
- [ ] Opisane są możliwe błędy/wyjątki
- [ ] Wskazane narzędzia (Read, Bash, Agent, etc.)

---

## Wzory (Reference)

### Wzór 1: Skill z Config Check
`analiza-zadan/SKILL.md` — 4 kroki, spawning agentów

### Wzór 2: Skill z API
`zgloszenia/SKILL.md` — Kanboard integration

### Wzór 3: Skill z Initialization
`init-kb/SKILL.md` — Collectuje dane, testuje

---

## Dla Agentów: Jak Używać

1. Przeczytaj SKILL.md procedury
2. Wykonuj po kolei: Krok 1 → 2 → 3 → 4
3. Jeśli nie możesz → dodaj pytanie do sekcji "Pytania/Problemy"

## Dla Twórców: Jak Tworzyć

1. Stwórz `.claude/skills/nazwa-skilla/SKILL.md`
2. Wypełnij 4 kroki procedury
3. Dodaj konkretne bash commande
4. Opisz możliwe problemy
5. Wskaż narzędzia

---

**Ostatnia aktualizacja:** 2026-04-26
