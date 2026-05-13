# Strategia marketingowa — `reczniki-haftowane.pl`

**Rola dokumentu:** nadrzędny plan kanałów i celów. Szczegóły płatnych kampanii: [marketing/google-ads/campaign-plan-small-budget.md](google-ads/campaign-plan-small-budget.md). Frazy i grupy pod Search: [docs/ads_ready_phrases.md](../docs/ads_ready_phrases.md).

**Dane do uzupełnienia z biznesu:** średnia marża brutto na zamówienie, koszt obsługi zamówienia, udział klientów powracających — bez tego break-even ROAS/CAC w tabeli poniżej pozostaje szacunkiem.

---

## 1. Cele biznesowe (ramowe)

| Obszar | Cel operacyjny | Jak mierzymy |
|--------|------------------|--------------|
| Przychód | Skalowanie sprzedaży zestawów prezentowych o wyższej wart koszyka | GA4: `purchase` (wartość), raporty sklepu |
| Marża | Priorytet SKU z wyższą marżą jednostkową (zestawy w koszu, wyższe ceny) | KPI produktowe + GMC / Ads |
| Efektywność płatna | ROAS i CPA zgodne z progiem rentowności po marży | Google Ads, porównanie z break-even ROAS |
| Organika | Utrzymanie i wzrost widoczności na frazy prezentowe i transakcyjne | GSC, [docs/urls_audit.csv](../docs/urls_audit.csv) |

**Break-even ROAS (szkic):** `ROAS_min ≈ cena sprzedaży / marża_kontribucyjna_na_sztuce` (uwzględnij koszt produkcji, pakowania, prowizji płatności, koszt wysyłki średniej). Ustal konkretny próg w arkuszu marży i wpisz tutaj jako „ROAS docelowy konta”.

---

## 2. Persony i intencja

- **Kupujący prezent (B2C):** szuka gotowego, „ładnego” upominku pod określoną okazję; niska tolerancja na skomplikowany UX w kreatorze.
- **Para / rodzina:** zestawy wieloosobowe, personalizacja imion, kosz jako element „do wręczenia”.
- **B2B (opcjonalnie):** firmowe upominki — jeśli kanał jest aktywny, dopisz osobną ścieżkę landingów i komunikacji.

Persony wiążą się z nawigacją okolicznościową: [docs/occasions_plan.md](../docs/occasions_plan.md) (landingi `/prezent-na-slub`, `/prezent-na-rocznice`, itd.).

---

## 3. Mix kanałów

| Kanał | Rola | Materiały w repo |
|-------|------|------------------|
| **SEO + treść** | Trwały ruch na frazy okolicznościowe i produktowe; spójność z menu OKAZJE | [docs/occasions_plan.md](../docs/occasions_plan.md), [docs/redirects_plan_301.md](../docs/redirects_plan_301.md), [docs/urls_audit_pages.csv](../docs/urls_audit_pages.csv) |
| **Google Ads (Shopping)** | Szybka widoczność na intencję zakupową, katalog 8 SKU | [marketing/google-ads/campaign-plan-small-budget.md](google-ads/campaign-plan-small-budget.md), [marketing/google-ads/google_merchant_feed.xml](google-ads/google_merchant_feed.xml) |
| **Google Ads (Search)** | Frazy z potencjałem, słabsza pozycja organiczna; ścisła kontrola zapytań | [docs/ads_ready_phrases.md](../docs/ads_ready_phrases.md) |
| **Remarketing / e-mail** | Odzyskanie porzuconych konfiguracji w kreatorze, powroty sezonowe | Wymaga list odbiorców (Ads, klient sklepu) i zgód RODO — wdrożenie poza tym plikiem |
| **Social** | Dowód społeczny, sezonowe kampanie (Meta itd.) | Nie opisane w repo — rezerwuj budżet i kalendarz jeśli aktywne |

**Zasada:** płatne kampanie i SEO mają wskazywać na te same landingi okolicznościowe tam, gdzie intencja jest prezentowa (zgodnie z mapowaniem w `occasions_plan`).

---

## 4. Kalendarz sezonowy (orientacyjny)

| Okres | Akcent komunikacji | Notatka |
|-------|-------------------|---------|
| Q4 (listopad–grudzień) | Święta, prezenty zbiorowe | Landing `/prezent-na-swieta` (menu w occasions_plan) |
| Luty | Walentynki | `/prezent-na-walentynki` |
| Wiosna / wczesne lato | Komunie (jeśli oferta trafia do segmentu) | Oceń dopasowanie produktu |
| Cały rok | Ślub, rocznica, parapetówka, urodziny | Priorytet w feedzie i w SEO zgodnie z `occasions_plan` |

---

## 5. Budżet i przeglądy

- **Paid (szkic):** bazowo **30 zł/dzień** — szczegół w planie Google Ads; ewentualny podział Shopping vs Search opisany w pliku kampanii.
- **Cotygodniowo:** przegląd search terms (Search + Shopping), negatywy, anomalie CPC/CTR.
- **Miesięcznie:** struktura kampanii, priorytety produktów w feedzie, zgodność landingów z GSC (nowe frazy w [docs/ads_ready_phrases.md](../docs/ads_ready_phrases.md)).

---

## 6. Analityka

- **GA4:** lejek `view_item` → `purchase` (już wzmiankowane w planie Ads).
- **Microsoft Clarity:** kroki kreatora (`Wizard_*`) — optymalizacja UX pod konwersję.
- **GSC:** źródło list fraz do Ads i do treści SEO ([docs/ads_ready_phrases.md](../docs/ads_ready_phrases.md)).

---

*Ostatnia aktualizacja struktury dokumentu: 2026-05-13.*
