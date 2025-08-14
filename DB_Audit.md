# DB_Audit (Initial)

## Co zrobiono
- Pobrałem realne metryki tabel (`scripts/check_supabase_data.py`).
- Przejrzałem migrację `database/migrations/004_expert_tables.sql` (tabele eksperckie + indeksy).

## Wyniki
- 30 tabel, 20 z danymi, łącznie 390 rekordów.
- Indeksy obecne m.in.: `ev_subsidies_poland(valid_from, valid_until)`, `charging_infrastructure_pl(location_city, tesla_compatible)`, `winter_performance_data(model_name)`, `tco_calculation_templates(customer_segment)`.
- Brak widocznych FK między tabelami mapującymi (np. `objection_archetypes`), brak migracji up/down.
- RLS/policies nieobecne w migracjach.

## Problemy
- Brak kluczy obcych dla tabel asocjacyjnych → ryzyko spójności.
- Brak indeksów pod często filtrowane pola w API (np. `products_competitors.brand`, `products_tesla.model_name`).
- Brak paginacji po stronie DB w zapytaniach – ryzyko pełnych skanów.
- Brak strategii migracji (rollback, lock safety).

## Rekomendacje
- Dodać FK dla: `objection_archetypes(objection_id→objections.id, archetype_id→archetypes.id)` oraz innych asocjacji.
- Dodać indeksy: `products_competitors(brand, model_name)`, `products_tesla(model_name)`, `playbooks(target_archetype_id, target_objection_id)`.
- Dodać migracje up/down (idempotentne) + transakcyjność.
- Wprowadzić RLS i policies na tabelach dynamicznych (session/logs/feedback/etc.).

## Następne kroki
- Zaprojektować pełny zestaw migracji (DDL + rollback) z bezpieczeństwem (lock timeout, batchowanie).
- Dodać testy integracyjne walidujące spójność (FK/NOT NULL/unikaty) i wydajność (EXPLAIN plan dla krytycznych zapytań).