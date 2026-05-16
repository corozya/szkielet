# Plan sprintu — reczniki-haftowane.pl

**Ostatnia aktualizacja:** 2026-05-16 (sprint 2 zakończony)
**Aktywne briefy produkcyjne:** 2

---

## Logika kolejności (ważność)

1. **Ścieżka konwersji** — martwe kliknięcia, mobile flow kreatora, landing ślub z Google.
2. **Widoczne błędy i zaufanie** — PageSpeed / SEO / LCP na całym site.
3. **Stabilizacja modelu danych kreatora** — template source of truth + deploy migracji na prod.
4. **Spójność wizualna** — edytor slotów ↔ kreator.

---

## Backlog sprintu (od najważniejszego)

| # | Warstwa | Zadanie | Brief | Status |
|---|---------|---------|--------|--------|
| 1 | **P2** | Drawing templates — migracja prod + transfer danych z lokala | `TASK_drawing_templates_source_of_truth.md` | ⏳ zablokowane (dane) |
| 2 | **P3** | Dopasowanie wizualne slot-template ↔ kreator | `slot-template-editor-i-kreator.md` | ⏳ częściowo (image slot config przez app.py) |

---

## Ostatnio zamknięte — Sprint 2 (2026-05-16)

| Zadanie | Commity | Uwagi |
|---------|---------|-------|
| Dead clicks + landings (P0) | `fc52380` | WeddingGiftPage cards → `/wizard/{slug}` |
| Mobile flow kreatora (P0) — Sprint 1 | `fc52380` | M7: preview padding; M4/M5/M8/M11 już były ok |
| Mobile flow kreatora — Sprint 2 | `eb9d4c2` | M1 auto-open, M2 onboarding tab, M3 collapse, drawing_position fallback |
| Mobile flow kreatora — Sprint 3 sticky CTA | `9cfb9e1` | M12 sticky DODAJ DO KOSZYKA, M14 summary order, M15 sticky checkout |
| Google → ślub paraliż (P0) | `fc52380` | ProductCard URL fix merged do sprint 1 PR |
| PageSpeed / nginx / vite (P1) | `78fd260` | robots.txt, Cache-Control immutable, gzip staging, vendor-sentry chunk |
| Slot editor drawing_position (P3) | `eb9d4c2` | 1-liner fallback w wizzardClientSvg.js |

---

## Blokery / otwarte

- **Drawing templates prod:** `settings.drawing_slot_templates` NIE istnieje na prod. Przed `php artisan migrate` na prod przenieść dane z lokalnej instancji (export JSON → import lub SQL dump).
- **Hero images LCP:** pliki `hero-banner.jpg/webp` są tylko na serwerze — nie w repo. Główna przyczyna LCP 8.6s. Do skopiowania do `frontend/public/mockups/` i dodania do repo lub pipeline deploy.
- **UX-M9** (lazy loading wzorów): pominięte — większa zmiana, osobny sprint.
- **Kontrast kolorów** (PageSpeed a11y): wymaga inspekcji CSS — pominięte.

---

## Uwagi architektoniczne

- **Drawing templates:** na prod brak tabel `drawing_templates` — przed rolloutem UI sprawdzić `migrate:status`. Migracja additive (bezpieczna), ale data migration wymaga `settings.drawing_slot_templates` — trzeba przenieść z lokala.
- **Hero images:** nginx serwuje z `frontend/dist/mockups/` — pliki muszą być w `frontend/public/mockups/` żeby Vite je skopiował do dist.
