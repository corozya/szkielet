# Audyt kreatora haftu (wizard)

**Data:** 2026-05-16  
**Zakres:** przegląd znanej architektury, backlogu z `handoff/`, analityki oraz możliwości pobrania danych przez MCP (w tym Microsoft Clarity).

---

## 1. Cel dokumentu

- Zebrać **jedno miejsce** z opisem kreatora z perspektywy orchestratora repo (`reczniki-haftowane.pl`).
- Wskazać **źródła dowodów** (Clarity, GA4, kod aplikacji — po podłączeniu `apps/`).
- Odpowiedzieć jasno: **czy mamy MCP Clarity i jak go uruchomić**, oraz **co jest dostępne w tej chwili w Cursorze**.

Pełny audyt behawioralny (heatmaps, nagrania sesji, lejek krok po kroku) wymaga **danych z panelu Clarity / GA4** lub dostępu do aplikacji pod `/wizard` (lub legacy `/wizzard`). Ten plik jest **szkieletem audytu + checklistą**; liczby i wnioski uzupełnia się po pobraniu raportów.

---

## 2. Produkt i ścieżki URL

Z dokumentacji marketingowej i handoffów:

| Obszar | Uwagi |
|--------|--------|
| Kreator (SPA) | Trasy typu `/wizard/:slug`; historycznie `/wizzard` (redirecty — patrz handoff `TASK_wizard_preset_links_from_realizations.md`). |
| Preset z realizacji | `/wizard/r/:hash` → dekodowanie → redirect z parametrami (`WizardPresetPage`). |
| Publiczny share | `/share/r/:hash`. |

Mapowanie starych URL-i z planu SEO: `docs/redirects_plan_301.md`, `docs/occasions_plan.md`.

---

## 3. Architektura techniczna (znana z repo)

Kod aplikacji (**frontend / backend Laravel**) żyje w podprojektach pod `apps/reczniki-haftowane/` — w samym orchestratorze często **nie ma** checkoutu `apps/`. Poniższe ścieżki pochodzą z istniejących handoffów.

### Backend (API)

- `GET /api/v1/wizzard/options` — opcje kreatora, lista `drawings` (m.in. relacja `template.slots`).
- `GET /api/v1/wizzard/drawing/{drawing}` — pojedynczy wzór.
- `GET/PUT /api/v1/slot-template/{type}` — szablony slotów (edytor admin / desktop).
- Settings kreatora: m.in. `wizard_default_config` (jedno źródło po refaktorze — `TASK_frontend_wizard_settings_single_source.md`).

### Frontend (warstwa „wizzard”)

| Obszar | Pliki (referencyjnie) |
|--------|------------------------|
| SVG podglądu | `frontend/src/lib/wizzard/wizzardClientSvg.js` |
| Sloty tekstowe z szablonu | `frontend/src/lib/wizzard/resolveDrawingTextSlots.js` |
| Podgląd | `frontend/src/components/wizzard/EmbroideryWizardPreview.jsx`, `EmbroideryPreviewStage`, `WizzardClientPreview` |
| Szablony SVG statyczne | `frontend/public/wizzard-templates/*.svg` |
| Inicjalizacja / preset URL | `frontend/src/hooks/useWizardInitialization.js`, `WizardPresetPage.jsx`, `src/lib/wizardRoutes.js` |

### Model danych (kierunek docelowy)

Szczegóły migracji: `handoff/TASK_drawing_templates_source_of_truth.md` (`drawing_templates`, `drawing_template_slots`, `drawings.template_id`, `svg_code` jako grafika).

---

## 4. Znane ryzyka i tematy z backlogu (handoff)

| Temat | Źródło |
|-------|--------|
| Pozycja haftu / viewBox / `drawing_position` | `handoff/slot-template-editor-i-kreator.md`, `fix-template-position-canvas-size.md` |
| DOMPurify + szkielety SVG | `handoff/fix-skeleton-svg-dompurify-id.md` |
| Przycinanie liter (czcionka A1) | `handoff/TASK_font_a1_ascender_clipping_fix.md` |
| Mobile UX (scroll, sticky tabs, wyszukiwarka wzorów) | `handoff/UX-mobile-kreator-optymalizacja.md` |
| Numery wzorów (`drawing.id` na karcie) | `handoff/TASK_wizard_pattern_catalog_numbers.md` |

Te punkty warto **łączyć z nagraniami Clarity** (gdzie użytkownicy się cofają, rage clicks, porzucenia na konkretnym kroku).

---

## 5. Analityka — co jest zaplanowane / opisane

### Microsoft Clarity

Z planu Ads / trackingu (`marketing/google-ads/campaign-plan-small-budget.md`, `marketing/MARKETING_PLAN.md`):

- Tagi sesji kreatora m.in.: **`Wizard_Step`**, **`Wizard_Product`**, **`Wizard_Current_Towel`** — pod analizę wąskich gardeł (np. zestawy 7 i 8).
- Status w planie: Clarity **aktywne**; **weryfikacja tagów w panelu** była oznaczona jako do dokończenia.

### GA4

- Lejek wysokopoziomowy: `view_item` → `purchase` (ten sam dokument kampanii).

---

## 6. MCP — czy mamy Clarity i skąd brać dane?

### 6.1. Co jest w repozytorium (gotowość pod MCP Clarity)

| Element | Stan |
|---------|------|
| Wrapper uruchomieniowy | **`scripts/run-clarity-mcp.sh`** — ładuje `.env`, wymaga **`MS_CLARITY`**, uruchamia **`npx -y @microsoft/clarity-mcp-server --clarity_api_token=…`** (bez globalnej instalacji). |
| Konfiguracja Cursor | Wpis **`clarity`** w **`.cursor/mcp.json`** → powyższy skrypt. |

**Wniosek:** MCP Clarity jest **podłączony w repo** po ustawieniu **`MS_CLARITY`** i restarcie MCP w Cursorze.

### 6.2. Narzędzia MCP (oficjalny serwer Microsoft)

Z [README `clarity-mcp-server`](https://github.com/microsoft/clarity-mcp-server):

| Narzędzie | Zastosowanie |
|-----------|----------------|
| **`query-analytics-dashboard`** | Metryki pulpitu (ruch, scroll, engagement, segmentacja) — pytania naturalnym językiem. |
| **`list-session-recordings`** | Lista nagrań z filtrami (URL, urządzenie, przeglądarka itd.) — np. ścieżki `/wizard`. |
| **`query-documentation-resources`** | Fragmenty dokumentacji Clarity. |

Limity **Data Export API** (to samo źródło danych): m.in. **10 żądań / projekt / dobę**, dane za **1–3** dni — patrz [Clarity Data Export API](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api).

### 6.3. Jak uruchomić lokalnie

1. **Settings → Data Export** w projekcie Clarity → token API → zapisz jako **`MS_CLARITY`** w root `.env`.
2. **Cursor:** ustawienia MCP — serwer **clarity** powinien startować z **`scripts/run-clarity-mcp.sh`** (wymaga Node + `npx`).
3. Po dodaniu/zmianie `.env` — **restart serwerów MCP** lub Cursora.

Inni hosty (Claude / Codex / Gemini): wpis jak w **`.cursor/mcp.json.example`** / `.codex/config.toml` / `.gemini/settings.json`.

### 6.4. Alternatywy jeśli MCP Clarity nie działa

- **Panel webowy Clarity** — ręczny audyt nagrań i dashboardów (filtrowanie po custom tags `Wizard_*`).
- **MCP Google Analytics** (`analytics` w `.cursor/mcp.json`) — eventy / lejek **jeśli** GA4 ma skonfigurowane odpowiednie zdarzenia dla kreatora (nie zastępuje heatmap Clarity).
- **Playwright MCP** — scenariusze E2E i regression UX po wdrożeniu zmian.

---

## 7. Checklist audytu kreatora (do wypełnienia)

### Dane zewnętrzne

- [ ] Clarity: nagrania sesji z tagami `Wizard_Step` / `Wizard_Product` / `Wizard_Current_Towel` — najczęstsze porzucenia i powtarzalne błędy kliknięć.
- [ ] Clarity: scroll depth / dead clicks na krokach z zestawami 7 i 8 (priorytet biznesowy z planu Ads).
- [ ] GA4: ścieżka do zakupu vs wejścia z `/wizard` / produktów — segmentacja ruchu.
- [ ] Porównanie desktop vs mobile (osobno — zgodnie z `UX-mobile-kreator-optymalizacja.md`).

### Kod i funkcjonalnie (w repo aplikacji)

- [ ] Mapa kroków kreatora vs instrumentacja (`Wizard_*` — kompletność i poprawność wartości).
- [ ] Zgodność podglądu SVG z szablonami (`wizzardClientSvg`, `resolveDrawingTextSlots`).
- [ ] Flow presetów: `/wizard/r/:hash`, parametr `?p=`.

### Wynik

- [ ] Lista hipotez UX + priorytety (impact / effort).
- [ ] Propozycje zadań w `handoff/` lub Kanboard.

---

## 8. Powiązane pliki w tym repo

- `scripts/run-clarity-mcp.sh`
- `.cursor/mcp.json`, `.cursor/mcp.json.example`
- `docs/teams/AI_HOSTS_AND_MCP.md` — ogólny zestaw MCP (GA, nie wymienia Clarity w tabeli „rekomendowany zestaw”; Clarity jest osobnym skryptem).
- `handoff/` — szczegóły techniczne i taski wymienione w §3–4.
- `marketing/google-ads/campaign-plan-small-budget.md` — tagi Clarity i KPI.
