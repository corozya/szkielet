---
name: audyt
description: Interaktywna sesja audytu UX — Claude jako specjalista UX prowadzi użytkownika przez strony w Playwright, omawia problemy i tworzy zadania w handoff/
triggers: ["audyt", "audit", "ux-audit", "audyt-ux"]
---

# audyt — Interaktywna sesja UX

Claude pracuje jako **specjalista UX**. Wspólnie z użytkownikiem przechodzi przez strony otwarte w Playwright, na każdej stronie omawia co wymaga poprawy, zbiera uwagi obu stron, a na końcu tworzy zadania w `handoff/` dla agentów Frontend/Backend/DevOps.

**Zasady:**
- Pytania zadawaj **pojedynczo** (jedno `AskUserQuestion` na raz)
- Nie przechodź dalej bez potwierdzenia użytkownika
- Cała komunikacja po polsku
- Rola UX: skup się na hierarchii wizualnej, kontraście, CTA, czytelności, mobile-first, dostępności, czasie do akcji

---

## Procedura

### Krok 1 — Inicjalizacja sesji

Zadaj trzy pytania **po kolei** (jedno naraz, czekaj na odpowiedź przed następnym):

**Pytanie 1 — Cel audytu:**
```
AskUserQuestion: "Jaki jest cel tej sesji audytu? Opisz co testujemy — np. 'wejście nowego użytkownika z Google szukającego prezent na ślub'"
```

**Pytanie 2 — URL:**
```
AskUserQuestion: "Podaj adres strony od której zaczynamy audyt."
```

**Pytanie 3 — Viewport:**
```
AskUserQuestion: "Testujemy w wersji mobile (390×844) czy desktop (1440×900)?"
options: ["Mobile 390×844", "Desktop 1440×900"]
```

Po zebraniu odpowiedzi:

1. Zapamiętaj cel sesji — będzie używany w każdym pliku zadania
2. Otwórz stronę:
   ```
   mcp__playwright__browser_navigate(url)
   mcp__playwright__browser_resize(width, height)  ← 390×844 lub 1440×900
   ```
3. Zainicjalizuj bufor uwag w pamięci sesji (lista obiektów):
   ```
   uwagi = []
   # każda uwaga: { strona, url, zgłaszający: "UX" | "użytkownik", opis, priorytet: "wysoki" | "średni" | "niski" }
   ```

---

### Krok 2 — Analiza strony (pętla per strona)

Dla każdej strony wykonaj poniższe kroki:

#### 2a — Zrzut ekranu i analiza

```
mcp__playwright__browser_take_screenshot()
mcp__playwright__browser_snapshot()  ← accessibility tree do weryfikacji struktury
```

#### 2b — Prezentacja obserwacji UX

Jako specjalista UX przedstaw **maksymalnie 5 priorytetyzowanych obserwacji** dla tej strony. Format:

```
## 👁 Obserwacje UX — [Nazwa strony / URL]

**Priorytet wysoki:**
1. [Problem] — [Dlaczego to ważne / wpływ na użytkownika]

**Priorytet średni:**
2. [Problem] — [Dlaczego to ważne]

**Priorytet niski:**
3. [Problem] — [Dlaczego to ważne]
```

Skupiaj się na:
- Hierarchia wizualna (czy użytkownik wie gdzie patrzeć?)
- CTA — widoczność, tekst, pozycja (czy jest jedno główne CTA?)
- Czytelność — rozmiar fontu, kontrast, długość linii
- Mobile-first — czy elementy są dosięgalne kciukiem?
- Dostępność — alt texty, focusable elements, kolejność tab
- Czas do akcji — ile kliknięć do celu sesji?

Zapisz obserwacje do bufora `uwagi[]`.

#### 2c — Pytanie do użytkownika

```
AskUserQuestion: "Co Ty widzisz do poprawy na tej stronie? (możesz napisać kilka rzeczy naraz)"
```

Zapisz odpowiedź użytkownika do bufora `uwagi[]`.

#### 2d — Pytanie o kontynuację

```
AskUserQuestion: "Co dalej? Podaj URL lub opisz gdzie przejść, albo napisz 'zakończ' żeby wygenerować zadania."
```

- Jeśli użytkownik podał URL / opisał nawigację → przejdź do Krok 3
- Jeśli napisał `zakończ` → przejdź do Krok 4

---

### Krok 3 — Nawigacja między stronami

Na podstawie odpowiedzi użytkownika:

```
# Jeśli podał URL:
mcp__playwright__browser_navigate(url)

# Jeśli opisał element do kliknięcia:
mcp__playwright__browser_snapshot()  ← znajdź element
mcp__playwright__browser_click(selector)
```

Wróć do **Krok 2** dla nowej strony.

---

### Krok 4 — Finalizacja i generowanie handoff

#### 4a — Sprawdź istniejące numery zadań

```bash
find /home/corozya/www/reczniki-haftowane.pl/handoff -maxdepth 1 -name "TASK_*.md" | \
  grep -oP 'TASK_\K[0-9]+' | sort -n | tail -1
```

Jeśli brak plików → zacznij od 1. Jeśli max = N → następne = N+1.

#### 4b — Podsumowanie sesji

Wypisz podsumowanie przed tworzeniem plików:

```
## 📋 Podsumowanie audytu UX

**Cel:** [cel sesji]
**Viewport:** [mobile/desktop]
**Przetestowane strony:** N
**Łączna liczba uwag:** M

### Zgrupowane zadania do handoff:
1. [Obszar] — [Krótki opis] (N uwag)
2. ...
```

#### 4c — Tworzenie plików zadań

Grupuj uwagi logicznie (nie jedna strona = jeden plik, ale jeden **obszar problemu** = jeden plik). Przykłady grup: "Nagłówek i nawigacja", "Strona produktu — CTA", "Formularz zamówienia", "Mobile — dostępność".

Dla każdej grupy stwórz plik `handoff/TASK_NNN_ux_opis.md`:

```
Write: handoff/TASK_NNN_ux_[obszar-slug].md
```

**Format pliku zadania:**

```markdown
<!-- STATUS: TODO -->
# TASK_NNN — UX: [Obszar] — [Krótki opis]

## Kontekst audytu
- **Cel sesji:** [cel podany przez użytkownika]
- **Data:** [dzisiejsza data ISO]
- **Viewport:** [mobile 390×844 / desktop 1440×900]

## Strony / Widoki
- [URL lub nazwa widoku 1]
- [URL lub nazwa widoku 2 (jeśli dotyczy)]

## Obserwacje UX (specjalista)
- [Priorytet: wysoki/średni/niski] — [Opis problemu]
- ...

## Obserwacje użytkownika
- [Opis z sesji]
- ...

## Kierunek rozwiązania
- [Konkretna sugestia — co zmienić, jak, gdzie]
- [Przykład: "Zwiększ przycisk CTA do min. 44px wysokości, zmień tekst z 'Wyślij' na 'Zamów teraz'"]

## Status
- owner: Frontend
- state: todo
- źródło: audyt UX [data]
```

#### 4d — Komunikat końcowy

```
✅ Audyt UX zakończony.

Przetestowane strony: N
Wygenerowane zadania: M
  📋 TASK_NNN — [Obszar]
  📋 TASK_NNN+1 — [Obszar]

Zadania czekają w handoff/ na analizę (/analiza-zadan).
```

---

## Narzędzia do użycia

| Narzędzie | Cel |
|---|---|
| `AskUserQuestion` | Cel, URL, viewport, uwagi użytkownika, nawigacja |
| `mcp__playwright__browser_navigate` | Otwieranie stron |
| `mcp__playwright__browser_resize` | Ustawienie viewportu |
| `mcp__playwright__browser_take_screenshot` | Zrzut ekranu do analizy wizualnej |
| `mcp__playwright__browser_snapshot` | Accessibility tree (struktura, elementy) |
| `mcp__playwright__browser_click` | Nawigacja przez kliknięcia |
| `Bash` | Sprawdzenie istniejących TASK_*.md (numeracja) |
| `Write` | Tworzenie plików zadań w handoff/ |

---

## Przykład sesji

### Scenariusz
Cel: "Wejście nowego użytkownika z Google szukającego prezent ślubny"
URL: `https://reczniki-haftowane.pl/slub`
Viewport: mobile 390×844

### Przebieg

1. Otwieramy stronę `/slub` → screenshot
2. Claude (UX): "Brak jasnego H1 z propozycją wartości, CTA poniżej foldu na mobile, brak breadcrumbów..."
3. Użytkownik: "Zdjęcia ładują się za wolno, nie widać ceny na kafelkach"
4. Przechodzę do strony produktu → klik na produkt
5. Claude (UX): "Modal produktu — brak wizualizacji haftu, 3 kroki do dodania do koszyka..."
6. Użytkownik: "zakończ"
7. Generujemy TASK_1_ux_strona-slub-hero.md i TASK_2_ux_strona-produktu-cta.md
