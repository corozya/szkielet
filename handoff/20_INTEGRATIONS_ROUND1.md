# 20_INTEGRATIONS_ROUND1

**Status:** W trakcie (Runda 1: Gotowa ✅, Runda 2: Do zrobienia ⏳)
**Priorytet:** Wysoki

Implementacja kolejnych adapterów integracji.

---

## Runda 1 — Szybkie wygrane

### MS Teams (`teams`)
- `app/Services/Destinations/TeamsAdapter.php`
- Format: Incoming Webhook → `{ "text": "..." }` lub Adaptive Card
- `configSchema`: `webhook_url`
- Testowanie lokalnie: Webhook Tester :8081

### Telegram (`telegram`)
- `app/Services/Destinations/TelegramAdapter.php`
- Wysyłka przez Bot API: `POST https://api.telegram.org/bot{TOKEN}/sendMessage`
- `configSchema`: `bot_token`, `chat_id`
- `testConnection`: wywołanie `getMe`
- Testowanie: prawdziwy bot testowy lub ngrok

### ClickUp (`clickup`)
- `app/Services/Destinations/ClickUpAdapter.php`
- REST API: `POST https://api.clickup.com/api/v2/list/{list_id}/task`
- `configSchema`: `api_token` (per-client), `list_id` (per-project jako container)
- `listContainers()`: pobierz spaces → folders → lists
- Testowanie: Webhook Tester :8081

### GitLab (`gitlab`)
- `app/Services/Destinations/GitLabAdapter.php`
- REST Issues API: `POST /projects/{id}/issues` — identyczne z GitHubAdapter
- `configSchema`: `base_url` (domyślnie gitlab.com), `token`, `project_id`
- Testowanie lokalnie: Gitea :3000 (GitHub-compatible — wystarczy do mockowania)

---

## Runda 2 — Killer feature

### AI Triage Agent (`ai_triage`)
- `app/Services/AiTriageService.php` (nie adapter — osobny serwis)
- Wywołanie Claude API (`claude-sonnet-4-6`) po zapisie feedbacku
- Zadania agenta:
  - Ocena severity (low/medium/high/critical)
  - Wyciąganie kroków reprodukcji z opisu
  - Wykrywanie duplikatów (porównanie z ostatnimi N zgłoszeniami)
  - Auto-kategoryzacja type: bug/ux/suggestion
  - Krótkie summary dla PM (non-tech)
- Dispatch jako osobny Job: `RunAiTriage` (nie blokuje zapisu feedbacku)
- Wyniki zapisywane w nowym polu `ai_analysis` (json) na `feedback_reports`
- Wyświetlenie w `Feedback/Show.jsx`

**Wymagania:**
- Migracja: dodanie kolumny `ai_analysis` (json, nullable) do `feedback_reports`
- `.env`: `ANTHROPIC_API_KEY=`
- Composer: `composer require anthropic-php/client` lub użyj Http facade z bearer tokenem

---

## DoD

### Runda 1
- [ ] `TeamsAdapter` zarejestrowany i wysyłający Adaptive Card
- [ ] `TelegramAdapter` zarejestrowany, `testConnection` działa
- [ ] `ClickUpAdapter` zarejestrowany, `listContainers` zwraca listy
- [ ] `GitLabAdapter` zarejestrowany, reużywa logiki GitHubAdapter

### Runda 2
- [ ] `AiTriageService` wywołuje Claude API po każdym nowym feedbacku (async Job)
- [ ] Wyniki widoczne w `Feedback/Show.jsx`
- [ ] Możliwość ponownego uruchomienia analizy ręcznie z widoku
