# Tests_Plan (Initial)

## Cel
Minimalny zestaw testów krytycznych dla ścieżek e2e i regresji.

## Zakres
- Backend API: `/sessions/create`, `/analyze`, `/strategy/generate`, `/feedback/submit`, WS `/ws/{session_id}`.
- DB: integralność FK, indeksy na krytycznych kolumnach, EXPLAIN dla zapytań.
- AI: deterministyczne formaty JSON, walidacja schema, fallback path.

## Scenariusze (priorytet)
- P0: happy path e2e: create session → analyze → strategy → feedback (200/JSON schema OK).
- P0: `/analyze` walidacja input_text (min/max, puste). 
- P1: `/data/*` paginacja/limity.
- P1: WS: nawiązanie, komunikat analyze i odpowiedź.
- P2: Retry/backoff przy błędach AI (symulacja timeoutu).

## Coverage cel
- 80%+ dla warstw domenowych; krytyczne ścieżki e2e pokryte w 100%.

## Następne kroki
- Dodać folder `backend/tests` i szkielety testów pytest.