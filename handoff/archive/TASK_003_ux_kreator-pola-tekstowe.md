<!-- STATUS: DONE -->
# TASK_003 — UX: Kreator — UX pól tekstowych w zakładce TEKST

## Kontekst audytu
- **Cel sesji:** Ścieżka zakupowa — prezent na ślub
- **Data:** 2026-05-17
- **Viewport:** Mobile 390×844

## Strony / Widoki
- `/wizard/zestaw-recznikow-xxl` — edytor slotu, zakładka TEKST

## Obserwacje UX (specjalista)
- [Priorytet: wysoki] — Brak przycisku zamykającego klawiaturę przy polach tekstowych. Jedynym sposobem schowania klawiatury jest ponowne kliknięcie w pole lub kliknięcie poza nim. Na mobile po otwarciu klawiatury dolny pasek zakładek jest jeszcze bardziej niedostępny. Standardowy pattern to przycisk "Gotowe" / "Zamknij" nad klawiaturą lub jako element inputa.
- [Priorytet: średni] — Kolejność pól: IMIĘ 2 jest wyświetlane nad IMIĘ 1. Naturalna kolejność to od 1 do N. Może powodować pomyłki (kto jest "imię 1" a kto "imię 2").
- [Priorytet: niski] — Licznik znaków pokazuje samą liczbę (np. "5") bez widocznego limitu. Użytkownik nie wie ile znaków może wpisać (np. "5 / 20").

## Obserwacje użytkownika
- "przy tekstach brakuje chyba przycisku zamykającego"
- "dopiero ponowne kliknięcie w tekst zwija okno"

## Kierunek rozwiązania
- Dodać przycisk "Zamknij klawiaturę" (ikonka ⌨️↓ lub "Gotowe") jako element paska narzędzi nad klawiaturą (inputAccessoryView na iOS / podobny pattern na Android)
- Zmienić kolejność pól na IMIĘ 1 → IMIĘ 2 (od pierwszego do ostatniego)
- Zmienić licznik z "5" na "5 / 20" (lub właściwy limit dla danego pola)

## Status
- owner: Frontend
- state: done
- źródło: audyt UX 2026-05-17
