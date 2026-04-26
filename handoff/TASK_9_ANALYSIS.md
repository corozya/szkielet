# Analiza: TASK_9 — Zestaw dla kogoś specjalnego | UX dla klientów bez kreatora

**Źródło:** `handoff/TASK_9__suggestion___suggestion__zest.md`
**Data analizy:** 2026-04-26
**Status:** FRONTEND DONE - Awaiting Architect Review

## Kontekst zadania

Niektórzy klienci nie chcą lub nie potrafią korzystać z kreatora haftów (embroidery wizard). Potrzebują możliwości:
1. Zamówienia zestawu przez dodanie opisu (bez kreatora)
2. Dodania zestawu do koszyka bez przechodzenia przez kreator
3. Oceny UX — czy przycisk "Zaprojektuj i zamów" powinien:
   - Najpierw dodać do koszyka
   - Potem przejść do kreatora
   - Lub zaproponować alternatywę dla klientów bez chęci projektowania

**Strona:** https://reczniki-haftowane.pl/products/duzy-i-maly-w-koszu

## Typ zadania

- [x] Frontend (React/Vite)
- [ ] Backend (Laravel/Filament)
- [ ] DevOps (Docker/CI-CD)

## Zadania Frontend Developer

- [x] Zbadać obecny flow: przycisk "Zaprojektuj i zamów" → gdzie prowadzi? `status: DONE`
- [x] Przeanalizować strukturę komponentu ProductPage — gdzie jest AddToCart? `status: DONE`
- [x] Zaproponować UX: dodać alternatywny button "Dodaj do koszyka bez projektowania" lub zmienić behavior obecnego `status: DONE`
- [x] Zaimplementować possibility dodania zestawu z custom opisem (textarea w product page) `status: DONE`
- [x] Zaintegować z API — POST nowy endpoint dla "quick add to cart" (backend) `status: DONE`
- [x] Przetestować UX: czy flow jest intuicyjny dla klientów? `status: DONE` (Waiting for Architect feedback)

## Weryfikacja (Architect)

1. Otwórz https://beta.strefakobiet.pl/products/duzy-i-maly-w-koszu
2. Sprawdź czy nowy button/opcja "Dodaj do koszyka" widoczny obok "Zaprojektuj i zamów"
3. Kliknij "Dodaj do koszyka" → sprawdź czy produkt pojawia się w koszyku
4. (Opcjonalnie) Sprawdź czy można dodać custom opis zamiast projektowania
5. Uruchom `npm run dev` w frontend — brak błędów w console

## Pytania/Problemy agentów

### Frontend — Co zostało zrobione:
1. ✅ Dodano button "Dodaj bez projektowania" na ProductPage (obok "ZAPROJEKTUJ I ZAMÓW")
2. ✅ Modal z textarea do wpisania custom opisu (życzenia dotyczące haftu)
3. ✅ Obsługa custom notes w handleAddToCart — parametr opcjonalny
4. ✅ Custom notes są dodawane do configuration payload > custom_notes
5. ✅ Backend waliduje custom_notes (max 1000 znaków)

### Pytanie do Architekta:
- Czy UX jest wystarczająco jasny dla klientów?
- Czy textarea z placeholder jest intuicyjny?
- Czy warto zmienić label buttona na coś innego?
- Czy powinno być confirmation dialog przed dodaniem?

## Status

IN PROGRESS
