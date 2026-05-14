# Zadanie: Nagłówek z podziękowaniem za wysoki na mobile — nie widać wyboru płatności

**Status:** todo  
**Priorytet:** normalny  
**Zgłoszone:** 2026-05-12

## Projekt
RecznikiHaftowane

## Kolumna
Backlog

## Opis
Na stronie potwierdzenia zamówienia (`/order/success`) nagłówek z podziękowaniem zajmuje zbyt dużo miejsca na ekranie mobilnym. Przez to sekcja z wyborem metody płatności (PayU / przelew) nie jest widoczna bez przewijania — klient może nie wiedzieć, że musi coś kliknąć.

**URL do odtworzenia:**
https://reczniki-haftowane.pl/order/success?orderNumber=ORD-2026-000004&accessToken=VcHGSxN3WQSBp8nTb3IIog8d87uNC8mB4k6W4JU58OjPe5B8FAOT40FqmLQnIeUi

**Device Info:**
- Screen: 1280x720, Viewport: 395x592 (mobile)
- Browser: Chrome 148 / Windows

## Wymagania

Na viewporcie mobilnym (≤ 430px szerokości) nagłówek powinien być na tyle zwięzły, żeby sekcja wyboru płatności była widoczna bez przewijania (above the fold) lub przynajmniej wyraźnie sygnalizowana.

Możliwe podejścia:
1. Zmniejszyć padding/margin nagłówka na mobile
2. Skrócić tekst nagłówka na małych ekranach
3. Przenieść wybór płatności wyżej w hierarchii strony

## Wskazówki

- Strona: `apps/reczniki-haftowane/frontend/src/pages/OrderSuccessPage.jsx`
- Nagłówek prawdopodobnie w komponencie na górze strony (szukaj klas Tailwind typu `py-`, `pt-`, `h-`, `min-h-`)
- Testować na viewport 395x592

## Szczegóły
- **Typ:** Bug / UX
- **Priorytet:** Normal
- **Kanboard:** #13
- **Data zgłoszenia:** 12.05.2026

---

## Akcja wymagana

Znajdź nagłówek w `OrderSuccessPage`, zmniejsz jego rozmiar na mobile tak, żeby sekcja płatności była widoczna. Po zakończeniu usuń ten plik z `handoff/` i dopisz wpis do sekcji „Zakończone” w `handoff/README.md`.
