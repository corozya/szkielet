<!-- STATUS: DONE -->
# TASK_005 — UX: Kreator — sloty, lista wzorów, przyciski koszyka

## Kontekst audytu
- **Cel sesji:** Ścieżka zakupowa — prezent na ślub
- **Data:** 2026-05-17
- **Viewport:** Mobile 390×844

## Strony / Widoki
- `/wizard/zestaw-recznikow-xxl` — widok główny kreatora (sloty)
- `/wizard/zestaw-recznikow-xxl` — edytor slotu, zakładka WZORY

## Obserwacje UX (specjalista)
- [Priorytet: wysoki] — Dwa przyciski "DODAJ DO KOSZYKA" na tej samej stronie: jeden pod siatką slotów (inline), jeden przyklejony na dole (sticky). Na mobile redundantny — wystarczy sticky. Inline powinien być ukryty (`hidden lg:block`) żeby nie dezorientował użytkownika.
- [Priorytet: wysoki] — Przycisk "DODAJ DO KOSZYKA" (sticky) powinien mieć główny brązowy kolor szablonu, taki jak główne CTA na stronie produktu. Aktualnie może wyglądać inaczej od reszty systemu.
- [Priorytet: średni] — DODAJ DO KOSZYKA aktywuje się już po skonfigurowaniu 1 z 4 ręczników bez żadnego komunikatu. Użytkownik może nie wiedzieć że pozostałe 3 ręczniki będą bez haftu (lub z domyślnym). Dodać tooltip / badge np. "Skonfigurowano 1 z 4 ręczników — pozostałe 3 będą takie same lub bez haftu".
- [Priorytet: średni] — 4 identyczne sloty "Ręcznik kąpielowy / Kliknij, by zaprojektować" bez numeracji widocznej na kafelku. Dla zestawu 4-osobowego warto pokazać "Ręcznik 1 z 4", "Ręcznik 2 z 4" itd. bezpośrednio na kafelkach (aktualnie numeracja jest tylko wewnątrz edytora).
- [Priorytet: średni] — Lista wzorów (100+ pozycji) domyślnie pokazuje "Wszystkie wzory". Na stronie `/prezent-na-slub` i produkcie ślubnym logiczne byłoby ustawić domyślny filtr "Ślub i rocznica" — skraca czas decyzji.
- [Priorytet: niski] — Stara zawartość koszyka z poprzedniej sesji (nieusunięty produkt) pojawiła się przy wejściu w ścieżkę nowego użytkownika. Dialog "Usuń produkt" niespodziewanie wyskoczył podczas audytu. Warto zbadać czy session storage / localStorage jest odpowiednio czyszczony lub czy koszyk wymaga wyraźniejszego zarządzania.

## Obserwacje użytkownika
- "pod wszystkimi slotami jest kolejny przycisk dodaj do koszyka. jeden powinniśmy ukryć na mobile. ten przyklejony wg mnie jest ok"
- "przycisk dodaj do koszyka powinien być brązowy — jak główny brązowy templatu"

## Kierunek rozwiązania
- Ukryć inline "DODAJ DO KOSZYKA" na mobile (`hidden lg:flex`), zostaje tylko sticky
- Zmienić kolor sticky przycisku na główny brązowy (sprawdzić token CSS/Tailwind klasy używanej przez inne CTA)
- Dodać badge lub komunikat inline pod siatką slotów: "X z 4 ręczników zaprojektowanych"
- Dodać numer slotu na kafelku (widoczny bez otwierania edytora)
- W zakładce WZORY: ustawiać domyślny filtr na podstawie kontekstu produktu (prop/slug z URL)

## Status
- owner: Frontend
- state: done
- źródło: audyt UX 2026-05-17
