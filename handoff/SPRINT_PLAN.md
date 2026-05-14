# Plan sprintu — reczniki-haftowane.pl

**Data:** 2026-05-14 | **Zadania aktywne:** 7

---

## Sprint bieżący (do 2026-05-21)

### P1 — Krytyczne / blokujące sprzedaż

| # | Zadanie | Typ | Priorytet |
|---|---------|-----|-----------|
| ~~1~~ | ~~`TASK_payu_sandbox_credentials.md`~~ | ~~Backend + DevOps~~ | ~~P1~~ ✅ done |
| ~~2~~ | ~~`TASK_backend_payu_ipn_transaction.md`~~ | ~~Backend~~ | ~~P1~~ ✅ done |
| ~~3~~ | ~~`TASK_naglowek_za_wysoki_mobile.md`~~ | ~~Frontend~~ | ~~P1~~ ✅ done |

### P2 — Bugi wpływające na jakość danych i stabilność

| # | Zadanie | Typ | Priorytet |
|---|---------|-----|-----------|
| ~~4~~ | ~~`TASK_frontend_checkout_analytics_one_shot.md`~~ | ~~Frontend~~ | ~~P2~~ ✅ done |
| ~~5~~ | ~~`TASK_frontend_internal_mode_bootstrap_race.md`~~ | ~~Frontend~~ | ~~P2~~ ✅ done |

---

## Sprint następny (od 2026-05-22)

| # | Zadanie | Typ | Priorytet |
|---|---------|-----|-----------|
| 6 | `TASK_11__bug___bug__edytuj_zam_wienie_.md` — edytuj zamówienie: prompt z mailem przy zmianie statusu | Frontend/Backend | P2 |
| 7 | `TASK_frontend_wizard_preview_override_sync.md` — synchronizacja lokalnego override podglądu kreatora | Frontend | P3 |
| 8 | `TASK_backend_order_number_allocator.md` — numeracja zamówień bez pełnego skanu tabeli | Backend | P3 |
| 9 | `TASK_frontend_wizard_settings_single_source.md` — jedno źródło settingsów kreatora | Frontend | P3 |

---

## Uwagi architektoniczne

- **PayU (#1 + #2)** — jeden backend agent, ten sam obszar kodu (`config/payu.php`, `PayUNotifyController`)
- **Analytics (#4 + #5)** — powiązane, ten sam agent frontendowy (GTM/GA4 bootstrap)
- **Wizard (#7 + #9)** — można zrównoleglić, różne komponenty, brak zależności
