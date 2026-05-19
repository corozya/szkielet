# gsc-mcp — instalacja

**Typ:** MCP | **Opis:** Google Search Console — dane ruchu, błędy indeksowania, Core Web Vitals

**Pliki:**
- `scripts/run-gsc-mcp.sh`

**MCP entry:**
```json
{ "command": "bash", "args": ["scripts/run-gsc-mcp.sh"], "cwd": "." }
```

**Setup:** brak dodatkowego — wymaga autoryzacji Google OAuth przy pierwszym uruchomieniu

**Wymagane dane (zbierz od użytkownika przed setup):**
| Zmienna | Opis | Przykład |
|---------|------|---------|
| `GSC_SITE_URL` | URL właściwości w GSC (z `sc-domain:` lub `https://`) | `sc-domain:example.com` |
| `GOOGLE_CLIENT_ID` | Client ID z Google Cloud Console | `123....apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | Client Secret z Google Cloud Console | `GOCSPX-...` |

Zapisz do `.env.gsc`. Autoryzacja OAuth uruchomi się przy pierwszym starcie serwera.
