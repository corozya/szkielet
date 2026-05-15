# TASK: Wizard Preview Missing Text in Embroidery Render

## Status
- **Priority:** High
- **Type:** Frontend / Wizard / Rendering
- **Created:** 2026-05-14
- **State:** Pending

## Context
Na stronie sukcesu zamówienia:

`https://reczniki-haftowane.pl/order/success?orderNumber=ORD-2026-000009&accessToken=BmlJ0OBHzyBAWHAHfs1cxfRUEtgt5NUb2A0735jtc9w8amrfYy4rAMv1mGsQydVd`

generowany podgląd haftu nie zawiera tekstu w renderze.

## Problem
- Podgląd wizualizacji haftu renderuje elementy graficzne, ale brak w nim tekstu.
- Najbardziej prawdopodobna przyczyna to problem z ładowaniem lub użyciem czcionki.
- Należy zweryfikować cały pipeline renderowania tekstu do podglądu, nie tylko samą stronę sukcesu.

## Requirements
- [ ] Zidentyfikować, w którym miejscu tekst znika: dane wejściowe, generator preview, asset fontu, czy finalny renderer.
- [ ] Sprawdzić, czy używana czcionka jest dostępna dla generatora podglądu.
- [ ] Upewnić się, że tekst z konfiguracji haftu trafia do finalnej wizualizacji.
- [ ] Naprawić render tak, aby tekst był widoczny w podglądzie na stronie sukcesu i w powiązanych widokach.

## Verification
- [ ] Wygenerować podgląd haftu z tekstem i potwierdzić, że tekst jest widoczny.
- [ ] Sprawdzić, że efekt działa także po odświeżeniu strony sukcesu.

## Notes
- Referencyjny URL z obserwacji:
  `https://reczniki-haftowane.pl/order/success?orderNumber=ORD-2026-000009&accessToken=BmlJ0OBHzyBAWHAHfs1cxfRUEtgt5NUb2A0735jtc9w8amrfYy4rAMv1mGsQydVd`
- Podejrzenie: brak lub nieprawidłowe użycie czcionki w procesie renderowania preview.
