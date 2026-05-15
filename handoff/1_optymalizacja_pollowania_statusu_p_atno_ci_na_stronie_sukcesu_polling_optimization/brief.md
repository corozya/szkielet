# Brief: Optymalizacja pollowania statusu płatności na stronie sukcesu (polling optimization)

**Task ID:** 1
**URL:** http://localhost/task/1
**Kolumna:** None
**Rola:**
**Suggested AI:**
**Fallback:**

## Opis zadania
Problem:
Strona /order/success wykonuje zapytania o status płatności (getOrderPaymentStatus) co 2 sekundy, nawet jeśli dla danego zamówienia nie ma aktywnej sesji płatności (np. po wejściu z linku w mailu, gdy płatność nie została jeszcze zainicjowana).

Cel:
Ograniczenie pollowania tylko do przypadków, gdy status płatności sugeruje, że transakcja jest w toku (pending lub initiating).

Szczegóły techniczne w: handoff/TASK_frontend_order_success_polling_optimization.md

## Status
- [ ] Implementacja
- [ ] Testy
- [ ] Weryfikacja
