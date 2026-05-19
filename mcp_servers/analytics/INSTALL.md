# analytics-mcp — instalacja

**Typ:** MCP | **Opis:** Google Analytics 4 — raporty, konwersje, zdarzenia, lejki

**Pliki:**
- `scripts/run-google-analytics-mcp.sh`

**MCP entry:**
```json
{ "command": "bash", "args": ["scripts/run-google-analytics-mcp.sh"], "cwd": "." }
```

**Setup:** brak dodatkowego — wymaga autoryzacji Google OAuth przy pierwszym uruchomieniu

**Wymagane dane (zbierz od użytkownika przed setup):**
| Zmienna | Opis | Przykład |
|---------|------|---------|
| `GA4_PROPERTY_ID` | ID właściwości GA4 (bez `properties/`) | `123456789` |
| `GOOGLE_CLIENT_ID` | Client ID z Google Cloud Console | `123....apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | Client Secret z Google Cloud Console | `GOCSPX-...` |

Zapisz do `.env.analytics`. Autoryzacja OAuth uruchomi się przy pierwszym starcie serwera.
