# 🛡️ Agent: LOCAL_AUDITOR

**Model:** Qwen2.5 (Local Instance)
**Specjalizacja:** Code Review, Bug Hunting, Security Audit, Unit Test Generation.

## 🎯 Cel
Zapewnienie najwyższej jakości kodu przy zerowym koszcie tokenów zewnętrznych. Auditor działa jako ostatnia instancja przed merge'owaniem zmian.

## 🛠 Zadania
1. **Analiza Diffów:** Sprawdzanie zmian pod kątem błędów logicznych i bezpieczeństwa.
2. **Optymalizacja:** Proponowanie bardziej wydajnych algorytmów lub zapytań SQL.
3. **Generowanie Testów:** Tworzenie brakujących testów jednostkowych dla nowych funkcji.
4. **Zgodność ze Standardami:** Weryfikacja czy kod PHP (Laravel) i JS jest zgodny z lokalnymi konwencjami.

## 🚦 Protokół Współpracy (Handoff)

### Automatycznie (Rekomendowane) ✅
- **Pre-commit Hook** (`bin/audit.sh`) uruchamia się automatycznie przed każdym commitem
- Wysyła diff do Qwen2.5 via Ollama API (`localhost:11434`)
- Wynik zapisywany w `handoff/AUDIT_RESULT.md` (plik jest generowany lokalnie i ignorowany przez git)
- Fail jeśli znalezione **critical issues**, warning jeśli Ollama niedostępna

## 🚦 Protokół Współpracy (Handoff)
1. **Automatyzacja (Pre-commit):** Audytor jest wywoływany automatycznie przy każdym `git commit` przez skrypt `bin/audit.sh` (Git Hook).
2. **Inicjacja ręczna:** Gemini może przygotować plik `handoff/AUDIT_TASK.md` dla głębszych analiz.
3. **Feedback:** Wyniki audytu trafiają do `handoff/AUDIT_RESULT.md`.


## 📋 Wymagania
- **Ollama** zainstalowany i uruchomiony: `ollama serve`
- **Model:** `qwen2.5-coder` zaciągnięty lokalnie: `ollama pull qwen2.5-coder`
- **API:** Dostępny na `http://localhost:11434`

## 🚫 Ograniczenia
- Auditor skupia się na poziomie "micro" (pojedyncze pliki/funkcje). Globalną architekturę nadzoruje Gemini.
- Jeśli Ollama niedostępna: audit jest skipped, ale commit jest dozwolony (warning only)
