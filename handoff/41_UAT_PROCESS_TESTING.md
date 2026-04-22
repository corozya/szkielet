# Plan: Procesy Testowania (UAT)

Niniejszy dokument definiuje strategię implementacji testów procesowych (UAT) w systemie, umożliwiającą właścicielowi projektu weryfikację gotowości funkcjonalności do wdrożenia na produkcję.

## 1. Model danych (Backend)
- Wprowadzenie encji `TestCampaign` (lub rozszerzenie `FeedbackCategory`), która będzie reprezentować konkretną kampanię testową (np. "Wdrożenie nowego checkoutu").
- Powiązanie kategorii z konkretnymi wdrożeniami.
- Przechowywanie statystyk: liczba wykonanych testów, liczba wyników `PASS` oraz `FAIL`.

## 2. Rozszerzenie Feedback-Extension (Wtyczka)
- **UI:** Modyfikacja `popup.html` / `popup.js`, aby po wybraniu kategorii typu "Test Procesowy" wyświetlały się dwa dedykowane przyciski: **[PASS]** i **[FAIL]**.
- **Walidacja:**
    - Wymuszenie uzasadnienia (komentarza) w przypadku wyboru statusu `FAIL`.
    - Automatyczne dołączanie `Context ID` testu do payloadu przesyłanego do API.

## 3. Logika Backendowa
- Implementacja w `FeedbackController` (lub dedykowanym `AuditController`) logiki inkrementującej statystyki kampanii przy każdym odebranym feedbacku oznaczonym jako test.
- Przygotowanie endpointów dla dashboardu właściciela prezentujących agregację wyników (np. pasek postępu: X/Y testerów potwierdziło PASS).

## 4. Weryfikacja i implementacja (Kolejne kroki)
- Analiza obecnego `feedback-extension/src/api.js` pod kątem komunikacji z API.
- Analiza obecnych kontrolerów w `backend-api` obsługujących feedback.
- Migracja bazy danych w celu wsparcia typowania kategorii (zwykły feedback vs. test procesowy).
