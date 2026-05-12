# TASK: Mail potwierdzający — przycisk CTA "Zobacz szczegóły zamówienia"

**Status**: todo  
**Priorytet**: średni  
**Zgłoszone**: 2026-05-12

## Problem

W mailu z potwierdzeniem zamówienia link "Zobacz szczegóły zamówienia" jest zwykłym tekstowym linkiem. Powinien być dużym, widocznym przyciskiem (CTA button) — lepiej widocznym dla klienta i zachęcającym do kliknięcia.

## Zakres zmian

### Backend — szablon maila

Znaleźć szablon maila potwierdzającego zamówienie (prawdopodobnie Blade lub Markdown Mail w `resources/views/emails/` lub `app/Mail/`).

Zmienić element `<a href="...">Zobacz szczegóły zamówienia</a>` na styl przycisku:

```html
<!-- Zamiast zwykłego linka: -->
<a href="{{ $orderUrl }}" style="
  display: inline-block;
  background-color: #2563eb;
  color: #ffffff;
  font-size: 16px;
  font-weight: 600;
  padding: 14px 32px;
  border-radius: 6px;
  text-decoration: none;
  text-align: center;
  margin: 24px 0;
">
  Zobacz szczegóły zamówienia →
</a>
```

**Uwagi dot. emaili HTML:**
- Używać inline styles (klienty mailowe ignorują `<style>`)
- Testować w popularnych klientach (Gmail, Outlook, Apple Mail)
- Kolor przycisku dopasować do palety brandowej sklepu

### Opcjonalnie

- Dodać sekcję oddzielającą przycisk od reszty treści (pozioma linia lub odstęp)
- Dodać fallback tekstowy dla klientów bez HTML: `Otwórz w przeglądarce: {{ $orderUrl }}`

## Weryfikacja

- [ ] Przycisk widoczny i klikalny w Gmail (web)
- [ ] Przycisk widoczny w Outlook
- [ ] Link prowadzi do właściwego URL zamówienia
- [ ] Mail wygląda poprawnie przy wąskim viewporcie (mobile)

## Uwagi

- Sprawdzić czy projekt używa pakietu Mailables (Laravel Mail) czy raw Blade views
- Jeśli używany jest gotowy template transakcyjny (np. przez zewnętrzny SMTP jak Mailgun/SendGrid) — sprawdzić czy szablon jest zarządzany lokalnie czy przez panel dostawcy
