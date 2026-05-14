# Handoff

- tylko aktywne zadania
- najpierw czytaj brief
- jeśli jest `handoff/ASK_PROJECT_NAME.md`, dopytaj użytkownika
- po zakończeniu usuń brief z `handoff/`
- zasady: `docs/teams/COMMON.md`

## Stan zadań

### Aktywne

Pliki briefów w `handoff/` (tylko te zadania wymagają pracy):

- `TASK_payu_sandbox_credentials.md` — osobne credentials PayU dla sandbox vs produkcja (`config/payu.php`, serwis, `.env.example`).
- `TASK_naglowek_za_wysoki_mobile.md` — `/order/success`: zbyt wysoki hero na mobile, wybór płatności poniżej folda (`OrderSuccessPage.jsx`).

### Zakończone
- `TASK_email_order_cta_button.md` - `done` - CTA w mailu: `<x-mail::button>` w `confirmation.blade.php` i `confirmation-resend.blade.php` (brief usunięty 2026-05-14)
- `TASK_22_occasion_navigation_structure.md` - `done` - osobne landing pages bez zmian w headerze
- `TASK_9_ANALYSIS.md` - `done` - smoke test przechodzi
- `TASK_23_internal_mode_ga4_payu_sandbox.md` - `done` - GTM nie bootstrappuje się przed wykryciem internal mode
- `TASK_11_frontend_intro_opis_jeden_field.md` - `done` - jedno pole opisu w intro kreatora + szablon
- `TASK_19_order_modes_exclusive_payload.md` - `done` - rozłączne payloady trybu description/designer
- `TASK_20_google_merchant_feed_images.md` - `done` - feed GMC z obrazami i kategorią
- `TASK_21_benchmark_seo_ga4_pre_rebuild.md` - `done` - benchmark GSC/GA4 + `docs/urls_audit.csv`, `docs/ads_ready_phrases.md`, `docs/redirects_plan_301.md`
- `TASK_10_ANALYSIS.md` - `done` - inbox kontaktów w panelu wystarcza
- `TASK_12_frontend_fix_options_required_description_mode.md` - `done`
- `TASK_13_frontend_hide_steps_header_on_intro.md` - `done`

### Usunięte
- `TASK_sentry_frontend_production_integration.md`
