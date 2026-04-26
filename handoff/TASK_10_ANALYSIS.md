# Analiza: TASK_10 — Kontakt i wycena haftu (panel admin + odpowiedź)

**Źródło:** `handoff/TASK_10__suggestion___suggestion__kont.md`
**Data analizy:** 2026-04-26
**Status:** IN PROGRESS

## Kontekst zadania

Na stronie `https://reczniki-haftowane.pl/kontakt` użytkownik wysyła wiadomość przez formularz kontaktowy. Wymaganie: dane z formularza mają być dostępne także z poziomu panelu administracyjnego oraz ma być możliwość odpowiedzi z panelu (workflow obsługi wiadomości).

Repo wygląda na to, że już ma backendowe API dla kontaktu (`Api/V1/ContactController`) oraz email template (`resources/views/emails/contact-message.blade.php`) i test (`tests/Feature/ContactApiTest.php`). Trzeba dołożyć warstwę “inbox” w panelu (Filament): zapis wiadomości + lista + statusy + akcja “odpowiedz”.

## Typ zadania

- [ ] Frontend (React/Vite)
- [x] Backend (Laravel/Filament)
- [ ] DevOps (Docker/CI-CD)

## Zadania Backend Developer

- [ ] Zidentyfikować obecny przepływ Contact API (czy zapisuje gdziekolwiek, czy tylko wysyła maila) `status: TODO`
- [ ] Dodać trwałe przechowywanie zgłoszeń kontaktowych (model + migracja) `status: TODO`
- [ ] Dodać zasób Filament do przeglądania wiadomości (lista + szczegóły) `status: TODO`
- [ ] Dodać w Filament akcję “Odpowiedz”:
  - wysyłka maila na adres nadawcy,
  - zapis odpowiedzi / metadanych (kto, kiedy, treść) w bazie,
  - oznaczenie wiadomości jako “answered” `status: TODO`
- [ ] Dodać statusy wiadomości (np. new/open/answered) i podstawowe filtry w panelu `status: TODO`
- [ ] Uzupełnić/napisać testy: zapis kontaktu + wysyłka odpowiedzi (Mail fake) `status: TODO`

## Weryfikacja (Architect)

- We frontendzie wyślij formularz na `/kontakt` i potwierdź, że backend tworzy rekord w DB.
- W panelu Filament:
  - widoczna jest lista wiadomości (najnowsze pierwsze),
  - można otworzyć szczegóły pojedynczej wiadomości,
  - akcja “Odpowiedz” wysyła maila i oznacza wiadomość jako answered,
  - widać historię odpowiedzi (min. ostatnia treść + timestamp).
- Uruchom testy backendu (jeśli są): z katalogu `apps/reczniki-haftowane/backend/` uruchomić test suite (np. `php artisan test`) i sprawdzić, że przechodzi.

## Pytania/Problemy agentów

(Agenci dopisują tu pytania/problemy w trakcie pracy)

## Status

IN PROGRESS

