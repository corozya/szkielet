# TASK: Kreator — moment pobierania list katalogowych (drawings, czcionki, …) + cache

## Meta

| Pole | Wartość |
|------|---------|
| **Problem obserwowany** | Po wejściu do kreatora od razu leci m.in. `GET /api/v1/drawings` (lokalnie np. `http://127.0.0.1:5173/api/v1/drawings`). Podejrzenie: pełny „katalog” (wzory, czcionki, nici itd.) ładuje się zanim użytkownik faktycznie tego potrzebuje. |
| **Cel** | **Przeanalizować** kiedy dane muszą być dostępne (intro, pierwszy render, wybór produktu, zakładka **Wzory** / **Czcionki** / **Nici**) i czy opłaca się **opóźnić** fetch lub **rozbić** zapytania — **bez** wielokrotnego pobierania tych samych dzięki cache. |
| **Priorytet** | Do ustalenia po analizie (wpływ: TTFB pierwszego ekranu kreatora, rozmiar odpowiedzi, równoległe zapytania przy starcie). |
| **Owner** | Frontend (`apps/reczniki-haftowane/`) |
| **Status** | Wdrożone |
| **Data briefu** | 2026-05-16 |

---

## Kontekst

- Dzisiaj dane katalogowe mogą być ciągnięte **monolitycznie na mount** ścieżki kreatora (`/wizard/...`), co konkuruje z innymi requestami (settings, produkt, prefety z URL).
- **Lazy load per zakładka** (np. drawings dopiero po wejściu w „Wzory”) może przyspieszyć perceived performance użytkownika, który najpierw zmienia produkt lub czyta intro.
- Ryzyko opóźnienia: **prefill z URL / preset**, walidacja wybranego `drawing_id` zanim użytkownik otworzy zakładkę, podgląd na pierwszym ekranie — trzeba sprawdzić w kodzie zależności.

---

## Zakres analizy (checklista)

1. **Inwentaryzacja requestów przy wejściu do kreatora** — Network tab / kod: które endpointy (`/drawings`, fonts, threads, `wizzard/options`, …) i w jakiej kolejności; które są warunkowe.
2. **Mapa zależności UI** — czy pierwszy paint / intro / wybór produktu wymaga pełnej listy drawings; czy wystarczy ID + meta z innego źródła.
3. **Warianty strategii** (do omówienia):
   - **A:** fetch przy pierwszym wejściu do kreatora, ale **po** krytycznym łańcuchu (settings + aktualny produkt), reszta `requestIdleCallback` / kolejka.
   - **B:** **osobne query per zasób**, włączone dopiero gdy zakładka jest aktywna lub użytkownik hover/focus na tab.
   - **C:** jeden zagregowany endpoint vs wiele małych — koszt RTT vs rozmiar payloadu.
4. **Cache / deduplikacja** — jeśli używane jest React Query (lub podobne): `staleTime`, `gcTime`, wspólny `queryKey`, prefetch przy najechaniu na tab, brak podwójnego mount w Strict Mode (jeśli dotyczy).
5. **Edge cases** — preset z realizacji, deep link z `drawing` w query, przełączenie produktu wymuszające inny podzbiór wzorów (jeśli jest filtrowanie).
6. **Metryki** — przed/po: liczba równoległych requestów przy cold start, czas do interaktywnego pierwszego kroku, rozmiar JSON.

---

## Kryteria akceptacji (faza 1 — analiza)

- [ ] Krótki dokument (w komentarzu do issue / w tym pliku sekcja „Wnioski”) z **rekomendacją**: zostawiamy jak jest / lazy per zasób / hybryda + uzasadnienie.
- [ ] Lista endpointów „start kreatora” vs „po akcji użytkownika”.
- [ ] Jeśli wdrożenie: brak regresji presetów URL i podglądu; **jedna** kopia danych w cache po nawigacji wewnątrz kreatora (brak zbędnych duplikatów fetch).

---

## Kryteria akceptacji (faza 2 — opcjonalne wdrożenie)

- [ ] Zmiana momentu lub granularności fetch zgodna z ustaleniami z fazy 1.
- [ ] Cache: konfiguracja `staleTime` (lub równoważnik) zapobiega powtarzaniu identycznych GET przy przełączaniu zakładek w tej samej sesji.
- [ ] Smoke / E2E: wejście w kreator → przejście **Produkt → Wzory → Czcionki** (lub minimalna ścieżka z briefu UX) bez błędów i bez „pustych” list po pierwszym otwarciu zakładki.

---

## Powiązania

- `handoff/TASK_performance_pagespeed_optimization_benchmark.md` — szerszy performance site.
- `handoff/UX-mobile-kreator-optymalizacja.md` — mobile first screen / skeleton.
- `handoff/TASK_UX_clarity_session_fixes_dead_clicks_landings.md` — tarcie UX; opóźniony fetch może wpłynąć na timing overlay / pierwszej interakcji (zweryfikować).

## Wnioski z audytu kodu

### Co dziś dzieje się na mount

- `useEmbroideryAssets()` odpala od razu trzy query: `['drawings']`, `['fonts']`, `['threads']` bez `enabled` i bez warunków wejścia.
  - Użycia: `WizardPage`, `WizardLoader`, `useProductPageLogic`, `CartPage`, `CheckoutPage`.
- `useProductPageLogic()` odpala dodatkowo `['drawings-grouped']` na starcie.
- Query cache już istnieje globalnie:
  - `staleTime: 5 min`
  - `gcTime: 10 min`
  - więc problemem nie są głównie duplikaty przy przejściach, tylko zbyt wczesny start całego katalogu.

### Co jest naprawdę potrzebne od razu

- `product` i `wizard_default_config` muszą wejść wcześnie.
- `drawings` jest potrzebne tylko w części scenariuszy:
  - preset / deep link z `drawing_id` lub `text`
  - kartka `Intro` z już skonfigurowanym slotem
  - otwarcie zakładki `Wzory`
- `fonts` i `threads` są potrzebne przy:
  - otwarciu zakładek `Czcionki` / `Nici`
  - introspekcji istniejącej konfiguracji, jeśli chcemy pokazać pełny preview
- `drawings-grouped` jest potrzebne tylko dla widoku wzorów i dla enrichementu preview, nie dla samego wejścia do kreatora.

### Krytyczne zależności UI

- `PersonalizationIntro` potrafi działać w stanie pustym bez pełnego katalogu i pokazuje placeholdery.
- `WizzardControlPanel` ma naturalny podział:
  - `Produkt` nie wymaga katalogu assetów
  - `Wzory` wymaga `drawings` + `drawingsGrouped`
  - `Nici` wymaga `threads`
  - `Czcionki` wymaga `fonts`
- `useWizardInitialization()` używa `drawings` tylko do legacy/preset tekstu:
  - bez `text` / `drawing_id` nie potrzebuje katalogu na starcie.

### Rekomendacja

- Nie trzymać wszystkiego jako jednego eager fetch na mount.
- Zastosować **hybrydę**:
  - eager tylko to, co blokuje pierwszy sensowny render i preset,
  - reszta lazy per zasób / per zakładka,
  - prefetch przy hover/focus na tab, żeby nie pokazywać pustych stanów po kliknięciu.
- Nie rozbijać cache na nowe, niespójne klucze bez potrzeby. Zostawić jedne stabilne queryKey per zasób, żeby dane współdzieliły się między wizardem, produktem i koszykiem.

## Wnioski

- `Start kreatora`:
  - `product`
  - `wizard_default_config`
  - `drawings` i `drawings-grouped` tylko gdy istnieje preset / już skonfigurowany haft
  - `fonts` i `threads` tylko gdy kreator ma już istniejącą konfigurację albo użytkownik otwiera odpowiedni tab
- `Po akcji użytkownika`:
  - hover / focus na `Wzory` -> prefetch `drawings` + `drawings-grouped`
  - hover / focus na `Czcionki` -> prefetch `fonts`
  - hover / focus na `Nici` -> prefetch `threads`
  - kliknięcie taba uruchamia właściwy query, jeśli cache jeszcze jest pusty
- Cache pozostaje wspólny:
  - te same `queryKey`
  - `staleTime` i `gcTime` z globalnego `QueryClient`
  - brak duplikatów przy przejściach w obrębie kreatora

### Zmiana w kodzie

- `useEmbroideryAssets()` dostał opcje `enabled` per zasób oraz helper `useEmbroideryAssetPrefetch()`.
- `WizzardControlPanel` uruchamia fetch tylko dla aktywnego taba i warm-up na hover/focus.
- `SetVisualization` nie pobiera `drawings-grouped`, jeśli nie ma żadnych referencji do haftu w konfiguracji.
- `WizardLoader` i logika produktu nie odpalają katalogu na pustym wejściu do kreatora.

## Proponowany plan prac

### Faza 1 — implementacja strategii ładowania

1. Rozdzielić katalog na osobne warstwy pobierania:
   - `drawings`
   - `drawings-grouped`
   - `fonts`
   - `threads`
2. Dodać warunkowe uruchamianie query:
   - lazy po otwarciu tabów,
   - eager tylko dla presetów / trybu edycji / konfiguracji z już wybranym assetem.
3. Dodać prefetch na hover/focus tabów `Wzory`, `Nici`, `Czcionki`.
4. Upewnić się, że `add-to-cart` i zapis edycji koszyka korzystają z danych z cache albo dociągają brakujące assety przed snapshotem.

### Faza 2 — zabezpieczenia regresji

1. Sprawdzić scenariusze:
   - wejście do kreatora bez konfiguracji,
   - preset z `drawing_id` / `font_id` / `thread_id` / `text`,
   - otwarcie `Wzory` po starcie bez katalogu,
   - edycja pozycji z koszyka.
2. Dodać testy jednostkowe / integracyjne dla:
   - braku requestów katalogowych na pustym intro,
   - fetchu po wejściu w konkretną zakładkę,
   - poprawnej inicjalizacji presetów.
3. Zweryfikować network:
   - liczba requestów przy cold start,
   - kolejność requestów,
   - brak podwójnego pobrania po nawigacji w obrębie kreatora.

### Faza 3 — decyzja końcowa

1. Jeśli zysk z lazy load jest mierzalny i nie psuje presetów, zostawić hybrydę.
2. Jeśli uproszczenie kodu ma większą wartość niż oszczędność RTT, zatrzymać tylko podział query i ograniczyć eager fetch do minimum.
3. Jeśli `drawingsGrouped` okaże się jedynym realnym bottleneckiem, najpierw odciąć właśnie ten request, a resztę zostawić na później.
