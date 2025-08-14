# Observability (Initial)

## Co zrobiono
- Przejrzano `config.py` (LOG_LEVEL/FORMAT). Brak strukturalnych logów, metryk i tracingu.

## Plan
- Logi: strukturalne JSON (uvicorn + app), korelacja `session_id`, poziomy (INFO/ERROR), sanitizacja PII.
- Metryki: FastAPI middleware (latency, RPS, errors), licznik wywołań `/analyze`, cache hit rate, Supabase query time.
- Tracing: OpenTelemetry (HTTP in/out, Supabase calls, AI calls), exporter OTLP.
- Alerty: SLO 99% 2xx dla `/analyze`, p95 latency < 800ms (bez AI) i < 4s (z AI), błąd AI > 5% w 5 min — alert.
- Dashboardy: latency p50/p95/p99, error rate per endpoint, Supabase slow queries, AI success vs fallback.

## Następne kroki
- Włączyć `structlog`/`logging` JSON + middleware metryk (prometheus_client) + OTel.
- Eksporter Prometheus i basic Grafana dashboardy (JSON).