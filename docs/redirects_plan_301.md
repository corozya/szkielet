# Plan przekierowań 301 — wycofane produkty
**Data:** 2026-05-12
**Kontekst:** Przebudowa strony — zachowanie autorytetu SEO dla wycofanych URL-i

## Przekierowania pilne (produkty "tortów" — widoczne w GSC)

| Stary URL | Nowy URL | Powód | Priorytet |
|-----------|----------|-------|-----------|
| `/oferta/tort-z-2-haftowanych-recznikow.html` | `/products/2-duze-reczniki-kosz` | Najbliższy odpowiednik (2 ręczniki kąpielowe w koszu); poz. 7.7 w GSC — pilne | 🔴 PILNE |
| `/oferta/tort-z-haftowanych-recznikow.html` | `/products/2-duze-reczniki-kosz` | Ogólna strona tortu — ten sam cel | 🔴 PILNE |

## Przekierowania starych URL-i na nowe (stary silnik → nowy)

| Stary URL | Nowy URL | Uwagi |
|-----------|----------|-------|
| `/oferta/personalizowane.html` | `/wizzard` | Strona personalizacji → kreator |
| `/oferta/zestaw-4-haftowanych-recznikow-w-koszu.html` | `/products/zestaw-4-recznikow-kosz` (lub /oferta) | Weryfikacja nowego URL |
| `/oferta/zestaw-2-kapielowych-haftowanych-recznikow-w-koszu.html` | `/products/2-duze-reczniki-kosz` | Weryfikacja nowego URL |
| `/oferta/2-duze-reczniki-ze-szlafrokami.html` | `/products/szlafrok-2-reczniki` | Weryfikacja nowego URL |
| `/oferta/szlafrok-2-reczniki.html` | `/products/szlafrok-2-reczniki` | Weryfikacja nowego URL |
| `/oferta/szlafrok-z-haftem.html` | `/products/szlafrok-z-haftem` | Weryfikacja nowego URL |
| `/oferta/duzy-recznik-z-haftem.html` | `/products/duzy-recznik` | Weryfikacja nowego URL |
| `/oferta/zestawy-ze-szlafrokami.html` | `/products?kategoria=szlafroki` | Weryfikacja nowego URL |
| `/oferta.html` | `/products` | Stara strona oferty |
| `/nasze-realizacje.html` | `/realizacje` lub `/` | Weryfikacja nowego URL |
| `/nasze-realizacje-6.html` | `/realizacje` | Strona 6 → główna realizacje |
| `/kontakt.html` | `/kontakt` | Zmiana rozszerzenia |
| `/czcionki.html` | `/kreator` lub `/wizzard` | Czcionki → do kreatora |
| `/wzory-haftow.html` | `/wizzard` | Wzory → kreator |
| `/wzory-haftow-na-rocznice-slubu.html` | `/wizzard?okazja=rocznica` | Jeśli kreator obsługuje okazje |
| `/koszyk.html` | `/koszyk` | Zmiana rozszerzenia |
| `/regulamin.html` | `/regulamin` | Zmiana rozszerzenia |

## Uwagi techniczne

1. **Duplikat www/non-www**: GSC widzi dwie wersje strony głównej (`www.` i bez `www.`). Upewnić się, że canonical i redirect 301 www→non-www (lub odwrotnie) są skonfigurowane spójnie.
2. **Obraz indeksowany**: `/pictures/900x/546f2a3d28dfc_4-reczniki-prezent-na-mikol.jpg` — dodać `X-Robots-Tag: noindex` lub `<meta name="robots" content="noindex">` dla plików graficznych.
3. **Blog URLs**: `/blog/haft_na_recznikach/9` ma 230 wyświetleń i 1 kliknięcie — zachować lub przekierować na nowy URL bloga.

## Weryfikacja po wdrożeniu

- [ ] Sprawdzić wszystkie przekierowania w GSC (Coverage → Excluded → Redirects)
- [ ] Sitemap po przebudowie: 69 URL-i → sprawdzić czy żaden wartościowy URL nie zniknął
- [ ] Pozycja "ręczniki haftowane" (7.6) — monitorować co tydzień przez 4 tygodnie po rebuildzie
