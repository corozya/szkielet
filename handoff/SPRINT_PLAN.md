# Plan sprintu — reczniki-haftowane.pl

**Data:** 2026-05-14 | **Zadania aktywne:** 3

---

## Sprint poprzedni — ZAKOŃCZONY ✅

| # | Zadanie | Typ |
|---|---------|-----|
| ~~1~~ | ~~PayU sandbox credentials~~ | ~~Backend + DevOps~~ |
| ~~2~~ | ~~PayU IPN transaction~~ | ~~Backend~~ |
| ~~3~~ | ~~Nagłówek za wysoki mobile~~ | ~~Frontend~~ |
| ~~4~~ | ~~Checkout analytics one shot~~ | ~~Frontend~~ |
| ~~5~~ | ~~Internal mode bootstrap race~~ | ~~Frontend~~ |

---

## Sprint bieżący (do 2026-05-21)

### P3 — Refaktory (sprint następny)

| # | Zadanie | Plik | Typ |
|---|---------|------|-----|
| — | Synchronizacja lokalnego override podglądu kreatora | `TASK_frontend_wizard_preview_override_sync.md` | Frontend |
| ~~—~~ | ~~Numeracja zamówień bez pełnego skanu tabeli~~ | ~~`TASK_backend_order_number_allocator.md`~~ | ~~Backend~~ ✅ done |
| — | Jedno źródło settingsów kreatora | `TASK_frontend_wizard_settings_single_source.md` | Frontend |

---

## Uwagi architektoniczne

- **KB#9 + KB#10** — wymagają dyskusji przed implementacją (opis mówi wprost "zapytaj/przedyskutuj")
- **Wizard (preview_override + settings)** — można zrównoleglić, różne komponenty, brak zależności
- **Kanboard wyczyszczony:** usunięto #3, #6, #7, #8 (śmieci z vendelo.pl)
