# Task: [REFactor] Jedno zrodlo settingsow kreatora

## Context
`wizardSettingsQueryOptions` jest używane w 4 miejscach: dwukrotnie w `useProductPageLogic` (raz w `useProductQueries` gdzie wynik jest ignorowany, raz bezpośrednio gdzie wynik jest używany), raz w `WizardLoader` (wynik ignorowany — de facto prefetch), raz w `WizardContext` (wynik używany).

**Ważne zastrzeżenie:** React Query deduplikuje te wywołania do jednego żądania sieciowego (ten sam query key), więc nie ma problemu z wydajnością ani duplikatami requestów do API. Problem jest architektoniczny — zduplikowane subskrypcje do tego samego cache'a i rozmyte miejsce odpowiedzialności za `wizard_default_config` i `drawing_slot_templates`.

## Expected Outcome
Ustawienia kreatora sa pobierane raz na sciezke i przekazywane dalej bez duplikowania hookow oraz bez niepotrzebnych odswiezen.

## Frontend Tasks
- [x] Usunac zbedne wywolania `useQuery(wizardSettingsQueryOptions)` z `useProductPageLogic` i `WizardPage`, zostawiajac jedno zrodlo prawdy.
- [x] Przekazac `wizardDefaultConfig` / `drawingSlotTemplates` przez propsy lub kontekst tam, gdzie sa potrzebne.
- [x] Dodac test lub smoke check, ktory potwierdza, ze otwarcie kreatora z poziomu produktu nie odpala znowu tych samych zapytan.

## Status: ZAKOŃCZONE ✅
- `useProductPageLogic` pobiera ustawienia i zwraca je do `ProductPage`.
- `ProductPage` przekazuje ustawienia do `WizardLoader` (overlay).
- `WizardPage` (standalone) pobiera ustawienia i przekazuje do swojego `WizardLoader`.
- `WizardProvider` (w `WizardContext.jsx`) przyjmuje dane przez propsy i nie wykonuje własnego `useQuery`.
- Zweryfikowano poprawność renderowania i testów.

## Validation
- Kreator i strona produktu nadal dostaja te same settingsy.
- Otwarcie `/wizard/:slug` z produktu nie powiela zbednych odczytow settingsow.

## Questions/Issues for Architect
- Brak.
