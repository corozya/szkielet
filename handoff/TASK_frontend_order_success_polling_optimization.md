# TASK: Frontend Order Success Polling Optimization

## Status
- **Priority:** High
- **Type:** Frontend / Payments / UX
- **Created:** 2026-05-14
- **State:** Pending

## Context
Na stronie sukcesu zamówienia `https://reczniki-haftowane.pl/order/success?orderNumber=...&accessToken=...` request do:

`GET /api/v1/orders/{orderNumber}/payment-status`

wykonuje się zbyt często, co generuje ciągłe odpytywanie backendu.

## Problem
- Polling statusu płatności nie ma wystarczającego odstępu czasowego.
- Request powinien wykonywać się maksymalnie raz na minutę między kolejnymi sprawdzeniami.
- Obecne zachowanie powoduje nadmierny ruch sieciowy i zbędne obciążenie backendu.

## Requirements
- [ ] Ograniczyć polling `payment-status` do jednego requestu na 60 sekund.
- [ ] Upewnić się, że polling nie uruchamia się równolegle z wieloma kolejnymi żądaniami.
- [ ] Zachować poprawne wykrywanie zmiany statusu płatności i zakończenie pollingu po sukcesie / finalnym stanie.
- [ ] Sprawdzić, czy odświeżenie strony nie resetuje mechanizmu w sposób powodujący spam requestów.

## Verification
- [ ] Otworzyć stronę sukcesu zamówienia i potwierdzić, że kolejne requesty do `payment-status` pojawiają się nie częściej niż co 60 sekund.
- [ ] Zweryfikować, że polling nadal działa do momentu uzyskania ostatecznego statusu.

## Notes
- Referencyjny URL z obserwacji:
  `https://reczniki-haftowane.pl/order/success?orderNumber=ORD-2026-000009&accessToken=BmlJ0OBHzyBAWHAHfs1cxfRUEtgt5NUb2A0735jtc9w8amrfYy4rAMv1mGsQydVd`
- Endpoint obserwowany w requestach:
  `/api/v1/orders/ORD-2026-000009/payment-status`
