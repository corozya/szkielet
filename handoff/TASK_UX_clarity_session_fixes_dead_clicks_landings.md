# TASK: UX — dead clicks (kreator + landing ślubny), pierwszy ekran, zaufanie

## Meta

| Pole | Wartość |
|------|---------|
| **Źródło dowodów** | `docs/audit-ux-kreator-sugestie.md` (wpisy #1–#17), Clarity Session Insights / nagrania |
| **Priorytet ogólny** | P0 — martwe kliknięcia na ścieżce konwersji |
| **Owner wdrożenia** | Frontend (+ treść/CMS przy landingach: Marketing / Backend wg stacku) |
| **Repo aplikacji** | `apps/reczniki-haftowane/` (frontend — ten orchestrator **nie zawiera** checkoutu; zmiany kodu tam) |
| **Status** | Do realizacji |
| **Data briefu** | 2026-05-16 |

---

## Cel

Usunąć **martwe kliknięcia** i oczywiste **pułapki UX** na ścieżce: **Google → landing okolicznościowy / kategoria → kreator**, oraz zwiększyć **szansę pierwszej interakcji** na landingach ślubnych bez psucia ścieżki już działającej z homepage (#5).

---

## Mapowanie problemów → wpisy Clarity

| Problem | Wpisy |
|---------|-------|
| Dead clicks w kreatorze (wzór / przełączanie / aplikacja zmian) | #3, #17 |
| Dead click na elemencie wyglądającym jak interakcja (landing) | #13 („Zamówienie przygotowujemy”) |
| Bardzo krótka ocena kreatora + pojedynczy klik / kliki „bez treści” | #4, #14 |
| Bounce na `/prezent-na-slub` i stronie kategorii ślub bez interakcji | #6–#9, #15–#16 |
| Multitasking / tab hidden — tło kontekstu, nie zawsze bug | #2, #12 |
| Regulamin → kontakt / polityka — sygnał zaufania | #10, #11 |
| Homepage bounce — niższy priorytet vs landing SERP | #1, #2 |

---

## P0 — Dead clicks (blokuje zaufanie i postęp w konfiguratorze)

### P0-A — Kreator: powtarzalne dead clicks podczas personalizacji

**Objaw:** Użytkownik aktywnie korzysta z zakładek (**Produkt**, **Wzory**, **Nici**, **Czcionki**), wybiera opcje, wpisuje tekst — jednocześnie Clarity raportuje **dead clicks** (#3: ~00:44, ~00:48; #17: ~00:31, ~02:17, ~03:10).

**Hipotezy techniczne (do zweryfikowania w kodzie):**

1. **Warstwa nad celem kliknięcia:** baner cookies, sticky header, tooltip, modal „tips”, niewidoczny `backdrop`, kontener z `pointer-events` lub pełnoekranowy overlay częściowo przezroczysty.
2. **Element wygląda jak przycisk, ale nie jest:** `div`/`span` ze stylami przycisku bez `button` + `onClick`, lub rodzic jest klikalny, dziecko nie przekazuje akcji.
3. **Stan „disabled” bez komunikatu:** komponent wizualnie aktywny, logicznie nieobsługujący kliku (np. slot nie wybrany, walidacja).
4. **Podwójna obsługa zdarzeń / meta Glass:** klik trafia w „dziurę” między siatką miniaturek a faktycznym `button`.
5. **Mobile touch target:** obszar wizualny większy niż obszar trafienia (< 44×44 px).

**Kroki rozwiązania (wykonawcze):**

1. W Clarity otworzyć nagrania dla sesji z dead clickiem na URL `/wizard/...` (#3, #17); zapisać **selektor/hash** elementu z timeline (jeśli dostępny) i **viewport** (mobile/desktop).
2. W DevTools **Replay / local:** włączyć „Show listeners”, sprawdzić **Layers / pointer-events**, wyłączyć kolejno: cookie bar, tips, sticky — aż dead click znika.
3. Dla każdego miejsca typu „wybór wzoru / koloru / czcionki”:
   - Semantyka: **`button type="button"`** lub **`a href`** zamiast `div onClick`.
   - **`cursor-pointer`** tylko tam, gdzie faktycznie jest akcja; elementy czysto informacyjne: **`cursor-default`**, **`role="status"`** lub **`aria-disabled="true"`** + tooltip „Wybierz najpierw …”.
4. Zapewnić **`z-index` mapę** dokumentu dla kreatora (cookie < modal < sticky < treść klikalna); test po zaakceptowaniu cookies.
5. Min. **44×44 px** hit area na mobile (CSS `min-h/min-w` lub niewidoczny padding na `button`).
6. Po fixie: jedna sesja **Playwright** (jeśli macie): przejście Produkt → Wzory → Nici → Czcionki + wybór opcji — assert brak „frozen” UI.

**Kryteria akceptacji P0-A:**

- [ ] Na nagraniu testowym (staging) ta sama ścieżca jak #17 nie generuje **dead click** przy legalnych próbach wyboru opcji.
- [ ] Żaden element z tekstem typu „Zastosuj” / „Wybierz” nie jest `div` bez obsługi klawiatury (`Enter` / `Space`).
- [ ] Przy stanie zablokowanym użytkownik widzi **powód** (komunikat inline lub toast), zamiast „nic się nie dzieje”.

---

### P0-B — Landing „Prezent na ślub” / `prezent-na-slub`: dead click na „Zamówienie przygotowujemy”

**Objaw:** (#13) Klik w ~3 s w tekście/elemencie „Zamówienie przygotowujemy” → **dead click**.

**Hipotezy:**

1. To **badge statusu** (informacja), ostylowany jak chip/link (`underline`, `cursor-pointer`, `hover`).
2. Nakładka lub rodzic bez akcji przechwytuje zdarzenie.

**Kroki rozwiązania:**

1. Zlokalizować string w CMS/szablonie frontendu (literówka w treści — rozważyć poprawkę copy na sensowny status, np. „Zamówienie w przygotowaniu” jeśli to status procesu, lub „Wysyłka / realizacja — …”).
2. Jeśli element **nie jest linkiem:**
   - Usunąć `cursor: pointer`, `:hover` sugerujące klik.
   - Ustawić `role="status"` lub `role="img"` + `aria-label` opisujące informację.
   - Nie stosować `onClick` bez nawigacji.
3. Jeśli **ma** prowadzić np. do FAQ o realizacji — zrobić z niego **`button`** lub **`a`** z jednoznacznym href i focus ring.
4. Nagranie Clarity po wdrożeniu: ten sam scenariusz nie pokazuje dead click na tym elemencie.

**Kryteria akceptacji P0-B:**

- [ ] Element nie wygląda jak interaktywny, jeśli nie wykonuje akcji — **albo** jest pełnoprawnym linkiem/przyciskiem z oczekiwanym efektem.
- [ ] Brak dead click na pierwszym naturalnym „sprawdzeniu” statusu przez użytkownika.

---

## P1 — Landing ślubny z Google: pierwszy ekran i pierwsza akcja

**Objaw:** Wiele sesji: wejście z Google na **`prezent-na-slub`** lub kategorię **„Prezent na ślub”**, **krótki czas**, **brak klików i scrolli** w Clarity (#6–#9, #16); część dłużej czyta bez klików (#15).

**Uwaga metodologiczna:** Brak scrolla w Clarity ≠ brak czytania; #15 sugeruje jednak że treść może „trzymać” bez CTA.

**Kroki rozwiązania:**

1. **Audyt pierwszego viewportu** (375px, 390px, 1440px): co widzi użytkownik **bez scrolla** — H1, zdjęcie, cena?, jedno główne CTA?
2. **H1 i podtytuł** zsynchronizować z intencją SERP (ślub / prezent / haft personalizowany); unikać ogólników jeśli Ads celuje w „prezent na ślub”.
3. **Jedno dominujące CTA** nad foldem: np. „Zaprojektuj zestaw na ślub” → najlepiej bezpośrednio do **konkretnego produktu bestselera** lub lista filtrowana (`docs/occasions_plan.md` wspomina filtrowanie wzorów ślubnych — sprawdzić czy działa po wejściu na landing).
4. **Drugie CTA** (outline): „Zobacz gotowe zestawy” → scroll do siatki / kotwica `#produkty`.
5. **Pas zaufania** nad lub pod hero (ikony + krótki tekst): czas realizacji, zwroty, bezpieczna dostawa, **link do realizacji** (realization gallery jeśli jest).
6. **Headline + produkt:** jeśli landing jest „okolicznościowy”, rozważyć **karuzelę 3 bestsellerów** widoczną bez scrolla na mobile.

**Kryteria akceptacji P1:**

- [ ] Na mobile w pierwszym ekranie widać **jasne CTA** i powód „dlaczego tu jestem”.
- [ ] Po wejściu z kampanii ślubnej użytkownik ma **jedno oczywiste następne kliknięcie** ≤10 s myślenia.
- [ ] (Opcjonalnie GA4) Event „cta_hero_slub_click” / scroll depth porównany przed/po.

---

## P2 — Wejście bezpośrednio do kreatora: wczesny drop-off

**Objaw:** (#4) ~16 s, jeden klik końcowy bez nawigacji; (#14) szybkie przełączanie zakładek po „Zacznij projektować”, potem kliki bez labeli — krótka sesja.

**Kroki rozwiązania:**

1. Pierwszy ekran kreatora: **loading skeleton** vs pusty stan — unikać „szarego pola” (`handoff/UX-mobile-kreator-optymalizacja.md` — domyślny kolor/produkt).
2. Po „Zacznij projektować”: **jednoznaczny focus** na pierwszym polu / pierwszej zakładce z krótkim tekstem „Krok 1: …”.
3. Zakładki: jeśli przełączanie jest zbyt szybkie → rozważyć **lazy mount** panelu bez „pustych” klików albo debounce; sprawdzić czy **tab bez treści** nie zaprasza do klikania pustki.
4. Instrumentacja: custom tag Clarity `Wizard_Step` przy zmianie kroku — korelacja z bounce.

**Kryteria akceptacji P2:**

- [ ] Brak „pustego” obszaru wyglądającego na klikalny zaraz po wejściu.
- [ ] **LCP / perceived readiness:** użytkownik widzi kompletny pierwszy krok < 2–3 s na typowym 4G (orientacyjnie).

---

## P3 — Homepage i treść pomocnicza

**Objaw:** (#5) literówka/sekcja „Eleganckie ręczniki z haf”; (#1–#2) krótkie wizyty.

**Kroki:**

1. Poprawić copy „z **haftem**” (lub zamierzoną frazę SEO).
2. Homepage: upewnić się, że **powyżej folda** jest ścieżka do okazji ślubnych podobna skutecznościowo do ścieżki z #5 (sekcja → prezent ślubny → kreator).

**Kryteria:** brak oczywistych błędów językowych w hero/sekcjach głównych.

---

## P4 — Zaufanie po regulaminie (bez przebudowy całego legal)

**Objaw:** (#10, #11) długa lektura regulaminu/polityki.

**Kroki:**

1. Na stronie koszyka i PDP: **skrót**: „Dostawa • Zwroty • Kontakt” z linkami (bez zmuszania do polityki).
2. Opcjonalnie **sticky** „Masz pytanie? Chat / tel.” na mobile w checkout — poza zakresem jeśli nie macie zasobów.

---

## P5 — Weryfikacja analityczna po wdrożeniu

1. Clarity: segment URL `contains` `wizard` — **Dead clicks / rage clicks** tygodniowo przed/po.
2. Landing `/prezent-na-slub`: **scroll depth**, **klik w hero CTA**, bounce rate (GA4).
3. Lista znanych elementów z PR + screenshoot „before/after” w komentarzu do taska.

---

## Atomowe zadania (AT-xx)

Szczegółowy, **atomowy** podział pracy (jedno AT ≈ jeden ticket lub jeden mały PR). Mapuje się na sekcje **P0–P5** powyżej.  
**Playwright:** tam gdzie potrzeba odtworzenia ścieżki lub regresji — jawna sugestia scenariusza.

### Faza 0 — Zrozumienie (bez zmian produktowych)

#### AT-01 — Inwentaryzacja dead clicks z Clarity (URL + czas + urządzenie)

| Pole | Treść |
|------|--------|
| **Problem** | Martwe kliknięcia są rozproszone po nagraniach (#3, #13, #17); bez spięcia z konkretnym selektorem trudno naprawiać. |
| **Cel** | Jedna lista: URL strony, przybliżony czas na timeline, typ urządzenia/przeglądarki z Clarity, tekst elementu (jeśli jest). |
| **Sugerowane kroki** | W panelu Clarity odfiltrować nagrania z dead click / rage click dla `reczniki-haftowane.pl`; wyeksportować lub skopiować metadane dla `/wizard/*`, `/prezent-na-slub`, kategorii ślubnej. |
| **Playwright** | Nie wymaga — chodzi o dane z Clarity. |

#### AT-02 — Mapa warstw (z-index) na stronie kreatora i landing ślubnym

| Pole | Treść |
|------|--------|
| **Problem** | Dead clicks często wynikają z **nakładki** (cookie, modal, sticky), nie z „martwego” przycisku. |
| **Cel** | Dokument (np. komentarz w issue): kolejność warstw dla `wizard` i `prezent-na-slub` — co jest na wierzchu po załadowaniu i po akceptacji cookies. |
| **Sugerowane kroki** | Na staging/prod w Chrome: Layers / nakładki po kolei wyłączać w DevTools (`display:none`) i sprawdzać, czy pod spodem jest oczekiwany cel kliknięcia. |
| **Playwright** | Opcjonalnie: screenshot po `page.goto` + po kliknięciu „Akceptuj cookies” — porównanie `boundingBox()` celów (diagnostyka). |

#### AT-03 — Playwright: smoke „ścieżka kreatora bez martwego UI”

| Pole | Treść |
|------|--------|
| **Problem** | Po naprawach trzeba powtarzalnie sprawdzać, że główna ścieżka nie ma „klik i nic”. |
| **Cel** | Jedna specyfikacja E2E (szkielet): URL produktu z kreatorem → zakładki **Produkt → Wzory → Nici → Czcionki** → po jednej opcji w każdej (jeśli dane testowe dostępne). |
| **Sugerowane kroki** | Zdefiniować staging URL i konto jeśli potrzeba; test na **widoczność** i brak overlay blokującego (`expect(locator).toBeVisible()`). |
| **Playwright** | **Tak — zalecane**; uruchomić po AT-10 / AT-11 lub jako regresja przed release. |

### Faza 1 — P0 Dead clicks (kreator)

#### AT-10 — Kreator: identyfikacja elementów z sesji #3 i #17

| Pole | Treść |
|------|--------|
| **Problem** | Dead clicks ~00:31, ~00:44, ~00:48, ~02:17, ~03:10 przy eksploracji zakładek i opcji. |
| **Cel** | Dla każdego timestampu: nazwa komponentu w kodzie (plik po odkryciu repo aplikacji). |
| **Sugerowane kroki** | Odtworzyć nagranie; zestawić z tekstem elementu z Clarity („Ręcznik …”, „Przejdź do zakładki”); wytypować siatkę wzorów, typ ręcznika, zakładki. |
| **Playwright** | Po znalezieniu selektorów: **`trace`** lub screenshot przy każdym kroku ścieżki testowej vs Clarity. |

#### AT-11 — Kreator: semantyka i hit area (klasa komponentów)

| Pole | Treść |
|------|--------|
| **Problem** | Wygląd przycisku bez działania lub za mały obszar dotyku. |
| **Cel** | Kafelek wzoru, opcja produktu, zakładka: **`button`** lub **`role="tab"`** + klawiatura; min. **44×44 px** na mobile. |
| **Sugerowane kroki** | `div`→`button` bez zmiany layoutu; `aria-selected` / `aria-current`; brak `pointer-events: none` na obsługiwanym dziecku. |
| **Playwright** | `click({ force: false })` na środku kafelka; viewport **390×844**. |

#### AT-12 — Kreator: stany wyłączone czytelne dla użytkownika

| Pole | Treść |
|------|--------|
| **Problem** | Kontrolka wygląda na aktywną, logika ignoruje klik → subiektywny dead click. |
| **Cel** | `aria-disabled="true"`, styl, tekst „Wybierz najpierw …” lub tooltip fokusowalny. |
| **Sugerowane kroki** | Mapowanie reguł biznesowych na copy UI. |
| **Playwright** | Stan niepełny: widoczny komunikat; brak mylącego `cursor-pointer` (np. klasa `cursor-not-allowed`). |

#### AT-13 — Kreator: cookie / tip / overlay vs pierwsze kliknięcia

| Pole | Treść |
|------|--------|
| **Problem** | Pierwsze sekundy (#14): szybkie kliki w zakładki i „puste” kliki; podobnie częściowo #3. |
| **Cel** | Cookies/tips nie zasłaniają pierwszego CTA; po akceptacji cookies brak przesunięcia layoutu powodującego pudło kliknięcia (CLS). |
| **Sugerowane kroki** | Kolejność mountu; opóźnić tooltip; `scroll-margin-top` pod sticky. |
| **Playwright** | Przed/po cookies — stabilny `boundingBox().y` dla „Zacznij projektować” (tolerancja kilka px). |

### Faza 2 — P0 Landing ślubny

#### AT-20 — `/prezent-na-slub`: „Zamówienie przygotowujemy” (#13)

| Pole | Treść |
|------|--------|
| **Problem** | Dead click ~3 s — element jak interaktywny lub przykryty. |
| **Cel** | Nieklikalna informacja (`role="status"`, bez pointer cursor) **albo** prawdziwy link/`button`. |
| **Sugerowane kroki** | Znaleźć w CMS/template; poprawić copy („w przygotowaniu”); jeśli FAQ — `href`. |
| **Playwright** | `goto` landing → klik w tekst statusu → nawigacja **lub** asercja `role=status` i brak działania linkowego jeśli nie-CTA. |

#### AT-21 — Landing: audyt pseudo-linków i badge’y

| Pole | Treść |
|------|--------|
| **Problem** | Bounce bez interakcji (#6–#9, #16) — użytkownik może nie widzieć **prawdziwego** CTA w pierwszym viewportcie. |
| **Cel** | Lista elementów nad foldem mobile: które są `<a>`/`<button>`, które tylko wyglądają jak przycisk. |
| **Sugerowane kroki** | Dla każdego „pseudo-CTA” — semantyka albo styl informacyjny. |
| **Playwright** | Liczba `a, button` widocznych w viewportcie ≥ **1** wyraźne główne CTA. |

### Faza 3 — P1 Konwersja pierwszego ekranu

#### AT-30 — Hero: jedna obietnica + jedno główne CTA

| Pole | Treść |
|------|--------|
| **Problem** | Krótkie wizyty bez klików (#7–#9, #16) vs długa lektura bez kliku (#15). |
| **Cel** | Pierwszy viewport: ślub + personalizacja + jedno dominujące CTA; secondary do `#produkty`. |
| **Sugerowane kroki** | Copy + design zsynchronizowane z SERP/Ads. |
| **Playwright** | H1 + główne CTA widoczne na **375px** i **1280px** (baseline screenshot opcjonalnie). |

#### AT-31 — Zgodność z `docs/occasions_plan.md` (filtrowanie ślubne)

| Pole | Treść |
|------|--------|
| **Problem** | Dokument zakłada filtrowanie po wejściu na `/prezent-na-slub`. |
| **Cel** | Lista/grid powiązana ze ślubem lub jasny komunikat filtrowania. |
| **Sugerowane kroki** | Weryfikacja implementacji w aplikacji; URL/store po mountcie. |
| **Playwright** | Po `goto('/prezent-na-slub')` — filtr/tag/produkt zgodnie z API. |

#### AT-32 — Pas zaufania (hero)

| Pole | Treść |
|------|--------|
| **Problem** | Sesje na regulamin/kontakt (#10) — część potrzebuje zaufania wcześniej w lejku. |
| **Cel** | 3–4 ikony + krótki tekst (realizacja, zwroty, dostawa — zgodnie z prawdą). |
| **Sugerowane kroki** | Komponent reużywalny PDP + landing okolicznościowy. |
| **Playwright** | Blok trust widoczny w viewportcie na `/prezent-na-slub`. |

### Faza 4 — P2 Wczesny drop-off kreatora

#### AT-40 — Domyślny stan produktu / anti pusty podgląd

| Pole | Treść |
|------|--------|
| **Problem** | #14 + mobile handoff — pusty/szary podgląd na starcie. |
| **Cel** | Domyślny sensowny stan + skeleton podczas load. |
| **Sugerowane kroki** | Defaults w konfiguracji produktu/kreatora. |
| **Playwright** | Po wejściu w wizard — podgląd/canvas/img w timeout; brak nieskończonego spinnera. |

#### AT-41 — Onboarding po „Zacznij projektować”

| Pole | Treść |
|------|--------|
| **Problem** | #14 — szybkie przełączanie zakładek, niepewność kolejnego kroku. |
| **Cel** | „Krok 1: …” lub wyraźne `aria-current` + focus na pierwszym polu. |
| **Sugerowane kroki** | Mikrokopiowanie; opcjonalnie lekki tooltip (nie blokujący). |
| **Playwright** | Po starcie — widoczny komunikat kroku lub `aria-current` na właściwej zakładce. |

### Faza 5 — P3 Copy

#### AT-50 — Homepage: „Eleganckie ręczniki z haf” (#5)

| Pole | Treść |
|------|--------|
| **Problem** | Literówka „haft”. |
| **Cel** | Poprawny tekst w CMS/komponencie. |
| **Playwright** | Opcjonalnie: asercja że nie występuje substring „z haf” jako błąd (ostrożnie z treścią dynamiczną). |

### Faza 6 — Metryki

#### AT-60 — Checklista Clarity + GA4

| Pole | Treść |
|------|--------|
| **Problem** | Brak pomiaru → brak potwierdzenia poprawy. |
| **Cel** | Snapshot tygodniowy: dead clicks `/wizard`, bounce `/prezent-na-slub`, scroll depth. |
| **Sugerowane kroki** | Ten sam okres 7 dni przed/po deployu; notatka w release. |
| **Playwright** | Nie zastępuje analityki. |

### Sugerowana kolejność atomowa (plan)

1. **AT-01 → AT-02**  
2. **AT-10**  
3. **AT-20 → AT-21**  
4. **AT-11 → AT-12 → AT-13**  
5. **AT-30 → AT-31 → AT-32**  
6. **AT-40 → AT-41**  
7. **AT-03** (regresja)  
8. **AT-50**, **AT-60**

---

## Kolejność realizacji (priorytety P0–P5)

1. **P0-A** + **P0-B** równolegle (różni deweloperzy lub najpierw P0-B jako szybki fix copy/DOM) — szczegóły atomowe: **AT-01–AT-13**, **AT-20–AT-21**.
2. **P1** — **AT-30–AT-32**.
3. **P2** — **AT-40–AT-41**.
4. **P3**, **P4**, **P5** — m.in. **AT-50**, checklista **AT-60**.

---

## Blokada środowiska (ten orchestrator)

Repozytorium **`reczniki-haftowane.pl`** (orchestrator) **nie zawiera** kodu sklepu SPA pod ścieżkami `/wizard`, `/prezent-na-slub`. **Implementacja wymaga repozytorium aplikacji** w `apps/reczniki-haftowane/` (lub innym wskazanym przez zespół).

**Frontend:** po wdrożeniu — commit wg konwencji repo aplikacji (`feat(wizard): …` / `fix(landing): …`). Push po weryfikacji — zgodnie z `AGENTS.md` / DevOps.

---

## Powiązane dokumenty

- `docs/audit-ux-kreator-sugestie.md` — surowe wpisy Clarity
- `handoff/UX-mobile-kreator-optymalizacja.md`
- `docs/occasions_plan.md` — landing ślubny i filtrowanie wzorów

*(Plan atomowy **AT-xx** jest w sekcji „Atomowe zadania” powyżej — osobny plik `PLAN_UX_atomic_clarity_fixes.md` nie jest utrzymywany.)*
