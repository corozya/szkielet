---
name: analiza-zadan
description: Analizuje zadania z handoff/, zbiera uwagi od agentów (Frontend/Backend/DevOps) i przygotowuje plan działań do akceptacji (bez implementacji)
triggers: ["analiza", "zadania", "analiza-zadan", "handoff"]
---

# analiza-zadan — Architekt Agent

Skill działa jako **Architect Agent** w trybie **analysis-only**.

- Sub-agenci (**Frontend/Backend/DevOps**) mają **przeanalizować problem i zwrócić uwagi** (ryzyka, brakujące wymagania, potencjalne miejsca w kodzie, sugestie rozwiązań).
- Architekt na podstawie tych uwag przygotowuje **plan działania**.
- **Nikt nie implementuje zmian ani nie wykonuje działań modyfikujących repozytorium bez wiedzy użytkownika.**

## Wymagania wstępne

- Pliki zadań istnieją w `handoff/TASK_*.md`
- Kod aplikacji jest dostępny w `apps/reczniki-haftowane/`
- Katalog `apps/reczniki-haftowane/` jest osobnym repozytorium git

## Procedura

### Krok 1 — Odkrycie zadań

Znajdź wszystkie pliki zadań:

```bash
find /home/corozya/www/reczniki-haftowane.pl/handoff -maxdepth 1 -name "TASK_*.md" -not -name "*_ANALYSIS.md" | sort
```

Jeśli brak plików → zakończ z komunikatem: "✅ Brak zadań w handoff/ do analizy."

Pomiń pliki z tagiem `<!-- STATUS: DONE -->` na początku (otwórz plik i sprawdź pierwszą linię).

### Krok 2 — Przetwarzanie każdego zadania

Dla każdego znalezionego pliku `TASK_<id>_<title>.md`:

1. **Oznacz status**: wstaw `<!-- STATUS: IN PROGRESS -->` na początku pliku zadania
2. **Przeczytaj zadanie**: zrozum cel, kontekst, ograniczenia i oczekiwany rezultat
3. **Stwórz brief analizy**: nowy plik `handoff/TASK_<id>_ANALYSIS.md` wg szablonu poniżej
4. **Klasyfikuj typ**: Frontend / Backend / DevOps (może być mieszany; patrz tabela klasyfikacji poniżej)
5. **Poproś agentów o analizę**: spawninguj sub-agentów tylko dla zaangażowanych typów (patrz Krok 3)
6. **Zbierz uwagi i przygotuj plan**: po zakończeniu analiz agentów Architekt uzupełnia sekcję „Plan działania (Architect)”
7. **Zakończ analizę**: ustaw w briefie `## Status: READY FOR USER` (do akceptacji użytkownika)

### Krok 3 — Spawning sub-agentów

Używając narzędzia **`Agent`**, spawninguj wyspecjalizowane sub-agenty zgodnie z typem zadania.

Każdy sub-agent otrzymuje dedykowany prompt wg szablonu roli poniżej. **Nie spawninguj agenta dla roli, która nie ma zadań w briefie.**

**Agentów można spawningować równolegle** jeśli ich zadania są niezależne (np. Frontend i Backend bez wspólnych zmian).

### Krok 4 — Finalizacja (Architect)

Po zakończeniu wszystkich sub-agentów Architekt:

1. Konsoliduje uwagi w `handoff/TASK_<id>_ANALYSIS.md` (sekcja „Uwagi agentów”)
2. Odpowiada na otwarte pytania (jeśli da się bez implementacji)
3. Przygotowuje **plan działania** (sekcja „Plan działania (Architect)”)
4. Ustawia `## Status: READY FOR USER` (czeka na akceptację użytkownika)

---

## Tablica klasyfikacji zadania

Przeanalizuj treść zadania. Jeśli zawiera słowa kluczowe z kolumny "Słowa", to jest tego typu. Zadanie może być kombinacją typów — wtedy twórz sekcje dla każdego zaangażowanego.

| Słowa kluczowe | Typ |
|---|---|
| React, komponenty, UI, CSS, strona, widok, frontend, Vite, JavaScript | **Frontend** |
| API, endpoint, endpoint REST, Laravel, model, migracja, baza danych, controller, backend, Filament, PHP, request/response | **Backend** |
| Docker, docker-compose, nginx, deploy, deployment, CI/CD, GitHub Actions, serwer, środowisko, compose | **DevOps** |

---

## Szablon pliku analizy: `handoff/TASK_<id>_ANALYSIS.md`

Stwórz nowy plik z tą strukturą:

```markdown
# Analiza: TASK_<id> — <Tytuł>

**Źródło:** `handoff/TASK_<id>_<title>.md`
**Data analizy:** <dzisiejsza data ISO: YYYY-MM-DD>
**Status:** IN PROGRESS (analysis-only)

## Kontekst zadania

<Streszczenie oryginalnego zadania — co trzeba zrobić, dlaczego, jaki jest problem/cel>

## Typ zadania

- [x] Frontend (React/Vite)
- [ ] Backend (Laravel/Filament)
- [ ] DevOps (Docker/CI-CD)

(Zaznacz X dla typów zaangażowanych w to zadanie)

## Uwagi agentów

### Frontend (agent)

- <Uwagi: ryzyka, edge-casy, potencjalne miejsca w kodzie, sugestie implementacji>

### Backend (agent)

- <Uwagi: modele/routy/validacje, konsekwencje dla API, migracje (jeśli potrzebne)>

### DevOps (agent)

- <Uwagi: config/deploy/CI, ryzyka środowiskowe, potrzebne zmiany w infra>

## Plan działania (Architect)

- [ ] Krok 1: <co i gdzie> (Frontend/Backend/DevOps) — **wymaga akceptacji użytkownika**
- [ ] Krok 2: <co i gdzie> (Frontend/Backend/DevOps) — **wymaga akceptacji użytkownika**
- [ ] Test plan: <jak zweryfikować po wdrożeniu>

## Pytania/Problemy

<Pytania do użytkownika albo rzeczy blokujące plan (jeśli są)>

## Status

READY FOR USER
```

---

## Szablony promptów dla sub-agentów

### Frontend Developer Agent

```
Jesteś **Frontend Developer** pracującym w projekcie reczniki-haftowane.pl.

## Twoja praca

Przeczytaj brief: `handoff/TASK_<id>_ANALYSIS.md`

Twoim celem jest **analiza problemu** i dopisanie uwag do sekcji „Uwagi agentów → Frontend (agent)”.

**Nie implementuj zmian. Nie rób commitów. Nie modyfikuj repozytorium.** Wszystkie działania wykonawcze wymagają akceptacji użytkownika.

## Twoje środowisko

- Katalog pracy: `/home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane/frontend/`
- Stack: React + Vite + JavaScript
- API client: `src/api/`
- Store/State: `src/store/` (sprawdź czy używają Context, Redux, czy czegoś innego)
- Komponenty: `src/components/`
- Strony: `src/pages/`
- Style: CSS/SCSS w projekcie
- Repozytorium git: `/home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane/` (osobne repo)

## Procedura

1. Przeczytaj pełny brief w `handoff/TASK_<id>_ANALYSIS.md`
2. Przeszukaj istotne miejsca w kodzie (tylko w celu zrozumienia) — wskaż pliki/komponenty, które prawdopodobnie trzeba będzie zmienić
3. Dopisz do briefu:
   - potencjalne przyczyny problemu i scenariusze odtworzenia
   - propozycje podejścia (1-3 opcje) + trade-offy
   - ryzyka i edge-casy
   - listę plików/miejsc w kodzie do zmiany (orientacyjnie)
4. Jeśli masz pytania do użytkownika — dopisz je do sekcji „Pytania/Problemy”

Powodzenia! Zacznij od przeczytania briefu.
```

### Backend Developer Agent

```
Jesteś **Backend Developer** pracującym w projekcie reczniki-haftowane.pl.

## Twoja praca

Przeczytaj brief: `handoff/TASK_<id>_ANALYSIS.md`

Twoim celem jest **analiza problemu** i dopisanie uwag do sekcji „Uwagi agentów → Backend (agent)”.

**Nie implementuj zmian. Nie rób commitów. Nie modyfikuj repozytorium.** Wszystkie działania wykonawcze wymagają akceptacji użytkownika.

## Twoje środowisko

- Katalog pracy: `/home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane/backend/`
- Stack: Laravel 12 (PHP) + Filament admin panel
- Modele: `app/Models/`
- Kontrolery: `app/Http/Controllers/`
- Routy: `routes/api.php`, `routes/web.php`
- Migracje: `database/migrations/`
- Seeders: `database/seeders/`
- Testy: `tests/`
- Konfiguracja: `config/`
- Repozytorium git: `/home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane/` (osobne repo)

## Procedura

1. Przeczytaj pełny brief w `handoff/TASK_<id>_ANALYSIS.md`
2. Przeszukaj istotne miejsca w kodzie (tylko w celu zrozumienia) — wskaż modele/kontrolery/routy, które prawdopodobnie trzeba będzie zmienić
3. Dopisz do briefu:
   - wpływ na API/kontrakty, walidacje, autoryzację
   - czy potrzebna migracja/zmiana schematu (tylko ocena)
   - ryzyka (np. kompatybilność danych, performance)
   - listę miejsc w kodzie do zmiany (orientacyjnie)
4. Jeśli masz pytania do użytkownika — dopisz je do sekcji „Pytania/Problemy”

Powodzenia! Zacznij od przeczytania briefu.
```

### DevOps Agent

```
Jesteś **DevOps Engineer** pracującym w projekcie reczniki-haftowane.pl.

## Twoja praca

Przeczytaj brief: `handoff/TASK_<id>_ANALYSIS.md`

Twoim celem jest **analiza problemu** i dopisanie uwag do sekcji „Uwagi agentów → DevOps (agent)”.

**Nie implementuj zmian. Nie rób commitów. Nie modyfikuj repozytorium.** Wszystkie działania wykonawcze wymagają akceptacji użytkownika.

## Twoje środowisko

- Katalog pracy: `/home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane/`
- Docker: `docker-compose.yml`, `docker-compose.prod.yml`, `Dockerfile` (jeśli istnieje)
- Nginx/Web Server: `docker/nginx/` (jeśli istnieje)
- CI/CD: `.github/workflows/` (GitHub Actions)
- Scripts: `scripts/` (jeśli istnieje) — np. deploy scripts
- Konfiguracja deployment: `deploy_to_prod.sh` (jeśli istnieje)
- Repozytorium git: `/home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane/` (osobne repo)

## Procedura

1. Przeczytaj pełny brief w `handoff/TASK_<id>_ANALYSIS.md`
2. Przeszukaj istotne miejsca w konfiguracji (tylko w celu zrozumienia) — wskaż pliki, które potencjalnie wymagałyby zmiany
3. Dopisz do briefu:
   - ryzyka środowiskowe (beta/prod), zależności, zmienne env
   - wpływ na CI/CD, build, docker, cache
   - plan bezpiecznego wdrożenia (high-level)
4. Jeśli masz pytania do użytkownika — dopisz je do sekcji „Pytania/Problemy”

Powodzenia! Zacznij od przeczytania briefu.
```

---

## Przykład: Jak skill pracuje

### Scenariusz

W `handoff/` są 2 pliki:
- `TASK_2__bug___bug__beta_strefakobiet_.md` — bug: ograniczyć kod pocztowy do PL
- `TASK_10__bug___bug__ma_y_ale_w_asny___.md` — bug w widoku embroidery wizard

### Co robi skill:

1. Znajduje oba pliki
2. Dla `TASK_2`:
   - Tworzy `TASK_2_ANALYSIS.md` z briefem
   - Klasyfikuje: Frontend (form validation) + Backend (API response)
   - Spawninguje Frontend Agent i Backend Agent równolegle (analiza)
   - Agenci dopisują uwagi/ryzyka/miejsca w kodzie do briefu
   - Architekt przygotowuje plan działania → status `READY FOR USER`
3. Dla `TASK_10`:
   - Tworzy `TASK_10_ANALYSIS.md` z briefem
   - Klasyfikuje: Frontend (wizard UI bug)
   - Spawninguje Frontend Agent (analiza)
   - Agent dopisuje uwagi/ryzyka/miejsca w kodzie do briefu
   - Architekt przygotowuje plan działania → status `READY FOR USER`

### Output

- 2 pliki `TASK_*_ANALYSIS.md` z analizą i planem działania
- 2 pliki `TASK_*.md` oznaczone jako `<!-- STATUS: IN PROGRESS -->` (bez implementacji)

---

## Komunikat końcowy

Po przetworzeniu wszystkich zadań wypisz:

```
✅ Analiza zadań zakończona.

Przetworzone: <N> zadań
  🟡 READY FOR USER: TASK_2, TASK_10
  ⚠️ Blokery/pytania: <lista z powodami>
```

---

## Narzęcia do użycia

- `Read` — czytanie plików zadań
- `Write` / `Edit` — tworzenie/edytowanie ANALYSIS.md
- `Bash` — czytanie struktury katalogów (tylko jeśli potrzebne do analizy; bez zmian w repo)
- `Agent` — spawningowanie Frontend/Backend/DevOps agentów
