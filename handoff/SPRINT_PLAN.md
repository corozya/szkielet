# Plan sprintu — reczniki-haftowane.pl

**Ostatnia aktualizacja:** 2026-05-16 (sprint 3 zakończony)
**Aktywne briefy produkcyjne:** 1

---

## Logika kolejności (ważność)

1. **Ścieżka konwersji** — martwe kliknięcia, mobile flow kreatora, landing ślub z Google.
2. **Widoczne błędy i zaufanie** — PageSpeed / SEO / LCP na całym site.
3. **Stabilizacja modelu danych kreatora** — template source of truth + deploy migracji na prod.
4. **Spójność wizualna** — edytor slotów ↔ kreator.

---

## Backlog sprintu (od najważniejszego)

*Brak aktywnych zadań — wszystkie blokery rozwiązane.*

---

## Ostatnio zamknięte — Sprint 3 cont. (2026-05-16)

| Zadanie | Uwagi |
|---------|-------|
| Hero images LCP | Pliki `hero-banner.jpg/webp` już w repo od `7bed8ce` — bloker był fałszywy |

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

- **Drawing templates prod — GOTOWE DO DEPLOY:** `php artisan migrate` na prod uruchomi kolejno: `2026_05_16_000000` (wgra settings) → `2026_05_15_120000` (stworzy tabele i wypełni z settings) → `2026_05_15_130000` (merge slots do JSON).
- **UX-M9** (lazy loading wzorów): pominięte — większa zmiana, osobny sprint.
- **Kontrast kolorów** (PageSpeed a11y): wymaga inspekcji CSS — pominięte.

---

## Uwagi architektoniczne

- **Hero images:** nginx serwuje z `frontend/dist/mockups/` — pliki muszą być w `frontend/public/mockups/` żeby Vite je skopiował do dist.
