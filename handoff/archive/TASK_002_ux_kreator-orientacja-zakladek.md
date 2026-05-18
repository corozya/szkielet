<!-- STATUS: DONE -->
# TASK_002 — UX: Kreator — brak nagłówków sekcji i orientacji w zakładkach

## Kontekst audytu
- **Cel sesji:** Ścieżka zakupowa — prezent na ślub
- **Data:** 2026-05-17
- **Viewport:** Mobile 390×844

## Strony / Widoki
- `/wizard/zestaw-recznikow-xxl` — edytor slotu (bottom sheet), wszystkie zakładki

## Obserwacje UX (specjalista)
- [Priorytet: wysoki] — Na każdej zakładce (PRODUKT, WZORY, NICI, CZCIONKI, TEKST) nagłówek "co teraz robisz" istnieje wyłącznie w systemie podpowiedzi (tooltip). Po kliknięciu "Ukryj podpowiedzi" treść znika i użytkownik widzi siatkę wyborów bez żadnego kontekstu. Problem dotyczy wszystkich zakładek.
- [Priorytet: wysoki] — Zakładka TEKST pojawia się dynamicznie dopiero po wyborze wzoru obsługującego tekst. Użytkownik który wybrał wzór bez tekstu nie rozumie dlaczego nie może wpisać imion. Brak komunikatu "wybierz wzór z tekstem żeby odblokować tę zakładkę".
- [Priorytet: średni] — Tooltip kontekstowy nie aktualizuje się przy zmianie zakładki. Na zakładce TEKST wyświetla się komunikat "Wybierz kolor nici" — niezgodny z aktualnym widokiem.

## Obserwacje użytkownika
- Potwierdzone: "tutaj chyba powinien być nagłówek 'Wybierz kolor ręcznika' — tylko na mobile"
- Potwierdzone: "to samo na innych zakładkach"

## Kierunek rozwiązania
- Dodać statyczny nagłówek H3 nad siatką wyborów w każdej zakładce, widoczny zawsze (nie tylko w tooltipie): "Wybierz kolor ręcznika", "Wybierz wzór haftu", "Wybierz kolor nici", "Wybierz czcionkę", "Wpisz tekst haftu"
- Zakładka TEKST gdy wzór bez tekstu: wyświetlić placeholder z komunikatem "Wróć do zakładki Wzory i wybierz wzór z miejscem na tekst (np. Serce z imionami, Imię)"
- Tooltip: przekazywać aktywną zakładkę jako kontekst i wyświetlać właściwy komunikat

## Status
- owner: Frontend
- state: done
- źródło: audyt UX 2026-05-17
