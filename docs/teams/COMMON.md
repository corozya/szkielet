# 🤝 Wspólne Standardy Agentów i Zespół

## 👥 Zespół Ekspertów (Role)

| Agent | Plik Roli | Kompetencje |
|-------|-----------|------------|
| **Architekt** | `docs/teams/ARCHITECTURE.md` | Projektowanie wysokopoziomowe, planowanie, logika systemowa. |

*Uwaga: Nowi agenci są dodawani do tej tabeli dopiero po zatwierdzeniu przez użytkownika w procesie wywiadu.*

---

## 📡 Protokół Komunikacji (Handoff)
1. **Orkiestrator (Gemini)** analizuje zadanie -> przeprowadza wywiad z użytkownikiem o potrzebnych agentach i ich **skillach**.
2. **Orkiestrator** tworzy brief w `handoff/TASK_ID.md` oraz pliki ról w `docs/teams/`.
3. **Specjaliści** czytają swój Plik Roli + `handoff/TASK_ID.md`.
4. **Specjaliści** wykonują pracę -> Aktualizują status w `handoff/`.
5. **Orkiestrator** weryfikuje i zamyka zadanie.

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
