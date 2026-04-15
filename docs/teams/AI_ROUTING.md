# AI Agent Routing Matrix

> Który agent AI jest preferowany do danego typu zadania, i w jakiej kolejności przy niedostępności.

## Profil mocnych stron

| Agent | Mocne strony | Słabe strony |
|-------|-------------|--------------|
| **Claude** | Złożone rozumowanie, architektura, code review, długi kontekst (200k), debugowanie | Limitowany przez okno kontekstu przy bardzo dużych plikach |
| **Gemini** | Bardzo długi kontekst (1M), analiza dużych codebases, research/SEO, parsowanie dokumentacji | Mniejsza precyzja przy złożonej logice biznesowej |
| **Codex** (GPT-4o) | Generacja kodu, boilerplate, React/JS/TS patterns, szybkie konwersje | Słabszy w architekturze systemowej, kontekst projektu |
| **Copilot** | Małe poprawki (in-IDE), PR review, DevOps scripts, security scanning, snippety | Brak kontekstu projektu bez ręcznego przekazania |

---

## Routing Matrix (Primary → Fallback)

| Zadanie | Primary | Fallback 1 | Fallback 2 |
|---------|---------|------------|------------|
| Architektura systemu | **Claude** | Gemini | Codex |

---

## Zasady przy niedostępności

1. **Sprawdź handoff/** — jeśli zadanie ma brief, każdy agent może je podjąć
2. **Wybierz fallback** z powyższej tabeli
3. **Zaznacz w handoff/** kto pracuje: `**Working: @Gemini**` (zapobiega kolizjom)
4. **Commit z inicjałem** agenta w trailerze: `Co-authored-by: Gemini <gemini@google.com>`

---

## Sygnały w handoff/ (opcjonalne)

W pliku `handoff/TASK_ID.md` można dodać:
```markdown
**Suggested AI:** Claude
**Fallback AI:** Codex
**Context size needed:** Large (use Gemini if file > 500 lines)
```

---

## Kiedy NIE delegować do danego agenta

- **Copilot** — zadania wymagające rozumienia architektury całego projektu (nie ma kontekstu)
- **Codex** — decyzje architektoniczne, zmiany cross-cutting (np. zmiana auth systemu)
- **Gemini** — bardzo specyficzna logika biznesowa (może nie znać konwencji projektu)
- **Claude** — gdy plik > 500 linii i potrzebujesz tylko mechanicznej zmiany → użyj Gemini
