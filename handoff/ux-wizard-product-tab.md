# UX: Kreator — poprawki w panelu prawym (tab Produkt + summary)

**Priorytet:** P1  
**Typ:** Frontend  
**Strona:** `/wizard/{slug}` — edytor slotu

---

## Problem 1 — Tab Produkt zwija się po wyborze koloru

Po kliknięciu koloru ręcznika komponent `WizzardProductOptionsTab` ustawia `setIsCollapsed(true)`, co zwija siatkę kolorów do jednej linii ze zdjęciem wybranego ręcznika. Użytkownik traci widok siatki i widzi nieoczekiwany widok z miniaturką ręcznika.

**Fix:**  
`apps/reczniki-haftowane/frontend/src/components/wizzard/WizzardProductOptionsTab.jsx`, linia ~54 — usunąć `setIsCollapsed(true)` z onClick. Siatka kolorów zostaje widoczna, wybrany kolor ma checkmark. Stan `isCollapsed` i przycisk zwijania można całkowicie usunąć jeśli nikt inny go nie używa.

---

## Problem 2 — Pasek "Wzór / Nić / Czcionka" na dole panelu

`WizzardSelectionSummary` renderuje pasek z aktualnym stanem wyboru (Wzór, Nić, Czcionka) na dole prawego panelu. Ten element:
- zajmuje miejsce skracając listę opcji
- duplikuje informacje widoczne już przez checkmarki w siatce
- jest nieczytelny przy pustym stanie (same myślniki)

**Fix:**  
`apps/reczniki-haftowane/frontend/src/components/wizzard/WizzardControlPanel.jsx` — usunąć `<WizzardSelectionSummary />` i jego import. Komponent `WizzardSelectionSummary.jsx` można usunąć z repozytorium jeśli nigdzie indziej nie jest używany.

---

## Status

Zrobione:
- usunięto logikę summary z [WizzardControlPanel.jsx](/home/corozya/www/projects/reczniki-haftowane.pl/frontend/src/components/wizzard/WizzardControlPanel.jsx)
- usunięto nieużywany plik [WizzardSelectionSummary.jsx](/home/corozya/www/projects/reczniki-haftowane.pl/frontend/src/components/wizzard/WizzardSelectionSummary.jsx)
- w panelu produktu nie ma już żadnego collapse ani zwijania po wyborze koloru
