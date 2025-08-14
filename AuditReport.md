# AuditReport (Initial)

## Co zrobiono
- Inwentaryzacja repo (`backend`, `frontend`, `database`, `scripts`).
- Weryfikacja konfiguracji i sekretów (OLLAMA/Supabase). Usunięto twardo zakodowane klucze z uruchomienia.
- Uruchomienie testu AI (`backend/test_quick_reply.py`) z podanym hostem i kluczem OLLAMA.
- Zrzut danych z Supabase (`scripts/check_supabase_data.py`) i zapis do `database/supabase_data_report.json`.

## Wyniki
- Backend: FastAPI + `ExpertOllamaClient`, `ExtendedDatabaseService` (31 tabel). Test AI przeszedł z realnym połączeniem do OLLAMA.
- Baza: 30 tabel widocznych, 20 zawiera dane (łącznie 390 rekordów). Krytyczne tabele (archetypes/objections/playbooks/products_tesla) wypełnione.
- Frontend: statyczny HTML (`ultra-bigdecoder.html`).
- CI: brak workflowów w repo.

## Ryzyka i luki (P0/P1)
- P0: Sekrety były w kodzie (usunięte z uruchamiania, nadal w historii). Brak polityki rotacji kluczy.
- P0: Brak formalnych migracji dla wszystkich 31 tabel (mamy `004_expert_tables.sql` + dane). Brak rollbacków.
- P1: Brak RLS/Polic w migracjach; rely na service_role. Ryzyko bezpieczeństwa w środowiskach współdzielonych.
- P1: Brak testów jednostkowych dla krytycznych endpointów; tylko skrypty/integ.
- P1: Brak CI/CD i skanów bezpieczeństwa.
- P2: Frontend bez bundlera/testów e2e; brak a11y/i18n.

## Rekomendacje
- P0: Sekrety wyłącznie z ENV/secret manager; usunąć domyślne API KEY z repo, dodać `.env.example` z placeholderami.
- P0: Dodać migracje idempotentne (up/down) dla wszystkich tabel + indeksy; plan rollbacku.
- P1: Dodać RLS/Policies i testy uprawnień (least privilege) + role i grants.
- P1: Wprowadzić walidację wejść (Pydantic/Zod) spójnie na API i w modelach.
- P1: Uruchomić CI (lint, testy, skany SCA, SBOM); dodać minimalne testy krytyczne (auth/session/analyze/strategy).
- P2: Wydzielić schematy DTO (OpenAPI), wprowadzić paginację i rate limiting per IP/user.

## Następne kroki
- Przygotować `RemediationPlan.md` z P0/P1/P2 i estymatami.
- Dodać minimalny PR: walidacja wejścia i krytyczne indeksy + .env.example.
- Przygotować `DB_Audit.md`, `API_Audit.md`, `Observability.md`, `Tests_Plan.md`.