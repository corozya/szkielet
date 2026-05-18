# Plan sprintu — reczniki-haftowane.pl

**Ostatnia aktualizacja:** 2026-05-18 (sprint 4 w toku)
**Aktywne briefy produkcyjne:** 1

---

## Logika kolejności (ważność)

1. **Wydajność (Performance)** — eliminacja lagów w kreatorze i optymalizacja renderowania (krytyczne dla UX na mobile).
2. **Backend cleanup** — zakończony; archiwalny brief w `handoff/archive/`.

---

## Backlog sprintu (od najważniejszego)

- Brak otwartego backlogu po stronie backend cleanup.
- Aktywny brief produkcyjny: `TASK_backend_frontend_inpost_geowidget.md` (oczekuje na start).

---

## Ostatnio zamknięte — Sprint 4 (2026-05-18)

| Zadanie | Uwagi |
|---------|-------|
| Podstrona galerii wzorów haftów (#5) | Zrealizowane. STATUS: DONE w pliku zadania. |
| Frontend perf: rozbicie renderu strony produktu (#4) | Zrealizowane. STATUS: DONE w pliku zadania. |
| Frontend perf: cleanup cache fontów (#2) | Zrealizowane. STATUS: DONE w pliku zadania. |
| Frontend perf: odchudzenie generowania SVG (#3) | Zrealizowane. STATUS: DONE w pliku zadania. |
| Deploy migracji Drawing Templates | Wykonano `php artisan migrate` na produkcji. Tabele i settings zsynchronizowane. |
| UX: Kreator — widoczność podglądu (#5) | Zadanie oznaczone jako nieaktualne / zrealizowane. |
| Polling płatności optimization (#1) | Zadanie oznaczone jako nieaktualne / zrealizowane. |

---

## Ostatnio zamknięte — Audyt UX (2026-05-17)

| Zadanie | Plik (Archiwum) | Uwagi |
|---------|-----------------|-------|
| UX: Kreator — overflow zakładek | `archive/TASK_001...` | Rozwiązane przez sticky GOTOWE |
| UX: Kreator — nagłówki sekcji | `archive/TASK_002...` | Dodano statyczne H3 |
| UX: Kreator — pola tekstowe | `archive/TASK_003...` | Poprawiono UX klawiatury i licznik |
| UX: Kreator — sloty i koszyk | `archive/TASK_005...` | Sticky CTA, kolory, numeracja |
| Bug: Przejdź do zakładki | `archive/TASK_006...` | Fix re-renderu panelu wzorów |

---

## Ostatnio zamknięte — Sprint 3 (2026-05-16)

| Zadanie | Plik | Uwagi |
|---------|------|-------|
| Drawing templates — seeder na prod | `migrations/2026_05_16_000000_seed_drawing_slot_templates_settings.php` | Wgrywa settings przed migrate; gotowe do `php artisan migrate` |
| Slot editor — image slot w SVG builderze | `wizzardClientSvg.js` | Już zaimplementowane poprawnie; brak zmian do zrobienia |
| Slot editor — image slot jako pole tekstowe | `PersonalizationStepSlot.jsx:109` | Już naprawione w poprzednim sprincie |

---

## Ostatnio zamknięte — Sprint 2 (2026-05-16)

| Zadanie | Commity | Uwagi |
|---------|---------|-------|
| Dead clicks + landings (P0) | `fc52380` | WeddingGiftPage cards → `/wizard/{slug}` |
| Mobile flow kreatora — Sprint 1 | `fc52380` | M7: preview padding; M4/M5/M8/M11 już były ok |
| Mobile flow kreatora — Sprint 2 | `eb9d4c2` | M1 auto-open, M2 onboarding tab, M3 collapse, drawing_position fallback |
| Mobile flow kreatora — Sprint 3 sticky CTA | `9cfb9e1` | M12 sticky DODAJ DO KOSZYKA, M14 summary order, M15 sticky checkout |
| Google → ślub paraliż (P0) | `fc52380` | ProductCard URL fix merged do sprint 1 PR |
| PageSpeed / nginx / vite (P1) | `78fd260` | robots.txt, Cache-Control immutable, gzip staging, vendor-sentry chunk |
| Slot editor drawing_position fallback | `eb9d4c2` | 1-liner fallback w wizzardClientSvg.js |

---

## Blokery / otwarte

- **UX-M9** (lazy loading wzorów): pominięte — większa zmiana, osobny sprint.
- **Kontrast kolorów** (PageSpeed a11y): wymaga inspekcji CSS — pominięte.

---

## Uwagi architektoniczne

- **Hero images:** nginx serwuje z `frontend/dist/mockups/` — pliki muszą być w `frontend/public/mockups/` żeby Vite je skopiował do dist.
