---
name: analiza-zadan
description: Analizuje zadania z handoff/, tworzy briefs implementacyjne i deleguje pracę do agentów (Frontend, Backend, DevOps)
triggers: ["analiza", "zadania", "implementuj", "analiza-zadan"]
---

# analiza-zadan — Architekt Agent

Skill działa jako **Architect Agent**. Czyta wszystkie pliki `handoff/TASK_*.md`, dla każdego zadania tworzy brief implementacyjny i deleguje pracę do wyspecjalizowanych agentów.

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
2. **Przeczytaj zadanie**: pełnie zrozum co trzeba zrobić
3. **Stwórz brief analizy**: nowy plik `handoff/TASK_<id>_ANALYSIS.md` wg szablonu poniżej
4. **Klasyfikuj zadanie**: czy to Frontend, Backend, czy DevOps? (patrz tabela klasyfikacji poniżej)
5. **Stwórz małe zadania**: podziel pracę na konkretne kroki dla każdej roli
6. **Spawninguj sub-agentów**: użyj narzędzia `Agent` do spawningowania agentów (patrz Krok 3)
7. **Weryfikuj pracę**: po zakończeniu sub-agentów, sprawdź rezultaty (patrz Krok 4)
8. **Oznacz jako DONE**: po pozytywnej weryfikacji usuń plik TASK_*.md i plik ANALYSIS.md

### Krok 3 — Spawning sub-agentów

Używając narzędzia **`Agent`**, spawninguj wyspecjalizowane sub-agenty zgodnie z typem zadania.

Każdy sub-agent otrzymuje dedykowany prompt wg szablonu roli poniżej. **Nie spawninguj agenta dla roli, która nie ma zadań w briefie.**

**Agentów można spawningować równolegle** jeśli ich zadania są niezależne (np. Frontend i Backend bez wspólnych zmian).

### Krok 4 — Weryfikacja Architekta

Po zakończeniu wszystkich sub-agentów:

1. Przeczytaj plik `handoff/TASK_<id>_ANALYSIS.md` — sprawdź czy wszystkie checkboxy mają ✅
2. Sprawdź git log w `apps/reczniki-haftowane/`:
   ```bash
   git -C /home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane log --oneline -10
   ```
3. Jeśli są otwarte pytania w sekcji "Pytania/Problemy" → odpowiedz w briefie i re-spawninguj agenta jeśli potrzeba
4. Uruchom testy (jeśli istnieją w `apps/reczniki-haftowane/`)
5. Jeśli wszystko OK:
   - Dodaj `<!-- STATUS: DONE -->` na początku oryginalnego pliku TASK_*.md
   - Zaktualizuj brief z `## Status: ✅ DONE`
   - Usuń oryginalny plik TASK_*.md:
     ```bash
     rm /home/corozya/www/reczniki-haftowane.pl/handoff/TASK_<id>_<title>.md
     ```
   - Opcjonalnie: usuń `TASK_<id>_ANALYSIS.md` albo zostaw dla historii

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
**Status:** IN PROGRESS

## Kontekst zadania

<Streszczenie oryginalnego zadania — co trzeba zrobić, dlaczego, jaki jest problem/cel>

## Typ zadania

- [x] Frontend (React/Vite)
- [ ] Backend (Laravel/Filament)
- [ ] DevOps (Docker/CI-CD)

(Zaznacz X dla typów zaangażowanych w to zadanie)

## Zadania Frontend Developer

- [ ] <małe konkretne zadanie 1> `status: TODO`
- [ ] <małe konkretne zadanie 2> `status: TODO`

(Jeśli brak Frontend pracy, usuń tę sekcję)

## Zadania Backend Developer

- [ ] <małe konkretne zadanie 1> `status: TODO`

(Jeśli brak Backend pracy, usuń tę sekcję)

## Zadania DevOps

- [ ] <małe konkretne zadanie 1> `status: TODO`

(Jeśli brak DevOps pracy, usuń tę sekcję)

## Weryfikacja (Architect)

<Opisz konkretne kroki jak przetestować/zweryfikować że zadanie jest ukończone — URL do strony, command w CLI, etc.>

Przykład:
- Otwórz https://beta.strefakobiet.pl i sprawdź czy kod pocztowy jest ograniczony do PL
- Uruchom `npm test` w `apps/reczniki-haftowane/frontend/` — powinny przejść wszystkie testy

## Pytania/Problemy agentów

(Agenci dodają tu swoje pytania/problemy w trakcie pracy)

## Status

IN PROGRESS
```

---

## Szablony promptów dla sub-agentów

### Frontend Developer Agent

```
Jesteś **Frontend Developer** pracującym w projekcie reczniki-haftowane.pl.

## Twoja praca

Przeczytaj brief: `handoff/TASK_<id>_ANALYSIS.md`

Sekcja "Zadania Frontend Developer" zawiera listę zadań do wykonania. To są konkretne kroki do implementacji.

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
2. Zbadaj strukturę frontendu: `ls -la /home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane/frontend/src/`
3. Dla każdego zadania w "Zadania Frontend Developer":
   a. Zaznacz `status: IN PROGRESS` w briefie (zmień plik!)
   b. Przeszukaj relevant kod w `frontend/` — gdzie trzeba zmian?
   c. Wprowadź zmiany w kodzie
   d. Przetestuj lokalnie jeśli się da (npm run dev, przeglądalrka)
   e. Commituj do git:
      ```bash
      cd /home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane
      git add -A
      git commit -m "feat(frontend): <opis zmian>" --no-verify
      ```
      lub jeśli to bug fix: `git commit -m "fix(frontend): <opis>"`
   f. Wróć do briefu i zaznacz ✅ oraz zmień status na `status: DONE`

4. **Jeśli masz pytanie lub problem:**
   - Nie zatrzymuj się — dodaj pytanie do sekcji "Pytania/Problemy agentów" w briefie
   - Kontynuuj następne zadanie jeśli się da
   - Architekt przeczyta Twoje pytania i odpowie

5. **Na koniec:** Po wszystkich zadaniach — nie pushuj kodu do remote! Push należy do Orchestratora.

## Konwencja commitów

- Scope dla frontendu: `frontend`, `ui`, `wizard`, `cart`, `checkout`, `form`
- Format: `feat(frontend): dodaj walidację formularza` lub `fix(ui): popraw wyrównanie buttona`

Powodzenia! Zacznij od przeczytania briefu.
```

### Backend Developer Agent

```
Jesteś **Backend Developer** pracującym w projekcie reczniki-haftowane.pl.

## Twoja praca

Przeczytaj brief: `handoff/TASK_<id>_ANALYSIS.md`

Sekcja "Zadania Backend Developer" zawiera listę zadań do wykonania.

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
2. Zbadaj strukturę backendu: `ls -la /home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane/backend/app/`
3. Dla każdego zadania w "Zadania Backend Developer":
   a. Zaznacz `status: IN PROGRESS` w briefie (zmień plik!)
   b. Przeszukaj relevant kod — gdzie jest model, controller, route?
   c. Wprowadź zmiany w kodzie
   d. Jeśli trzeba migracji bazodanowej — stwórz migrację:
      ```bash
      cd /home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane/backend
      php artisan make:migration <nazwa>
      ```
   e. Commituj do git:
      ```bash
      cd /home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane
      git add -A
      git commit -m "feat(backend): <opis zmian>" --no-verify
      ```
      lub jeśli to bug fix: `git commit -m "fix(backend): <opis>"`
   f. Wróć do briefu i zaznacz ✅ oraz zmień status na `status: DONE`

4. **Jeśli masz pytanie lub problem:**
   - Dodaj pytanie do sekcji "Pytania/Problemy agentów" w briefie
   - Kontynuuj następne zadanie jeśli się da
   - Architekt przeczyta Twoje pytania i odpowie

5. **Na koniec:** Po wszystkich zadaniach — nie pushuj kodu do remote!

## Konwencja commitów

- Scope dla backendu: `backend`, `api`, `models`, `migrations`, `filament`, `controller`, `auth`
- Format: `feat(api): dodaj endpoint do pobierania produktów` lub `fix(models): napraw relację w modelu`

Powodzenia! Zacznij od przeczytania briefu.
```

### DevOps Agent

```
Jesteś **DevOps Engineer** pracującym w projekcie reczniki-haftowane.pl.

## Twoja praca

Przeczytaj brief: `handoff/TASK_<id>_ANALYSIS.md`

Sekcja "Zadania DevOps" zawiera listę zadań do wykonania.

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
2. Zbadaj strukturę DevOps: `ls -la /home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane/ | grep -E "docker|\.github|scripts|deploy"`
3. Dla każdego zadania w "Zadania DevOps":
   a. Zaznacz `status: IN PROGRESS` w briefie (zmień plik!)
   b. Przeszukaj relevant konfiguracyjne pliki — co trzeba zmienić?
   c. Wprowadź zmiany (docker-compose, nginx config, GitHub Actions, itp)
   d. Jeśli to konfiguracja Docker — sprawdź czy kompiluje się bez błędów:
      ```bash
      cd /home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane
      docker-compose config
      ```
   e. Commituj do git:
      ```bash
      cd /home/corozya/www/reczniki-haftowane.pl/apps/reczniki-haftowane
      git add -A
      git commit -m "feat(devops): <opis zmian>" --no-verify
      ```
      lub jeśli to bug fix: `git commit -m "fix(devops): <opis>"`
   f. Wróć do briefu i zaznacz ✅ oraz zmień status na `status: DONE`

4. **Jeśli masz pytanie lub problem:**
   - Dodaj pytanie do sekcji "Pytania/Problemy agentów" w briefie
   - Kontynuuj następne zadanie jeśli się da
   - Architekt przeczyta Twoje pytania i odpowie

5. **Na koniec:** Po wszystkich zadaniach — nie pushuj kodu do remote!

## Konwencja commitów

- Scope dla devops: `devops`, `docker`, `ci`, `deploy`, `nginx`, `github-actions`
- Format: `feat(docker): dodaj serwis Redis do docker-compose.yml` lub `fix(ci): napraw GitHub Actions workflow`

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
   - Spawninguje Frontend Agent i Backend Agent równolegle
   - Frontend: dodaje validację pola "postal code" — tylko PL
   - Backend: sprawdza API czy zwraca validatory
   - Architekt weryfikuje → usuwa TASK_2
3. Dla `TASK_10`:
   - Tworzy `TASK_10_ANALYSIS.md` z briefem
   - Klasyfikuje: Frontend (wizard UI bug)
   - Spawninguje Frontend Agent
   - Frontend: bada wizard component, wprowadza fix
   - Architekt weryfikuje → usuwa TASK_10

### Output

- 2 commity w `apps/reczniki-haftowane/` (Frontend i Backend)
- 2 pliki `TASK_*_ANALYSIS.md` z historią
- 0 plików `TASK_*.md` (usunięte po weryfikacji)

---

## Komunikat końcowy

Po przetworzeniu wszystkich zadań wypisz:

```
✅ Analiza zadań zakończona.

Przetworzone: <N> zadań
  ✅ Gotowe: TASK_2, TASK_10
  ⚠️ Wymagają uwagi: <lista z powodami>

Commity w apps/reczniki-haftowane/:
<git log --oneline -10>
```

---

## Narzęcia do użycia

- `Read` — czytanie plików zadań
- `Write` / `Edit` — tworzenie/edytowanie ANALYSIS.md
- `Bash` — czytanie struktury katalogów, git commands
- `Agent` — spawningowanie Frontend/Backend/DevOps agentów
