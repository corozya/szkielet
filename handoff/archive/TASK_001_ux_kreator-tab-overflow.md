<!-- STATUS: DONE -->
# TASK_001 — UX: Kreator — overflow paska zakładek, GOTOWE poza ekranem

## Kontekst audytu
- **Cel sesji:** Ścieżka zakupowa — prezent na ślub
- **Data:** 2026-05-17
- **Viewport:** Mobile 390×844

## Strony / Widoki
- `/wizard/zestaw-recznikow-xxl` — edytor slotu (bottom sheet)

## Obserwacje UX (specjalista)
- [Priorytet: wysoki] — Gdy pojawia się zakładka TEKST (po wyborze wzoru z tekstem), pasek ma 6 pozycji: PRODUKT, WZORY, NICI, CZCIONKI, TEKST, GOTOWE. Na 390px GOTOWE wypada poza prawy kraniec ekranu i jest niewidoczne. Użytkownik który wpisał imiona nie może zatwierdzić konfiguracji slotu — blokada zakupu.

## Obserwacje użytkownika
- Potwierdzone: "gdy jest tab tekst dolne menu nie mieści się i jest obcięte - coś musimy z tym zrobić"

## Kierunek rozwiązania
- Opcja A (rekomendowana): wynieść GOTOWE poza pasek zakładek jako osobny sticky button, np. nad paskiem lub jako floating CTA — zawsze widoczny niezależnie od liczby zakładek
- Opcja B: pasek z `overflow-x: auto` + gradient cieniujący prawy kraniec sygnalizujący że jest więcej zakładek — ryzyko: GOTOWE nadal może być niezauważone
- Opcja C: skrócić etykiety zakładek do samych ikon na mobile (np. 🎨 / ✏️ / 🧵 / A / T) — zmniejsza czytelność

## Status
- owner: Frontend
- state: done
- źródło: audyt UX 2026-05-17
