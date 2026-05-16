# Handoff

- tylko aktywne zadania
- najpierw czytaj brief
- jeśli jest `handoff/ASK_PROJECT_NAME.md`, dopytaj użytkownika
- po zakończeniu usuń brief z `handoff/`
- zasady: `docs/teams/COMMON.md`

## Plan sprintu

Szczegółowy plan z priorytetami: `SPRINT_PLAN.md`

## Stan zadań

**Ostatnia weryfikacja:** 2026-05-16

### Aktywne (brief w repozytorium)

| # | Brief | Temat | Stan |
|---|-------|--------|------|
| 1 | `TASK_UX_clarity_session_fixes_dead_clicks_landings.md` | UX P0: dead clicki / landings (Clarity) | Audyt ✓, fixy w kodzie — w toku |
| 2 | `TASK_ux_wizard_mobile_panel_flow.md` | Mobile UX kreatora (UX-M1–M16, sprinty) | Do wdrożenia |
| 3 | `TASK_ux_google_prezent_na_slub_paralysis.md` | Google → landing ślub → kreator (paraliż CTA) | Analiza ✓, decyzje / wdrożenie — otwarte |
| 4 | `TASK_performance_pagespeed_optimization_benchmark.md` | PageSpeed / LCP / robots / SEO / A11y | Otwarte |
| 5 | `TASK_drawing_templates_source_of_truth.md` | Template jako źródło prawdy; cleanup legacy | Rdzeń ✓, migracja prod + cleanup — w toku |
| 6 | `slot-template-editor-i-kreator.md` | Dopasowanie wizualne slot-template ↔ kreator | W toku |

**Mikro-backlog (bez osobnego briefu):** flash podglądu w koszyku/checkout dla starych pozycji bez `drawing_template`; miniatura wzoru „osa” w małym kafelku — po lazy catalog (zamknięte 2026-05-16).

### Zakończone (brief usunięty z `handoff/`)

- `TASK_frontend_wizard_lazy_catalog_fetch.md` — `done` — lazy fetch katalogu per zakładka + prefetch + `useEmbroideryAssets({ enabled })` (2026-05-16)
- `wizard-preview-fixes-progress.md` — `done` (częściowo) — `enrichDrawingWithTemplate`, snapshot `drawing_template`, SetVisualization; reszta → mikro-backlog powyżej (2026-05-16)
- `TASK_ux_mobile_sprint1_ANALYSIS.md` — `done` — analiza Sprint 1; wdrożenie w `TASK_ux_wizard_mobile_panel_flow.md` (2026-05-16)
- `TASK_backend_drawing_text_slots_table_audit.md` — `done` — raport staging/prod vs template migrations (2026-05-16)
- `UX-mobile-kreator-optymalizacja.md` — `done` (zastąpione) — treść pokryta przez `TASK_ux_wizard_mobile_panel_flow.md` (2026-05-16)
- `TASK_font_a1_ascender_clipping_fix.md` — usunięte (brief testowy workflow, nie produkcja)
- `TASK_wizard_preview_missing_text_font_issue.md` — `done` (brief wcześniej usunięty)
- `TASK_wizard_preset_links_from_realizations.md` — `done` — `WizardPresetPage`, preset z realizacji w Filament (brief wcześniej usunięty)
- `TASK_analytics_fix_double_tracking.md` — `done` (2026-05-14)
- `TASK_analytics_fix_ecommerce_pricing.md` — `done` (2026-05-14)
- `TASK_analytics_add_view_cart.md` — `done` (2026-05-14)
- `TASK_payu_sandbox_credentials.md` — `done` (2026-05-14)
- `TASK_backend_payu_ipn_transaction.md` — `done` (2026-05-14)
- `TASK_email_order_cta_button.md` — `done` (2026-05-14)
- `TASK_22_occasion_navigation_structure.md` — `done`
- `TASK_9_ANALYSIS.md` — `done`
- `TASK_23_internal_mode_ga4_payu_sandbox.md` — `done`
- `TASK_11_frontend_intro_opis_jeden_field.md` — `done`
- `TASK_19_order_modes_exclusive_payload.md` — `done`
- `TASK_20_google_merchant_feed_images.md` — `done`
- `TASK_21_benchmark_seo_ga4_pre_rebuild.md` — `done`
- `TASK_10_ANALYSIS.md` — `done`
- `TASK_12_frontend_fix_options_required_description_mode.md` — `done`
- `TASK_13_frontend_hide_steps_header_on_intro.md` — `done`
- `TASK_naglowek_za_wysoki_mobile.md` — `done` (2026-05-14)
- `TASK_frontend_checkout_analytics_one_shot.md` — `done` (2026-05-14)
- `TASK_frontend_internal_mode_bootstrap_race.md` — `done` (2026-05-14)
- `TASK_frontend_wizard_settings_single_source.md` — `done` (2026-05-16)
- `TASK_frontend_order_success_polling_optimization.md` — `done` (2026-05-16)
- `fix-template-position-canvas-size.md` — `done` (2026-05-16)
- `fix-skeleton-svg-dompurify-id.md` — `done` (2026-05-16)
- `TASK_backend_order_number_allocator.md` — `done`
- `TASK_frontend_wizard_preview_override_sync.md` — `done`

### Usunięte

- `TASK_sentry_frontend_production_integration.md`
