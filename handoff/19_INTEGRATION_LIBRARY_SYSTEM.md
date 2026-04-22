# 19_INTEGRATION_LIBRARY_SYSTEM

**Status:** Częściowo zakończone ✅ (Biblioteka działa, Runda 1 adapterów gotowa)
**Zadania:** Budowa centralnej biblioteki integracji (API Library) na wzór Google Cloud Console.

**Cel:** Stworzenie profesjonalnego katalogu integracji, gdzie użytkownik może przeglądać, aktywować i zarządzać zewnętrznymi systemami w skali całej organizacji.

**Zakres:**
1. **Metadata & Registry (Backend):**
    - `DestinationRegistry` musi obsługiwać kategorie (`messaging`, `devops`, `task-management`, `analytics`).
    - Każdy adapter musi dostarczać: `longDescription(): string`, `features(): string[]`, `setupInstructions(): string`.
    - Dodanie logotypów integracji (jako ścieżki do SVG lub komponenty React).

2. **Library View (Frontend):**
    - Utworzenie strony `/dashboard/integrations` (Biblioteka Integracji).
    - Grid z kafelkami: Logo, Nazwa, Krótki opis, Status (Not Enabled / Enabled).
    - Filtrowanie po kategoriach i wyszukiwarka.

3. **Integration Detail Page:**
    - Dynamiczna strona dla każdej integracji z pełnym opisem, listą funkcji i instrukcją "Krok po kroku".
    - Przycisk "Enable" (jeśli wymaga globalnych kluczy API dla klienta).

4. **Project Integration Context:**
    - W ustawieniach projektu (`Projects/Edit.jsx`) użytkownik widzi listę "Twoje Integracje" (tylko te włączone w bibliotece).
    - Uproszczony proces dodawania do projektu: "Wybierz z biblioteki" -> "Konfiguruj parametry specyficzne dla projektu (np. ID kanału)".

**DoD:**
- Działająca wyszukiwarka i kategoryzacja w bibliotece.
- Możliwość przejścia do szczegółów każdej integracji.
- Spójny flow: Aktywacja w bibliotece -> Konfiguracja w projekcie.
