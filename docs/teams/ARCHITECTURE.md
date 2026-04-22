# Architecture: WorksOnMine

## Komponenty

- `backend-api/` (Laravel 12 + Inertia React): API + dashboard admina + integracje docelowe
- `feedback-extension/` (Chrome MV3): zbiera debug pack (screenshot/console/network) i wysyła do API

## Model danych

### Multi-tenancy
- `Client` → posiada `User` (adminów) i `Project`
- Izolacja po `client_id` na poziomie middleware i kontrolerów

### Role użytkowników (tylko administratorzy)
- `superadmin` — zarządza klientami i zaproszeniami beta
- `admin` — zarządza projektami, linkami zaproszeniowymi, integracjami
- ~~`tester`~~ — **usunięty model**: testerzy nie mają kont w systemie

### Testerzy (bez kont)
- `Tester` — email + hashed API token (`wom_...`)
- `ProjectInviteLink` — shareable link z opcjami: domena, limit użyć, wygaśnięcie
- `project_tester` — pivot: który tester ma dostęp do którego projektu

Jeden tester (email) może być zaproszony do wielu projektów różnych firm — ma jeden token per instancja WorksOnMine.

### Feedback
- `FeedbackReport` — przechowuje dane od admina (`user_id`) LUB testera (`tester_id`)

## Przepływ: dołączenie testera

```
Admin → tworzy ProjectInviteLink → kopiuje URL → wysyła (Slack/email/cokolwiek)
Tester → otwiera /join/{token} → podaje email
       → backend tworzy/aktualizuje Tester, przypisuje do projektu
       → zwraca api_token (wom_...) → strona wstrzykuje do #extension-config
       → content.js zapisuje { testerToken, testerApiUrl } w chrome.storage.local
       → wtyczka skonfigurowana
```

## Przepływ: wysyłka feedbacku

```
Extension popup → getProjectForUrl(url)
  → próbuje testerToken: GET /api/v1/tester/check?url=
  → próbuje saasApiKey:  GET /api/v1/projects/check?url=
  → zwraca { project, _token, _url, _type }

Użytkownik klika "Wyślij" → callSaaSWith(project, endpoint, 'POST', payload)
  → _type='tester': POST /api/v1/tester/feedback
  → _type='admin':  POST /api/v1/feedback
```

## API — endpointy extension

| Endpoint | Auth | Opis |
|---|---|---|
| `GET /api/v1/tester/check` | `wom_...` token | Sprawdź URL dla testera |
| `POST /api/v1/tester/feedback` | `wom_...` token | Wyślij feedback jako tester |
| `GET /api/v1/projects/check` | Sanctum (admin) | Sprawdź URL dla admina |
| `POST /api/v1/feedback` | Sanctum (admin) | Wyślij feedback jako admin |

## Integracje docelowe (DestinationRegistry)

Po zapisaniu `FeedbackReport` system próbuje automatycznie przekazać do skonfigurowanego destination:
- **Kanboard** — tworzy kartę w wybranym projekcie/kolumnie
- **GitHub** — tworzy issue w wybranym repo

Konfiguracja per-projekt: `destination_type` + `destination_config` (JSON).

## Granice bezpieczeństwa

- Multi-tenancy po `client_id` (middleware `client_access`)
- Tester token: `hash('sha256', 'wom_...')` w bazie, plaintext tylko przy generowaniu
- Invite link: jednorazowy lub z limitem, opcjonalna domena emaila, można unieważnić
- Pliki: walidacja ścieżki przed serwowaniem z `storage/app/public`
- Signed routes dla jednorazowych linków admina (extension install)

## Dokumenty operacyjne

- Role i standardy: `docs/teams/COMMON.md`
- Jak pracować z zadaniami: `docs/teams/AGENT_GUIDE.md`
- Roadmap: `docs/ROADMAP.md`
