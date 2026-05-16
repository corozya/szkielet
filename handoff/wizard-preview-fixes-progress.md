# Stan prac: Wizard preview fixes (sesja 2026-05-16)

## Status

**WSTRZYMANE — czekamy na zakończenie `handoff/TASK_frontend_wizard_lazy_catalog_fetch.md`**

Po zakończeniu tamtego zadania wrócimy tutaj i dokończymy otwarte kwestie (sekcja poniżej).

---

## Co zostało zrobione

### 1. `enrichDrawingWithTemplate` utility
**Plik:** `src/lib/wizzard/enrichDrawingTemplate.js`

Cross-referencja wzoru z płaskiej listy `/drawings` z `drawingsGrouped` w celu dodania brakującego `template` (zawiera `canvas_width`, `canvas_height`, `slots`). Bez tego SVG renderuje się ze złym viewBoxem.

### 2. Kreator — wzbogacanie przy wyborze wzoru
**Plik:** `src/components/wizzard/WizzardControlPanel.jsx`

`enrichDrawingWithTemplate` wywoływane przy `onSelectDrawing` — wzór w store jest zawsze wzbogacony. To "source of truth".

### 3. Kreator — podgląd po stronie preview
**Plik:** `src/components/wizzard/EmbroideryWizardPreview.jsx`

Fallback enrichment w `resolvedDrawing` useMemo — obsługuje stare dane z localStorage które nie miały template.

### 4. Intro strony produktu
**Pliki:** `src/components/personalization/PersonalizationFlow.jsx`, `PersonalizationIntro.jsx`

`drawingsGrouped` propagowane przez `PersonalizationFlow` → `PersonalizationIntro` → `slotPreviews` useMemo. Duże miniaturki konfigurowanych slotów renderują poprawnie.

### 5. SetVisualization — self-fetching `drawings-grouped`
**Plik:** `src/components/shared/SetVisualization.jsx`

- Dodany `useQuery(['drawings-grouped'])` wewnątrz komponentu (React Query deduplikuje — zero podwójnych requestów jeśli wizard już pobrał)
- `enrichDrawingWithTemplate` wywoływane w `renderTile`
- `getDrawingCanvasSize` dodane do resolve drawing — `_canvas_width`/`_canvas_height` teraz poprawne

### 6. Snapshot koszyka — `drawing_template`
**Plik:** `src/lib/wizzard/wizardConfigSchema.js`

`buildCartConfigSnapshot` teraz zapisuje `drawing_template: sc?.drawing?.template ?? null` w każdym slocie. Dzięki temu `SetVisualization` ma dane do poprawnego renderowania bez czekania na `drawings-grouped` fetch — eliminuje flash "duża pszczoła → pszczoła + tekst" po odświeżeniu strony.

W `SetVisualization.renderTile` używane priorytetowo przed `drawingsGrouped`:
```js
const drawingForEnrich = rawDrawing && sc?.drawing_template && !rawDrawing.template
  ? { ...rawDrawing, template: sc.drawing_template }
  : rawDrawing
```

### 7. Wygląd kreatora — portretowy kontener
**Plik:** `src/components/personalization/PersonalizationStepSlot.jsx`

- Lewy panel: tło-blur z `cacheUrl('media/tlo.png')`, pełna szerokość
- Wewnętrzny kontener: `aspect-[2/3]` z `ring-4 ring-white/60 shadow-2xl rounded-2xl`
- Nakładka haftu: `w-[75%] aspect-[3/4]`
- `showSlotFrames` default: `false` (brak ramek dookoła slotów)

### 8. Naprawione bugi renderowania SVG
**Plik:** `src/lib/wizzard/wizzardClientSvg.js`

- `buildClientSvgFromLayout`: early return null gdy brak slots (zamiast pustego SVG blokującego fallback do direct mode)
- `contentSquareViewBox`: null fallback na CANVAS_W/CANVAS_H
- `buildClientSvgDirect`: używa własnego viewBox SVG gdy brak canvas size i brak slotów

---

## Co pozostało / otwarte kwestie

### Flash w koszyku (stare pozycje)
`drawing_template` jest zapisywane tylko dla NOWYCH pozycji koszyka. Stare pozycje bez `drawing_template` nadal mają flash przy pierwszym załadowaniu. Po implementacji `TASK_frontend_wizard_lazy_catalog_fetch.md` ten problem powinien zniknąć przez wcześniejszy prefetch `drawings-grouped`.

### Miniaturka koszyka — bee poza widocznym obszarem
Wzór "osa" (pszczoła + tekst) w małej miniaturce koszyka (~80px) pokazuje tekst ale pszczoła może wypadać poza widoczny obszar przy overlay size `h-[100%] w-[82%]`. W kreatorze (duży panel) wszystko widoczne. Do zbadania po zakończeniu lazy catalog fetch.

### `drawingsGrouped` niedostępne dla checkout
`CheckoutPage` może mieć podobny flash — do zbadania po zakończeniu lazy catalog fetch.

---

## Powiązane zadania

- `handoff/TASK_frontend_wizard_lazy_catalog_fetch.md` — **BLOKUJE powrót do tego zadania**
- Plan w `~/.claude/plans/` — ogólny plan refaktoru `EmbroiderySlotPreview` (odłożony, częściowo zrealizowany)
