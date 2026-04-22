# 21_TEST_PLANS_WITH_EVIDENCE (v2 - Uzupełniony)

**Status:** Planowanie / Gotowy do Implementacji
**Priorytet:** Wysoki
**Wizja:** Gemini jako "Single Source of Truth" dla gotowości wdrożeniowej (Release Readiness).

---

## 1. Cykl Życia Planu Testów (Statusy)

Zamiast prostego `is_active`, wprowadzamy pole `status` (string/enum):

1.  **DRAFT**: Tworzony przez PM. Niewidoczny dla testerów.
2.  **ACTIVE**: Publikowany. Widoczny we wtyczce jako "Aktywna Misja".
3.  **COMPLETED**: Osiągnięto zdefiniowane cele (automatycznie lub ręcznie). Wciąż widoczny we wtyczce, ale z oznaczeniem "Zadanie wykonane - dziękujemy".
4.  **ARCHIVED**: Ukryty we wtyczce. Tylko do wglądu w Dashboardzie (post-mortem).

---

## 2. Unikalność Potwierdzeń (Anti-Spam)

Aby dowód był rzetelny, ograniczamy "puste klikanie":
- **Zasada:** W ramach jednego `TestPlan`, jeden `tester_id` (lub `user_id`) może wysłać tylko **jedno skuteczne potwierdzenie `passed`**.
- **Logika:** Jeśli tester wyśle drugie `passed` z tego samego konta/tokena:
  - System **nadpisuje** poprzednie zgłoszenie (aktualizuje logi i metadane do najnowszego stanu).
  - Licznik `confirmed_count` nie zwiększa się.
- **Błędy (bugs):** Są nielimitowane – tester może zgłosić 5 różnych błędów do jednej misji.

---

## 3. Cele Platformowe (Coverage Targets)

W modelu `TestPlan` dodajemy pole `targets` (JSON), które pozwala zdefiniować wymagane pokrycie:
```json
{
  "min_total": 10,
  "requirements": [
    { "type": "browser", "value": "Safari", "min": 3 },
    { "type": "device_type", "value": "mobile", "min": 5 }
  ]
}
```
Dashboard będzie pokazywał postęp realizacji tych konkretnych "sub-celi". Plan przechodzi w `COMPLETED` dopiero po spełnieniu wszystkich warunków.

---

## 4. Bezpieczeństwo i Higiena Logów (PII Protection)

Zgłoszenia typu `passed` generują dużo danych (logi sieci/konsoli). Wprowadzamy rygorystyczne zasady:

### A. Scrubbing (Czyszczenie przed zapisem)
W `FeedbackController`, przed zapisem do bazy:
- **Headers:** Automatyczne usuwanie: `Authorization`, `Cookie`, `X-CSRF-TOKEN`.
- **URLs:** Maskowanie parametrów wrażliwych w URLach (regex): `?token=...`, `&password=...`.
- **Console:** Usuwanie linii zawierających słowa kluczowe (password, secret, key).

### B. Retencja (Oszczędność miejsca)
- Logi dla zgłoszeń `passed` są przechowywane tylko przez **30 dni** (lub do czasu ARCHIVIZACJI planu).
- Po tym czasie logi są usuwane, zostaje tylko rekord meta-danych: *"Tester X potwierdził OK (Safari, Mobile) dnia Y"*.
- Logi dla zgłoszeń `bug` zostają na stałe (zgodnie z obecną polityką).

---

## 5. Zmiany Techniczne (Delta)

### Backend
- **Migracja `test_plans`**: Dodanie `status` (default: draft), `targets` (JSON).
- **Relacja `TestPlan -> FeedbackReport`**: Dodanie metody `confirmedReports()` (filtry: type=passed, unique tester).
- **Service `TestPlanManager`**: Logika sprawdzania, czy plan spełnił cele po każdym nowym zgłoszeniu.

### Extension
- **Persystencja**: Wtyczka zapisuje `active_test_plan_id` in `browser.storage.local`.
- **UI**: Przycisk "Wszystko OK" staje się nieaktywny (lub zmienia się w "Zaktualizuj potwierdzenie"), jeśli tester już raz kliknął OK w tej misji.

---

## 6. Integracje (Policy)
- **Zasada:** Zgłoszenia typu `passed` **NIGDY** nie są wysyłane do zewnętrznych narzędzi (Kanboard, GitHub).
- **Dlaczego:** Aby nie generować szumu dla deweloperów. Są to dane wyłącznie analityczno-audytowe wewnątrz Gemini.

---

**DoD (Definition of Done):**
- [ ] Admin widzi brakujące platformy (np. "Brakuje nam jeszcze 2 testów na Safari").
- [ ] Logi w bazie są wyczyszczone z tokenów sesji.
- [ ] Tester nie może "nabić" licznika wielokrotnym klikaniem.
