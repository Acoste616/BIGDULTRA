# Architecture (Initial)

## C4 – Context
- Użytkownik przeglądarkowy → Frontend (SPA HTML/JS) → Backend (FastAPI) → AI (Ollama gpt-oss:120b) oraz DB (Supabase Postgres).

## C4 – Container
- Frontend: prosta SPA serwowana przez `http.server`.
- Backend: FastAPI (`main_refactored.py`), serwisy: `ExpertOllamaClient`, `ExtendedDatabaseService`.
- DB: Supabase (31 tabel; 30 widocznych, 20 z danymi), brak RLS w migracjach.
- AI: Ollama client z `host` + `Authorization` header.

## C4 – Component (Backend)
- API Endpoints (sessions/analyze/strategy/data/feedback/ws)
- AI Client (`services/ai/expert_ollama_client.py`) – integracja chat JSON.
- DB Service (`services/database_extended.py`) – dostęp do tabel, aliasy/łączenia.
- Prompts (`prompts/`) – system prompt + analysis prompt.

## Diagram (propozycja)
[Frontend] → HTTP/WS → [FastAPI] → (AI) Ollama Chat
                               ↘→ (DB) Supabase (PostgREST)

## Decyzje architektoniczne
- JSON format wymuszony przy odpowiedzi AI (redukcja nieokreśloności).
- Cache TTL na poziomie AI analizy (300s).
- Service-role key do audytu (docelowo: RLS + role/grants per środowisko).

## Ryzyka
- Brak RLS i uprawnień – exposure danych.
- Brak paginacji – ryzyko dużych payloadów i N+1.
- Brak CI/CD i observability – mała widoczność regresji i awarii.