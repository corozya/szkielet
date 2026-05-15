# Raport z Audytu Wydajności (PageSpeed Insights)
**Data:** 2026-05-14
**URL:** http://reczniki-haftowane.pl

## 1. Podsumowanie Wyników

| Kategoria | Mobile | Desktop |
| :--- | :---: | :---: |
| **Wydajność** | **64** | **76** |
| **Ułatwienia dostępu** | 92 | 92 |
| **Sprawdzone metody** | 100 | 100 |
| **SEO** | 92 | 92 |

---

## 2. Szczegółowe Metryki (Mobile)

*   **First Contentful Paint (FCP):** 3,0 s
*   **Largest Contentful Paint (LCP):** **8,6 s** (Krytyczny)
*   **Total Blocking Time (TBT):** 220 ms
*   **Speed Index (SI):** 3,9 s
*   **Cumulative Layout Shift (CLS):** 0,003 (Bardzo dobry)

---

## 3. Główne Problemy i Wnioski

### Wydajność
1.  **Bardzo wysoki LCP (8,6 s):** Główny element treści wczytuje się zdecydowanie zbyt długo. Prawdopodobnie duży obraz w sekcji Hero lub opóźnione renderowanie kluczowych elementów przez JS.
2.  **Zasoby blokujące renderowanie:** Szacowany zysk **~730 ms** po eliminacji blokujących plików CSS i JS.
3.  **Optymalizacja obrazów:**
    *   Potrzebne przejście na formaty WebP/AVIF.
    *   Możliwa redukcja wagi o ok. **280 KiB**.
4.  **Nieużywany JavaScript:** Ok. **180 KiB** kodu JS ładowane jest bez potrzeby przy pierwszej odsłonie.

### SEO
1.  **Błąd w robots.txt:** PageSpeed raportuje 1 błąd. Analiza wykazała, że plik zawiera niestandardowe dyrektywy Cloudflare (`Content-Signal`), które mogą być źle interpretowane przez walidatory.

### Ułatwienia dostępu (Accessibility)
1.  **Kontrast:** Niewystarczający kontrast kolorów tła i tekstu w niektórych sekcjach.
2.  **Rozróżnialność linków:** Linki powinny być odróżnialne od tekstu nie tylko za pomocą koloru (np. przez podkreślenie).

---

## 4. Planowane Poprawy (Zadanie: TASK_performance_pagespeed_optimization_benchmark)
*   Analiza i optymalizacja LCP (priorytet).
*   Wdrożenie nowoczesnych formatów obrazów.
*   Naprawa błędów w `robots.txt`.
*   Korekta kontrastów i stylu linków.

---
*Po wdrożeniu poprawek zostanie wykonany test porównawczy.*
