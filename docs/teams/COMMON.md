# 🤝 Wspólne Standardy Agentów i Zespół

## 👥 Zespół Ekspertów (Role)

| Agent | Plik Roli | Kompetencje |
|-------|-----------|------------|
| **Architekt** | `docs/teams/ARCHITECTURE.md` | Projektowanie wysokopoziomowe, planowanie, logika systemowa. |
| **Product Strategist** | `docs/teams/PRODUCT_STRATEGIST.md` | Wizja produktu, Roadmapa, Discovery. |
| **SaaS Architect** | `docs/teams/SAAS_ARCHITECT.md` | Backend PHP (Laravel), Multi-tenancy, Auth. |
| **Extension Expert** | `docs/teams/EXTENSION_EXPERT.md` | Wtyczki Browser, Logi sieciowe, UI Injection. |
| **Integration Guru** | `docs/teams/INTEGRATION_GURU.md` | API ClickUp, Jira, Kanboard, Adaptery. |
| **UX Developer** | `docs/teams/UX_DEVELOPER.md` | Dashboard React, Panel Klienta. |

*Uwaga: Nowi agenci są dodawani do tej tabeli dopiero po zatwierdzeniu przez użytkownika w procesie wywiadu.*

---

## 📡 Protokół Komunikacji (Handoff)
1. **Orkiestrator (Gemini)** analizuje zadanie -> przeprowadza wywiad z użytkownikiem o potrzebnych agentach i ich **skillach**.
2. **Orkiestrator** tworzy brief w `handoff/TASK_ID.md` albo w katalogu `handoff/TASK_ID/brief.md` oraz pliki ról w `docs/teams/`.
3. **Specjaliści** czytają swój Plik Roli + brief zadania, niezależnie od tego, czy jest plikiem czy katalogiem.
4. **Specjaliści** wykonują pracę.
5. **Specjaliści** aktualizują brief zadania (Status -> Zakończone, Notatki techniczne).
6. **Orkiestrator** weryfikuje i zamyka zadanie.

## ✅ Definition of Done (DoD) dla Agentów
Zadanie uznaje się za zakończone TYLKO gdy:
1. **Kod:** Jest przetestowany, zgodny ze standardami i udokumentowany wewnątrz plików.
2. **🛡️ Lokalny Audyt (Audit-before-Commit):** Przeprowadzono audyt bezpieczeństwa i jakości za pomocą lokalnego LLM (np. Qwen2.5-Coder via Ollama). Raport zapisano w `handoff/LAST_AUDIT.md`.
3. **Git:** Zmiany są scommitowane z poprawnym prefiksem PO uzyskaniu pozytywnego wyniku audytu.
4. **Zadania (Handoff):** Brief zadania został zaktualizowany (Status: **Zakończone**).
5. **Roadmapa:** Odpowiedni punkt w `docs/ROADMAP.md` został oznaczony jako wykonany.
6. **Weryfikacja:** Agent uruchomił testy i potwierdził brak regresji.

---

## 🏛 Standardy Operacyjne

### 📍 Źródło Prawdy
1. **Codebase:** Główne źródło prawdy o stanie aplikacji.
2. **Dokumentacja (`docs/teams/`):** Źródło prawdy dla **zasad, architektury i ról**.

### 📦 Zarządzanie Repozytorium (Git)
- **Commits:** Każdy Agent Ekspert odpowiada za commitowanie własnych zmian.
  - *Format:* `feat(scope): krótki opis` lub `fix(scope): krótki opis`.
- **Finalizacja i Push:** Główny Agent (Gemini) lub Agent DevOps odpowiada za finalny push po weryfikacji zadania.
- **Nigdy nie pushuj bezpośrednio na Production:** Wszystkie zmiany muszą najpierw przejść przez środowisko `beta` (patrz `DEVOPS.md`).

---

## ⚡ Mandat Wydajności Tokenowej (KRYTYCZNE)
- **Priorytet Modeli:** ZAWSZE preferuj szybsze i tańsze modele (np. `gemini-1.5-flash`) do rutynowych zadań i dokumentacji. Używaj większych modeli (`pro`) TYLKO do złożonych decyzji architektonicznych.
- **`rtk` Proxy:** Używaj `rtk gain` dla statystyk. Obowiązkowe dla wszystkich komend shell.
- **Minimalistyczna Komunikacja:** 
  - Pomiń zbędne uprzejmości i długie podsumowania.
  - Używaj diffów i chirurgicznych odczytów zamiast pełnej treści plików.
- **Grep przed Read:** Nigdy nie czytaj całego pliku, aby znaleźć jedną rzecz.
