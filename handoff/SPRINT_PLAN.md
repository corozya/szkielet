# Plan sprintu — reczniki-haftowane.pl

**Ostatnia aktualizacja:** 2026-05-16  
**Aktywne briefy produkcyjne:** 8 (+ 1 brief testowy workflow — poza sprintem)

---

## Logika kolejności (ważność)

1. **Ścieżka konwersji** — martwe kliknięcia i blokady w konfiguratorze / landingach (bezpośredni utracony revenue).
2. **Widoczne błędy po zakupie i przy pozyskaniu ruchu** — zepsuty podgląd na success, słaby LCP/SEO dotykają zaufania i wejść organicznych.
3. **Stabilizacja modelu danych kreatora** — dług strukturalny; bez domknięcia wraca ryzyko rozjazdów edytora vs frontend vs eksport.
4. **Mobile funnel** — duży udział ruchu mobilnego; poprawki UX kreatora podnoszą konwersję szerzej niż pojedynczy kanał presetów.
5. **Domknięcie presetów z realizacji** — funkcja w kodzie; krótki koszt operacyjny (migracja, env, E2E) odblokowuje marketing.
6. **Edytor slotów ↔ kreator (wizualnie)** — narzędzie/spójność operacyjna; ważne dla zespołu, mniejszy wpływ bezpośredni na klienta końcowego niż punkty 1–4.

---

## Backlog sprintu (od najważniejszego)

| # | Warstwa | Zadanie | Brief |
|---|---------|---------|--------|
| 1 | **P0** | Martwe kliknięcia na ścieżce konwersji (kreator + landingi) — brief ustala **P0** | `TASK_UX_clarity_session_fixes_dead_clicks_landings.md` |
| 2 | **P1** | Brak tekstu w podglądzie haftu na stronie sukcesu zamówienia | `TASK_wizard_preview_missing_text_font_issue.md` |
| 3 | **P1** | PageSpeed / LCP / robots / SEO / kontrast (wpływ na cały site) | `TASK_performance_pagespeed_optimization_benchmark.md` |
| 4 | **P2** | Drawing templates — domknięcie legacy, cleanup helperów, desktop editor | `TASK_drawing_templates_source_of_truth.md` |
| 5 | **P2** | Optymalizacja UX kreatora na mobile | `UX-mobile-kreator-optymalizacja.md` |
| 6 | **P3** | Preset linki z realizacji — migracja, `FRONTEND_URL`, test E2E | `TASK_wizard_preset_links_from_realizations.md` |
| 7 | **P3** | Dopasowanie wizualne slot-template ↔ kreator | `slot-template-editor-i-kreator.md` |
| 8 | **TBD** | Kreator: moment pobierania list katalogowych (`/drawings` itd.) vs lazy + cache | `TASK_frontend_wizard_lazy_catalog_fetch.md` |

**Poza sprintem:** `TASK_font_a1_ascender_clipping_fix.md` — brief testowy workflow; nie blokuje roadmapy produkcyjnej.

---

## Ostatnio zamknięte (brief usunięty)

- Optymalizacja pollowania statusu płatności na `/order/success` — interwał 60 s, query włączone tylko dla stanów w toku (`OrderSuccessPage.jsx`).
- Jedno źródło settingsów kreatora — `TASK_frontend_wizard_settings_single_source.md`.
- Fix pozycji canvas / szkieletów SVG — `fix-template-position-canvas-size.md`, `fix-skeleton-svg-dompurify-id.md`.
- Sprint 2026-05-14: PayU sandbox/IPN, nagłówek mobile, checkout analytics, internal mode race, analytics GA4 (double tracking, ceny, view_cart), allocator zamówień, preview override sync — wg wpisów w `README.md` sekcja „Zakończone”.

---

## Uwagi architektoniczne

- **Drawing templates** — po stabilizacji usunąć martwy fallback i legacy cache związane ze starym modelem slotów.
- **Kanboard:** śmieci z innych projektów usuwane ad hoc (np. vendelo.pl).
