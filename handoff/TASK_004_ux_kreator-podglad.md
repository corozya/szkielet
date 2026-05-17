<!-- STATUS: TODO -->
# TASK_004 — UX: Kreator — pozycjonowanie i widoczność podglądu ręcznika

## Kontekst audytu
- **Cel sesji:** Ścieżka zakupowa — prezent na ślub
- **Data:** 2026-05-17
- **Viewport:** Mobile 390×844

## Strony / Widoki
- `/wizard/zestaw-recznikow-xxl` — edytor slotu (bottom sheet), obszar podglądu

## Obserwacje UX (specjalista)
- [Priorytet: średni] — Obszar podglądu ręcznika ma widoczną wolną przestrzeń powyżej obrazu (między nagłówkiem bottom sheetu a zdjęciem). Na mobile każdy piksel viewport jest cenny. Podgląd mógłby być wyżej, co zwiększa jego widoczną powierzchnię i wpływ na decyzję.
- [Priorytet: średni] — Podgląd ręcznika renderuje wzór i tekst dopiero po wyborze koloru nici (NICI). Jeśli użytkownik wybrał wzór i wpisał tekst ale pominął NICI, podgląd wygląda na "nie działający". Brak komunikatu "wybierz kolor nici żeby zobaczyć pełny podgląd".
- [Priorytet: niski] — Przy otwartej klawiaturze na mobile podgląd jest zepchnięty poza viewport — użytkownik wpisuje tekst nie widząc efektu na żywo.

## Obserwacje użytkownika
- "podgląd ręcznika może być wyżej, mamy nad nim sporo wolnego miejsca"

## Kierunek rozwiązania
- Zmniejszyć margines/padding powyżej obrazu podglądu w bottom sheecie (sprawdzić na iPhone 14, Pixel 7)
- Dodać stan "podgląd niekompletny" z komunikatem inline np. "Wybierz kolor nici żeby zobaczyć pełny efekt haftu"
- Rozważyć sticky podgląd: przy scrollu treść zakładki scrolluje się pod stałym obrazem podglądu (pattern używany np. w konfiguratora butów)

## Status
- owner: Frontend
- state: todo
- źródło: audyt UX 2026-05-17
