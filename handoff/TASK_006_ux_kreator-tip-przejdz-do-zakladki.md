<!-- STATUS: DONE -->
# TASK_006 — Bug: Kreator — "Przejdź do zakładki" nie renderuje treści docelowej zakładki

## Kontekst audytu
- **Cel sesji:** Ścieżka zakupowa — prezent na ślub
- **Data:** 2026-05-17
- **Viewport:** Mobile 390×844

## Strony / Widoki
- `/wizard/zestaw-recznikow-xxl` — edytor slotu (bottom sheet), tooltip systemu podpowiedzi

## Opis bugu
Tooltip "Wybierz wzór haftu" (widoczny na zakładce PRODUKT po wyborze koloru ręcznika) zawiera przycisk "Przejdź do zakładki". Po kliknięciu:

**Oczekiwane zachowanie:**
1. Tooltip się zamyka
2. Aktywna zakładka zmienia się na WZORY
3. Treść zakładki (siatka wzorów) jest widoczna

**Faktyczne zachowanie:**
1. Tooltip się zamyka ✓
2. Tab bar zdaje się wskazywać WZORY jako aktywny
3. Siatka wzorów **nie renderuje się** — obszar treści jest pusty lub ma zerową wysokość
4. Widoczny jest tylko podgląd ręcznika i stopka strony

**Weryfikacja:** kliknięcie przycisku WZORY bezpośrednio w pasku zakładek działa poprawnie — siatka wzorów pojawia się natychmiast.

## Kroki do reprodukcji
1. Wejdź na `/wizard/zestaw-recznikow-xxl`
2. Kliknij dowolny slot
3. Wybierz kolor ręcznika (zakładka PRODUKT)
4. Pojawi się tooltip "Wybierz wzór haftu" z przyciskiem "Przejdź do zakładki"
5. Kliknij "Przejdź do zakładki"
6. Sprawdź czy siatka wzorów jest widoczna → **nie jest**

## Kierunek rozwiązania
- Sprawdzić handler przycisku "Przejdź do zakładki" — prawdopodobnie wywołuje `setActiveTab('wzory')` ale nie triggeruje re-renderu/scroll do contentu
- Upewnić się że po zmianie aktywnej zakładki komponent treści (panel wzorów) jest montowany/renderowany synchronicznie
- Dodać ewentualnie `scrollIntoView` na panel treści po przełączeniu

## Status
- owner: Frontend
- state: done
- źródło: audyt UX 2026-05-17
