# TASK_20 — Google Merchant feed: kompletność i obrazy produktu

## Cel
- Uporządkować feed Google Merchant Center tak, żeby był zgodny z wymaganiami Google i lepiej nadawał się do Shopping/PMax.

## Kontekst
- Feed działa pod `GET /feed/google-merchant.xml`.
- Aktualnie `g:image_link` jest wyliczany przez backendowy kontroler feedu.
- Feed ma podstawowe pola, ale brakuje części sygnałów, które pomagają w zgodności i skuteczności reklam.

## Podzadania
- [ ] Zmienić logikę generowania `g:image_link` tak, żeby feed brał obraz produktu z galerii jako podstawowe źródło.
- [ ] Użyć jako zdjęcia produktu pierwszego zdjęcia z galerii, jeśli produkt ma przypisaną galerię.
- [ ] Zostawić fallback tylko wtedy, gdy produkt nie ma żadnego zdjęcia w galerii.
- [ ] Dodać `g:additional_image_link` dla pozostałych zdjęć z galerii, do limitu 10 dodatkowych obrazów.
- [ ] Dodać `g:google_product_category` dla ręczników / tekstyliów domowych.
- [ ] Poprawić `g:identifier_exists` na wartość zgodną ze specyfikacją Google (`no` dla custom/handmade bez GTIN/MPN).
- [ ] Ocenić, czy warto dodać `g:sale_price` i `g:sale_price_effective_date` dla okazji / promocji.
- [ ] Ocenić, czy potrzebny jest `g:shipping` w feedzie, czy wystarczy konfiguracja shipping w Merchant Center.
- [ ] Zweryfikować, czy `product_type` odzwierciedla strukturę sklepu i czy warto go rozbić na bardziej semantyczne gałęzie.
- [ ] Zweryfikować wynik na przykładowym produkcie i sprawdzić, czy XML odpowiada wymogom Merchant Center.

## Weryfikacja
- Feed XML dla produktu z galerią pokazuje pierwszy obraz z galerii w `g:image_link`.
- Dodatkowe obrazy są eksportowane jako `g:additional_image_link`.
- `g:identifier_exists` ma wartość zgodną ze specyfikacją Google.
- Feed zawiera sensowną kategorię Google i nie używa placeholderów jako głównego obrazu.
- Produkt bez galerii nadal ma sensowny fallback.
- Wygenerowany XML przechodzi podstawową walidację i nadal zwraca `200`.

## Status
- owner: Backend
- state: done
