# TASK: Naprawa obcinania ascenderów w czcionce a1.ttf

> ⚠️ **ADNOTACJA: To zadanie pochodzi z testu workflow handoff — nie jest zadaniem produkcyjnym.**

## Status
- **Priority:** Medium
- **Type:** Frontend / Wizard / Fonts
- **Created:** 2026-05-15
- **State:** Pending

## Problem
Czcionka 1 (`a1.ttf`) w kreatorze haftu obcina górne ozdobniki liter takich jak R, M, A.
Analiza metryki czcionki wykazała:

| Parametr | Wartość |
|---|---|
| unitsPerEm | 2048 |
| hhea.ascender | 1638 |
| OS/2.typoAscender | 1638 |
| OS/2.winAscent | 2108 |
| glyph R: yMax | **1691** ← ponad ascender! |
| glyph M: yMax | **1670** ← ponad ascender! |

Glify R i M wychodzą ponad zadeklarowany `hhea.ascender` (1691 > 1638), przez co przeglądarka obcina górne ozdobniki przy renderowaniu SVG text z `dominant-baseline: middle`.

## Rozwiązania (dwa podejścia)

### Opcja A — Poprawka w czcionce (rekomendowana)
Podwyższenie `hhea.ascender` i `OS/2.typoAscender` do wartości pokrywającej rzeczywisty yMax glifów:

```bash
python3 -c "
from fontTools import ttLib
import shutil
shutil.copy('a1.ttf', 'a1.ttf.bak')
font = ttLib.TTFont('a1.ttf')
font['hhea'].ascender = 1750
font['OS/2'].sTypoAscender = 1750
font.save('a1.ttf')
print('Zapisano. winAscent pozostaje bez zmian:', font['OS/2'].usWinAscent)
"
```

Plik do edycji: `backend/storage/app/public/fonts/a1.ttf`
(oraz kopia w `backend/storage/app/public/media/fonts/a1.ttf`)

### Opcja B — Poszerzenie clip-path w SVG (już wdrożona jako workaround)
Zmiana w `frontend/src/lib/wizzard/wizzardClientSvg.js` funkcja `applyClipPath`:
clip rect poszerzony o 25% góra / 15% dół slotu.
Wymaga przebudowania frontendu (`npm run build` po `sudo rm -rf frontend/dist/`).

## Requirements
- [ ] Wykonać Opcję A (poprawka w pliku TTF) dla `a1.ttf` w obu lokalizacjach
- [ ] Zweryfikować, że litery R, M, A nie są obcinane w podglądzie kreatora
- [ ] Opcjonalnie: sprawdzić pozostałe czcionki pod kątem podobnego problemu

## Verification
- [ ] Otworzyć kreator → wybrać Czcionkę 1 → wpisać "Magda & Radek" → górne elementy liter widoczne
- [ ] Sprawdzić na podglądzie mobilnym i desktopowym
