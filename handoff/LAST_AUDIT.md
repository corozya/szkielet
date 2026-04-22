# LAST_AUDIT

Data: 2026-04-18
Zakres: Tester invite links refactor

## Co zrobiono
- Usunięto model testera jako User z `client_id`
- Dodano `Tester` (email + hashed token `wom_...`) bez konta w systemie
- Dodano `ProjectInviteLink` (shareable link z opcjami: domena, limit, wygaśnięcie)
- Pivot `project_tester` zamiast `project_user` dla testerów
- Nowe API endpointy dla testerów: `GET/POST /api/v1/tester/*` (middleware `tester_token`)
- Strona `/join/{token}` (publiczna, bez logowania) — tester podaje email, wtyczka się konfiguruje
- Panel admin: `Projects/Invitations.jsx` — tworzenie/unieważnianie linków, lista testerów
- Extension: `api.js` obsługuje dwa typy tokenów, `content.js` rozróżnia `connectionType`

## Stan
- Migracje wgrane na RPi ✓
- Build frontendu ✓
- Extension pliki zaktualizowane ✓

## Uwagi
- `project_invite_links.testers` hasMany przez `ProjectTester` — usunąć tę relację z modelu,
  używać `ProjectInviteLink` bezpośrednio (patrz bug fix poniżej)
- Brak testów feature dla nowego flow (do dodania)
