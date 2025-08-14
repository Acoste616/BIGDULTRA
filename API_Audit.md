# API_Audit (Initial)

## Co zrobiono
- Przejrzałem `backend/main_refactored.py` pod kątem endpointów i modeli.
- Zweryfikowałem walidację wejścia w `models/schemas.py`.

## Wyniki
- Endpointy: `/`, `/health`, `/sessions/create`, `/analyze`, `/strategy/generate`, `/data/*` (comprehensive, subsidies, tco, charging-infrastructure), `/feedback/submit`, `/suggestions/create`, `/stats/dashboard`, `/sparring/*`, `/learning/extract`, `WS /ws/{session_id}`.
- Walidacja: Pydantic modele request/response obecne i sensowne limity (np. `input_text` min/max). Brak globalnego handlera błędów/formatu błędów.
- Brak wersjonowania API w ścieżce (tylko `API_VERSION` w config), brak rate limiting per klient.

## Problemy
- Część endpointów `GET /data/*` nie ma paginacji/filtrów → ryzyko dużych odpowiedzi.
- Brak spójnego schematu błędów (tylko modele `ErrorResponse`, `ValidationErrorResponse` nie są stosowane globalnie).
- Brak testów jednostkowych endpointów.

## Rekomendacje
- Wprowadzić `APIRouter` z prefiksem `/api/v1` i tagami; dodać globalny exception handler zwracający ustrukturyzowane błędy.
- Dodać limity i paginację w listujących endpointach (`limit`, `offset`, walidacja zakresów).
- Włączyć rate limiting (np. slowapi) z rozsądnymi domyślnymi progami.
- Zdefiniować jawne kontrakty OpenAPI (response_model dla wszystkich endpointów, kody błędów).

## Następne kroki
- PR: refaktor routerów i dodanie handlerów błędów + paginacja dla `/data/*`.
- Dodać testy dla `/sessions/create`, `/analyze`, `/strategy/generate`, `/feedback/submit`.