# Workflow Repository

- `kanboard_setup/` - Kanboard tooling
- `handoff/` - aktywne briefy
- `docs/teams/` - instrukcje agentów

Kod aplikacji jest w repozytorium produktu.

## Setup Kanboard (one-command)

1. Zainstaluj zależności (Node.js 18+):
   - `npm install` (w tym repo)
2. Skonfiguruj i przetestuj połączenie:
   - `npm run init-kb`

Skrypt zapisze konfigurację do `kanboard_setup/.env` i zweryfikuje API metodą `getVersion`.

## Start projektu (repo + Kanboard)

Jedna komenda do onboardingu projektu dla agentów:

- `npm run start-project`

Proces:
- pyta o URL repozytoriów (po jednym) i klonuje je do `apps/<repo>/` (gałąź `main`)
- dopisuje `apps/` do `.gitignore`, żeby nie commitować kodu aplikacji do “szkieletu”
- zawsze uruchamia `npm run init-kb` i dopytuje o konfigurację Kanboard

Regułka do wklejenia dla agentów:

> Uruchom `npm run start-project`. Skrypt podłączy repozytoria do `apps/` (pyta po jednym URL, zawsze `main`, nie nadpisuje istniejących katalogów), dopisze `apps/` do `.gitignore`, a potem zawsze uruchomi `npm run init-kb` i doprowadzi do poprawnej konfiguracji Kanboard.
