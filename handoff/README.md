# Handoff

- tylko aktywne zadania
- najpierw czytaj brief
- jeśli jest `handoff/ASK_PROJECT_NAME.md`, dopytaj użytkownika
- po zakończeniu usuń brief z `handoff/`
- zasady: `docs/teams/COMMON.md`

## Plan sprintu

Szczegółowy plan z priorytetami: `SPRINT_PLAN.md`

## Stan zadań

### Aktywne (brief w repozytorium)

Kolejność wg ważności — szczegóły: `SPRINT_PLAN.md`.

| # | Brief | Temat |
|---|-------|--------|
| 1 | `TASK_UX_clarity_session_fixes_dead_clicks_landings.md` | UX P0: dead clicki / landings (Clarity) |
| 2 | `TASK_wizard_preview_missing_text_font_issue.md` | Brak tekstu w podglądzie haftu na success |
| 3 | `TASK_performance_pagespeed_optimization_benchmark.md` | PageSpeed / SEO / A11y |
| 4 | `TASK_drawing_templates_source_of_truth.md` | Template jako źródło prawdy (wizard); cleanup legacy |
| 5 | `UX-mobile-kreator-optymalizacja.md` | Mobile UX kreatora |
| 6 | `TASK_wizard_preset_links_from_realizations.md` | Presety z realizacji — TODO: migracja, FRONTEND_URL, E2E |
| 7 | `slot-template-editor-i-kreator.md` | Dopasowanie wizualne slot-template ↔ kreator |
| 8 | `TASK_frontend_wizard_lazy_catalog_fetch.md` | Kreator: kiedy pobierać drawings/czcionki/nici — lazy + cache |
| — | `TASK_font_a1_ascender_clipping_fix.md` | ⚠️ brief testowy workflow (nie backlog produkcyjny) |

### Zakończone (brief usunięty z `handoff/`)

- `TASK_analytics_fix_double_tracking.md` — `done` — usunięty ręczny `page_view` z `usePageTracking`; `App.jsx` nie rejestruje już RouteTracker (2026-05-14)
- `TASK_analytics_fix_ecommerce_pricing.md` — `done` — `cartItemsToGa4()` liczy premiumy z konfiguracji i używa rzeczywistej ceny jednostkowej (2026-05-14)
- `TASK_analytics_add_view_cart.md` — `done` — `trackViewCart()` + automatyczne wysyłanie na `/cart` po załadowaniu koszyka (2026-05-14)
- `TASK_payu_sandbox_credentials.md` — `done` — sandbox credentials w `config/payu.php` + `PayUService::resolveConfig()` + `.env.example` (2026-05-14)
- `TASK_backend_payu_ipn_transaction.md` — `done` — `DB::transaction()` wokół `firstOrCreate`+update w `PayUNotifyController`, 13/13 testów zielonych (2026-05-14)
- `TASK_email_order_cta_button.md` — `done` — CTA w mailu: `<x-mail::button>` w `confirmation.blade.php` i `confirmation-resend.blade.php` (brief usunięty 2026-05-14)
- `TASK_22_occasion_navigation_structure.md` — `done` — osobne landing pages bez zmian w headerze
- `TASK_9_ANALYSIS.md` — `done` — smoke test przechodzi
- `TASK_23_internal_mode_ga4_payu_sandbox.md` — `done` — GTM nie bootstrappuje się przed wykryciem internal mode
- `TASK_11_frontend_intro_opis_jeden_field.md` — `done` — jedno pole opisu w intro kreatora + szablon
- `TASK_19_order_modes_exclusive_payload.md` — `done` — rozłączne payloady trybu description/designer
- `TASK_20_google_merchant_feed_images.md` — `done` — feed GMC z obrazami i kategorią
- `TASK_21_benchmark_seo_ga4_pre_rebuild.md` — `done` — benchmark GSC/GA4 + `docs/urls_audit.csv`, `docs/ads_ready_phrases.md`, `docs/redirects_plan_301.md`
- `TASK_10_ANALYSIS.md` — `done` — inbox kontaktów w panelu wystarcza
- `TASK_12_frontend_fix_options_required_description_mode.md` — `done`
- `TASK_13_frontend_hide_steps_header_on_intro.md` — `done`
- `TASK_naglowek_za_wysoki_mobile.md` — `done` — zmniejszone padding/ikonka/typografia hero na mobile w `OrderSuccessPage.jsx` (2026-05-14)
- `TASK_frontend_checkout_analytics_one_shot.md` — `done` — `useCheckoutAnalytics` z `useRef` — eventy tylko po faktycznej zmianie selekcji, 6/6 testów (2026-05-14)
- `TASK_frontend_internal_mode_bootstrap_race.md` — `done` — `useInternalMode` czyta wyłącznie localStorage, brak drugiego fetchu i race z GTM, 4/4 testów (2026-05-14)
- `TASK_frontend_wizard_settings_single_source.md` — `done` — jedno źródło settingsów kreatora (props / WizardProvider bez duplikatu `useQuery`) (2026-05-16)
- `TASK_frontend_order_success_polling_optimization.md` — `done` — polling `payment-status` co 60 s, tylko `pending`/`initiating`; cooldown w `orderPaymentPoll` (2026-05-16)
- `fix-template-position-canvas-size.md` — `done` — pozycja slotów vs canvas w `resolveDrawingTextSlots.js` (2026-05-16)
- `fix-skeleton-svg-dompurify-id.md` — `done` — ID szkieletów SVG + ścieżki bez DOMPurify `name` clash (2026-05-16)
- `TASK_backend_order_number_allocator.md` — `done` — numeracja zamówień bez pełnego skanu (plan sprintu 2026-05-14)
- `TASK_frontend_wizard_preview_override_sync.md` — `done` — sync override podglądu (plan sprintu 2026-05-14)

### Usunięte

- `TASK_sentry_frontend_production_integration.md`
