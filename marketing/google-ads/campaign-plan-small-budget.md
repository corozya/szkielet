# Plan kampanii Google Ads dla `reczniki-haftowane.pl` (Aktualizacja: 13.05.2026)

Cel: zdobycie średnio 1 zamówienia dziennie przy budżecie **30 zł/dzień**, skupiając się na produktach o najwyższej marży i potencjale prezentowym.

**Kontekst strategii:** [marketing/MARKETING_PLAN.md](../MARKETING_PLAN.md). Frazy i grupy pod Search: [docs/ads_ready_phrases.md](../../docs/ads_ready_phrases.md).

**Konto Google Ads (produkcja):** „Ręczniki Haftowane”, **customer ID `513-517-5046`**. Kampanie **Shopping** / **Search** uruchamiaj na tym CID. W GMC podpięte jest też drugie konto Ads — **nie** używaj go do kampanii sklepu (albo odłącz w GMC, jeśli zbędne).

---

## 1) Produkty priorytetowe

**Tier A (główny nacisk bidów i komunikacji):**

1. **Zestaw ID 8** — rodzinny zestaw w koszu (299 zł): wysoka wartość koszyka, „duży prezent”.
2. **Zestaw ID 7** — para w koszu / ślub, rocznica (219 zł): wysoka rotacja, jasna intencja zakupowa.

**Tier B (wysoki AOV — utrzymanie w feedzie, stawki pod kontrolą segmentu cenowego):**

3. **Zestaw ID 17** — XXL, 339 zł: potencjalnie wysoka marża jednostkowa; obserwuj ROAS w raporcie produktów GMC/Ads. Jeśli CR lub marża gorsze niż 7/8, **nie podbijaj** CPC ponad Tier A bez danych.

**Źródło danych dla GMC:** kanoniczny feed produkcyjny [https://reczniki-haftowane.pl/feed/google-merchant.xml](https://reczniki-haftowane.pl/feed/google-merchant.xml) (scheduled fetch). Plik [marketing/google-ads/google_merchant_feed.xml](google_merchant_feed.xml) w repo jest **mirrorem** do review i diffów — utrzymuj go zgodnie z URL (lub generuj z aplikacji). Łącznie **8 produktów**.

---

## 2) Strategia feedu (zrealizowane w repo)

Ręczny feed XML zamiast automatycznego — copy pod okazje i produkt:

- **Tytuły:** okazje (ślub, rocznica, kosz, prezent).
- **Opisy:** gramatura, haft premium, gotowość do wręczenia.
- **Custom labels (`g:custom_label_2`):**
  - **`price_100_plus`** — SKU ≥ ~100 zł (większość zestawów): wyższy zakres CPC / wyższy priorytet przy optymalizacji.
  - **`price_60_99`** — tańsze SKU w feedzie: **niższy** CPC docelowy niż dla `price_100_plus`, żeby nie palić budżetu na niższy AOV.

Pozostałe etykiety (`custom_label_0` / `1`) służą segmentacji okazji i typu zestawu — przydatne przy raportach i ewentualnym podziale produktów na grupy produktów w Ads.

---

## 3) Analityka i konwersje (zrealizowane)

1. **Microsoft Clarity:** kroki Kreatora Haftu — tagi `Wizard_Step`, `Wizard_Product`, `Wizard_Current_Towel` (wąskie gardła, zwłaszcza przy zestawach 7 i 8).
2. **GA4:** lejek `view_item` → `purchase`.

---

## 4) Struktura kampanii w Google Ads

### Kampania: `Shopping | Bestsellers | Manual CPC`

- **Typ:** Standard Shopping (zamiast PMax przy małym budżecie — większa kontrola stawek i zapytań).
- **Zakres:** 8 aktywnych produktów z XML; nacisk bidów Tier A > Tier B > pozostałe zgodnie z `custom_label_2` i wynikami.
- **Stawki:** Manual CPC z eCPC. Cel CPC: **0,60–0,90 zł** (dostosuj per segment `price_100_plus` vs `price_60_99`).
- **Budżet:** **30 zł/dzień** na całość konta w wariancie „tylko Shopping”; jeśli działa też Search, zwiększ dzienny cap lub rozdziel budżety (patrz niżej).

### Kampania (opcjonalna): `Search | Intencja zakupowa`

**Budżet:** przy całkowitym limicie 30 zł/dzień — **bezpieczny start: 6–9 zł/dzień na Search** (20–30%), reszta Shopping; albo **osobny dzienny cap** (np. 40 zł sumarycznie), jeśli Shopping stabilnie się broni.

**Grupy reklam** — mapowanie na [docs/ads_ready_phrases.md](../../docs/ads_ready_phrases.md):

| Grupa | Przykładowe frazy | Match types | Landing (intencja) |
|-------|-------------------|-------------|-------------------|
| Haft na ręczniku | ręczniki z haftem, haft na ręczniku, haft na ręcznikach | [Exact] + wybrane [Phrase] na warianty zamówieniowe | Strona kategorii / bestseller lub `/wizzard` z jasnym CTA — testuj |
| Personalizacja | personalizowane ręczniki, ręcznik personalizowany | [Exact], [Phrase] | Produkt lub landing okolicznościowy z [docs/occasions_plan.md](../../docs/occasions_plan.md) |
| Zamówienie | ręczniki z haftem na zamówienie, ręczniki haftowane na zamówienie | [Exact], [Phrase] | Produkt + zaufanie (dostawa, realizacja) |
| Prezent / okazja | ręczniki z haftem na prezent, na ślubie, na urodziny | głównie [Exact] | **`/prezent-na-slub`**, **`/prezent-na-urodziny`**, itd. wg mapy okazji |

**Negatywy (lista startowa — dopasuj pod rzeczywiste search terms):**  
`darmowe`, `diy`, `jak zrobić`, `wzór`, `szablon`, `allegro`, `olx`, `vinted`, `hurt`, `b2b`, `używane`, `pdf`, `haft maszynowy używana` (warianty), zapytania informacyjne bez intencji zakupu.

**Shopping + Search (kanibalizacja):**

- Search na **węższych** frazach transakcyjnych/prezentowych; szerokie head-terms zostaw na Shopping.
- Jeśli to samo zapytanie generuje duplikaty kosztów: obniż CPC Search lub dodaj negatywy frazowe na Search dla zapytań, które i tak wygrywa Shopping po niskim CPA.
- Rozważ **wykluczenia listy remarketingowej** lub RLSA (tylko „nowi” vs „powracający”) po zebraniu danych — wymaga list w Ads.

---

## 5) Harmonogram i działania

| Krok | Status | Zadanie |
| :--- | :---: | :--- |
| 1a. Feed produkcyjny | ✅ | URL `…/feed/google-merchant.xml` — źródło dla Merchant Center. |
| 1b. Mirror w repo | ✅ | [google_merchant_feed.xml](google_merchant_feed.xml) zsynchronizowany z produkcją (dodatkowe obrazy, wagi, `identifier_exists`, kategoria tekstowa). |
| 1c. Merchant Center | ✅ | Nowy feed w GMC, produkty zaktualizowane. Utrzymaj **scheduled fetch** na `https://reczniki-haftowane.pl/feed/google-merchant.xml` i monitoruj „Ostatni import”. |
| 2. Tracking | ✅ / ⏳ | Clarity aktywne; dokończyć weryfikację tagów w panelu. |
| 3. Launch Shopping | ⏳ | **Brak kampanii w Ads** — następny krok: utworzyć **Standard Shopping** (nie PMax), patrz [§8](#8-pierwsza-kampania-standard-shopping-krok-po-kroku). |
| 4. Launch Search (opcjonalnie) | ⏳ | Po stabilnym Shopping lub z osobnym capie budżetu. |
| 5. Optymalizacja | ⏳ | Po ~7 dniach: negatywy z search terms (**Search i Shopping**), przegląd produktów o słabym ROAS. |

---

## 6) Oczekiwany efekt (dzienne KPI)

- **Kliknięcia:** ok. 35–50 dziennie przy samym Shopping ~30 zł i CPC w zakresie powyżej.
- **CR (sesja płatna):** 2–3% — warto zweryfikować **osobno dla ruchu płatnego** w GA4 (często niższe niż średnia sklepu).
- **Zamówienia:** ok. **1/dzień** przy powyższych założeniach.
- **ROAS:**
  - **Konto / kampania:** cel zgodny z progiem rentowności z [marketing/MARKETING_PLAN.md](../MARKETING_PLAN.md) (break-even z marży).
  - **„Min. 6,0 dla zestawu nr 8”:** KPI **produktowe** — raport produktów w Google Ads lub Merchant Center (koszt reklamy przypisany do konwersji na SKU 8), a nie jedynie średnia ROAS całej kampanii z 8 pozycjami.

---

## 7) Weryfikacja domknięcia (checklist)

**Domknięte (potwierdzone / technicznie OK):**

| Punkt | Uwagi |
|--------|--------|
| Feed URL | `GET https://reczniki-haftowane.pl/feed/google-merchant.xml` → **200**, treść XML (weryfikacja zdalna 2026-05-13). |
| GMC — import | Potwierdzone przez Ciebie: nowy feed, produkty zaktualizowane. |
| Mirror w repo | [google_merchant_feed.xml](google_merchant_feed.xml) — do ewentualnego diffu z produkcją po zmianach w sklepie. |

**Do potwierdzenia w panelach (5–10 min):**

| Punkt | Gdzie | Co sprawdzić |
|--------|--------|----------------|
| Ostatni fetch | GMC → **Produkty** / źródło danych | Status **ukończony**, brak masowych błędów; data ostatniego przetworzenia. |
| Diagnostyka | GMC | Brak **krytycznych** alertów na poziomie konta i produktów (cena, dostępność, zdjęcia, `identifier_exists`). |
| Połączenie z Ads | GMC / Ads | Merchant połączony z Ads; **kampanie tylko na CID `513-517-5046`** (Ręczniki Haftowane). |
| Domena i zweryfikowany sklep | GMC | Claim strony / weryfikacja zgodna z praktyką konta. |
| GA4 + konwersje | GA4 / Ads | Import konwersji „zakup” (lub primary conversion) do Ads — **Test** w tagu lub pierwsze testowe zamówienie. |
| Clarity | Clarity | Nagrania / tagi `Wizard_*` jeśli nadal włączasz optymalizację kreatora. |

**Nadal otwarte względem planu uruchomienia kampanii:**

| Krok | Status |
|------|--------|
| **3. Launch Shopping** | ⏳ **Nie utworzono** — pierwsza kampania w Google Ads; postępuj wg [§8](#8-pierwsza-kampania-standard-shopping-krok-po-kroku). |
| **4. Search** | ⏳ Opcjonalnie po stabilnym Shopping. |
| **5. Optymalizacja** | ⏳ Po ~7 dniach od startu reklam (negatywy, ROAS per SKU). |
| **2. Tracking** | ✅ / ⏳ Domknij weryfikację tagów w GA4/GTM jeśli coś jeszcze nie jest „Verified” w Ads. |

---

## 8) Pierwsza kampania Standard Shopping (krok po kroku)

**Warunek:** to samo konto **Merchant Center** co feed oraz konto Google Ads **513-517-5046** (patrz nagłówek dokumentu i checklist §7).

1. W Google Ads: **Utwórz** → **Nowa kampania** (lub odpowiednik w Twojej wersji językowej panelu).
2. Cel: np. **Sprzedaż** / **Sprzedawaj produkty z katalogu** — wybierz ścieżkę prowadzącą do **Shopping**.
3. **Ważne:** wybierz typ **Standardowa kampania produktowa** (**Standard Shopping**), **nie** Performance Max — zgodnie z [§4](#4-struktura-kampanii-w-google-ads) tego dokumentu (kontrola budżetu i CPC przy małym daily cap).
4. Powiąż **konto Merchant Center** (wybierz właściwe ID sklepu).
5. **Kraj sprzedaży:** Polska (lub zgodnie z wysyłką). **Oferty:** z podłączonego katalogu (8 produktów z feedu).
6. **Budżet:** ok. **30 zł/dzień** (kampania tylko Shopping; Search dodasz później osobno).
7. **Strategia ofert:** **Ręczne ustawianie stawek CPC** (Manual CPC); opcjonalnie włącz **ulepszanie CPC** (eCPC), jeśli akceptujesz automatyczne korekty stawki w granicach celu.
8. Utwórz **grupę reklam** — przy ośmiu SKU możesz zacząć od **wszystkich produktów** w jednej grupie; później podział po `custom_label_2` (`price_100_plus` vs `price_60_99`) pod różne stawki.
9. Zapisz kampanię; sprawdź status **kwalifikacji** reklam i czy produkty nie są odrzucone (szczegóły w GMC).
10. Po 24–48 h: pierwsze wrażenia z wyświetleń / kliknięć; po **~7 dniach** przejdź do kroku harmonogramu **5** (negatywy, ROAS).

Dokumentacja Google (oficjalna, UI bywa aktualizowany): [Tworzenie kampanii Shopping](https://support.google.com/google-ads/answer/3455581).

---

*Plan zaktualizowany: docelowe konto Ads CID 513-517-5046.*
