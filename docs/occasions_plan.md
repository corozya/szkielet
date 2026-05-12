# Plan Rozbudowy Nawigacji: Okazje (Occasions)
**Data:** 2026-05-12
**Zadanie:** TASK_22

## 1. Cel Biznesowy
Przejście z nawigacji produktowej (np. "Ręcznik 50x100") na nawigację intencyjną ("Prezent na Ślub"). Ułatwia to wybór klientowi i poprawia SEO na frazy o wysokiej kaloryczności.

## 2. Proponowana Struktura Menu

### Menu Główne (Desktop/Mobile)
- **OKAZJE (Dropdown)**
  - 💒 **Ślub** (`/prezent-na-slub`)
  - 💍 **Rocznica Ślubu** (`/prezent-na-rocznice`)
  - 🏠 **Nowy Dom / Parapetówka** (`/prezent-na-parapetowke`)
  - 🎂 **Urodziny / Imieniny** (`/prezent-na-urodziny`)
  - ❤️ **Walentynki** (`/prezent-na-walentynki`)
  - 🎄 **Święta** (`/prezent-na-swieta`)
- **KREATOR HAFTU** (`/wizzard`)
- **NASZE PRODUKTY (Dropdown)**
  - Zestawy w koszach
  - Ręczniki kąpielowe
  - Szlafroki z haftem
  - Poduszki (Nowość)

## 3. Mapowanie Landing Pages i SEO

| Okazja | Landing Page URL | Fraza kluczowa | Priorytet |
| :--- | :--- | :--- | :--- |
| **Ślub** | `/prezent-na-slub` | ręczniki na ślub z haftem | 🔴 Krytyczny (Poz 9.3) |
| **Rocznica** | `/prezent-na-rocznice` | ręczniki na rocznicę ślubu | 🔴 Krytyczny (Poz 7.1) |
| **Parapetówka** | `/prezent-na-parapetowke` | personalizowany prezent na parapetówkę | 🟠 Średni |
| **Urodziny** | `/prezent-na-urodziny` | ręcznik z dedykacją na urodziny | 🟠 Średni |
| **Walentynki** | `/prezent-na-walentynki` | ręcznik z haftem na walentynki | 🟡 Niski |

## 4. Przekierowania 301 (Integracja z TASK_21)

Poniższe URL-e zostaną przekierowane na nowe landingi "Okazji", aby przekazać "link juice":

- `wzory-haftów-na-rocznicę-ślubu.html` (Poz 7.1) → `/prezent-na-rocznice`
- `oferta/tort-z-2-haftowanych-recznikow.html` (Poz 7.7) → `/prezent-na-slub` (lub Zestaw w koszu)
- `wzory-haftów.html` (Poz 5.1) → `/wizzard` (Główny hub wzorów)
- `śmieszne-wzory-haftów.html` (Poz 6.3) → `/prezent-na-urodziny` (lub dedykowana sekcja)

## 5. Wymagania Funkcjonalne (UX)
1. **Dynamiczne Filtrowanie:** Po wejściu na `/prezent-na-slub`, lista produktów powinna automatycznie filtrować wzory haftu do kategorii "Ślub".
2. **Hero Section:** Każdy landing page powinien mieć nagłówek H1 z frazą kluczową i krótki opis (SEO text).
3. **Deep Linking do Kreatora:** Przycisk "Personalizuj" przy produkcie na stronie okazji powinien otwierać kreator z pre-definiowanym wzorem (np. obrączki).

## 6. Harmonogram Wdrożenia
1. [ ] Akceptacja struktury menu przez klienta.
2. [ ] Przygotowanie treści SEO dla 4 głównych landingów.
3. [ ] Wdrożenie techniczne (React Router / Backend routes).
4. [ ] Uruchomienie przekierowań 301.
5. [ ] Monitoring GSC przez 14 dni.
