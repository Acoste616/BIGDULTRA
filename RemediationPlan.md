# RemediationPlan (Initial)

## P0 (Security/Reliability)
- Secrets hygiene: usuń domyślne klucze z repo; `.env.example` + README kroki (S, high impact)
- Rotacja kluczy Supabase/OLLAMA po audycie (S, high impact)
- Migracje up/down dla 31 tabel; brakujące indeksy; plan rollbacku (M, high impact)

## P1 (Platform/Quality)
- RLS/Policies dla tabel dynamicznych; role/grants least-privilege (M, high impact)
- Walidacja wejść na API (Pydantic modele request/response) (S, medium impact)
- CI/CD: lint, tests, SCA, SBOM; artefakty (M, high impact)
- Testy krytyczne: sessions/analyze/strategy/ws (M, high impact)

## P2 (UX/Perf)
- Paginacja/listy, limity odpowiedzi, rate limiting (S)
- Frontend: bundler/testy e2e/a11y, i18n (M)
- Observability: strukturalne logi, metryki, trace + dashboardy (M)

## Proponowany pierwszy PR
- Dodanie `.env.example`, sanitization kluczy, walidacja wejść dla `/analyze`, indeksy kluczowe (S, low risk, high gain).