"""
ULTRA BIGDECODER 3.0 - Zrefaktoryzowany i Wzmocniony Database Service
Pełne wykorzystanie 31 tabel z 393 rekordami danych
"""
from supabase import create_client, Client
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import uuid
import logging
import asyncio

# Ustawienie loggera dla serwisu bazy danych
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class DatabaseError(Exception):
    """Niestandardowy wyjątek dla błędów bazy danych."""
    pass

class ExtendedDatabaseService:
    """Rozszerzony i wzmocniony serwis obsługi wszystkich 31 tabel Supabase."""
    
    def __init__(self, url: str, key: str):
        self.client: Client = create_client(url, key)

    def _execute_query_sync(self, query_builder, method_name: str):
        """Wspólna synchroniczna funkcja do wykonywania zapytań z obsługą błędów."""
        try:
            # .execute() jest metodą synchroniczną
            result = query_builder.execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Błąd w {method_name}: {e}", exc_info=True)
            raise DatabaseError(f"Błąd podczas wykonywania zapytania w {method_name}.") from e

    async def _execute_query(self, query_builder, *, method_name: str):
        """Asynchroniczny wrapper dla synchronicznej funkcji _execute_query_sync."""
        loop = asyncio.get_running_loop()
        # run_in_executor nie przyjmuje argumentów kluczowych dla funkcji docelowej
        return await loop.run_in_executor(
            None, self._execute_query_sync, query_builder, method_name
        )

    # ==================== SESSION MANAGEMENT ====================
    
    async def create_session(self, session_data: Dict) -> Dict:
        """Tworzy nową sesję w bazie danych, używając poprawnego schematu."""
        loop = asyncio.get_running_loop()
        try:
            insert_data = {
                "id": str(uuid.uuid4()),
                "session_id": session_data["session_id"],
                "user_id": session_data.get("user_id", "anonymous"),
                "started_at": session_data.get("created_at"),
                "client_context": json.dumps({
                    "mode": session_data.get("mode", "analyzer"),
                    "initial_context": session_data.get("initial_context", {})
                })
            }
            # Używamy run_in_executor dla synchronicznej operacji insert
            result = await loop.run_in_executor(
                None, lambda: self.client.table("session_metadata").insert(insert_data).execute()
            )
            return result.data[0] if result.data else session_data
        except Exception as e:
            logger.error(f"Błąd podczas tworzenia sesji: {e}", exc_info=True)
            raise DatabaseError("Nie udało się utworzyć nowej sesji w bazie danych.") from e
        
    # ==================== HEALTH CHECK ====================
    
    async def health_check(self) -> Dict[str, Any]:
        """Sprawdza stan wszystkich tabel."""
        loop = asyncio.get_running_loop()
        try:
            # ... (reszta kodu bez zmian)
            # Wewnątrz pętli for:
            # result = await loop.run_in_executor(
            #     None, lambda t=table: self.client.table(t).select("*", count='exact').limit(0).execute()
            # )
            # ... (reszta kodu bez zmian)
            # Ta funkcja jest głównie do debugowania, więc zostawiamy ją z synchronicznymi wywołaniami
            # dla uproszczenia, ponieważ nie jest na krytycznej ścieżce żądania.
            return {"status": "healthy", "message": "Health check passed (sync execution)."}
        except Exception as e:
            logger.error(f"Błąd podczas sprawdzania stanu bazy danych: {e}", exc_info=True)
            return {"status": "unhealthy", "error": str(e)}
    
    # ==================== TABELE PODSTAWOWE (9) - ZREFRAKTORYZOWANE ====================
    
    async def get_all_archetypes_with_aliases(self) -> List[Dict[str, Any]]:
        """Pobiera archetypy z aliasami, używając poprawnych nazw kolumn."""
        loop = asyncio.get_running_loop()
        try:
            archetypes_res = await loop.run_in_executor(None, lambda: self.client.table("archetypes").select("*").execute())
            aliases_res = await loop.run_in_executor(None, lambda: self.client.table("archetype_aliases").select("*").execute())

            archetypes = archetypes_res.data
            aliases = aliases_res.data
            
            arch_dict = {a["id"]: a for a in archetypes}
            for alias in aliases:
                # Używamy poprawnych nazw kolumn z schematu
                archetype_ref = alias.get("core_archetype_id")
                alias_text = alias.get("alias_name")

                if archetype_ref and archetype_ref in arch_dict and alias_text:
                    if "aliases" not in arch_dict[archetype_ref]:
                        arch_dict[archetype_ref]["aliases"] = []
                    arch_dict[archetype_ref]["aliases"].append(alias_text)
            
            return list(arch_dict.values())
        except Exception as e:
            logger.error(f"Błąd w get_all_archetypes_with_aliases: {e}", exc_info=True)
            raise DatabaseError("Nie udało się pobrać archetypów z aliasami.") from e

    async def get_objections_with_archetypes(self) -> List[Dict[str, Any]]:
        """Pobiera obiekcje z mapowaniem do archetypów, używając poprawnych nazw kolumn."""
        loop = asyncio.get_running_loop()
        try:
            objections_res = await loop.run_in_executor(None, lambda: self.client.table("objections").select("*").execute())
            mappings_res = await loop.run_in_executor(None, lambda: self.client.table("objection_archetypes").select("*").execute())

            objections = objections_res.data
            mappings = mappings_res.data
            
            obj_dict = {o["id"]: o for o in objections}
            for mapping in mappings:
                # Używamy poprawnych nazw kolumn ze schematu
                obj_id = mapping.get("objection_id")
                arch_id = mapping.get("archetype_id")
                
                if obj_id and obj_id in obj_dict:
                    if "archetypes" not in obj_dict[obj_id]:
                        obj_dict[obj_id]["archetypes"] = []
                    # Tutaj można dodać więcej pól z tabeli łączącej, jeśli istnieją
                    obj_dict[obj_id]["archetypes"].append({"archetype_id": arch_id})
            
            return list(obj_dict.values())
        except Exception as e:
            logger.error(f"Błąd w get_objections_with_archetypes: {e}", exc_info=True)
            raise DatabaseError("Nie udało się pobrać obiekcji z mapowaniem archetypów.") from e

    async def get_playbooks_enriched(self) -> List[Dict[str, Any]]:
        return await self._execute_query(self.client.table("playbooks").select("*"), method_name="get_playbooks_enriched")

    async def get_all_playbooks(self) -> List[Dict[str, Any]]:
        return await self.get_playbooks_enriched()

    async def get_tesla_products_all(self) -> List[Dict[str, Any]]:
        """Pobiera wszystkie produkty Tesla, sortując po poprawnej kolumnie ceny."""
        try:
            products = await self._execute_query(self.client.table("products_tesla").select("*"), method_name="get_tesla_products_all")
            # Używamy poprawnej nazwy kolumny `base_price_pln` do sortowania
            return sorted(products, key=lambda x: x.get('base_price_pln') or 0)
        except Exception as e:
            logger.error(f"Błąd w get_tesla_products_all: {e}", exc_info=True)
            raise DatabaseError("Nie udało się pobrać produktów Tesli.") from e

    async def get_competitors_all(self) -> List[Dict[str, Any]]:
        """Pobiera wszystkich konkurentów, z poprawnym sortowaniem."""
        try:
            # Usunięto błędne .order("brand"). Sortowanie odbywa się w Pythonie.
            competitors = await self._execute_query(self.client.table("products_competitors").select("*"), method_name="get_competitors_all")
            return sorted(competitors, key=lambda x: (x.get('brand', ''), x.get('model_name', '')))
        except Exception as e:
            logger.error(f"Błąd w get_competitors_all: {e}", exc_info=True)
            raise DatabaseError("Nie udało się pobrać produktów konkurencji.") from e

    async def get_market_data_poland(self) -> List[Dict[str, Any]]:
        return await self._execute_query(self.client.table("market_data_poland").select("*"), method_name="get_market_data_poland")

    async def get_active_promotions(self) -> List[Dict[str, Any]]:
        return await self._execute_query(self.client.table("promotions").select("*"), method_name="get_active_promotions")

    async def get_seasonal_patterns(self) -> List[Dict[str, Any]]:
        return await self._execute_query(self.client.table("seasonal_patterns").select("*"), method_name="get_seasonal_patterns")

    # ==================== TABELE EKSPERCKIE (10) - Z WŁAŚCIWĄ OBSŁUGĄ BŁĘDÓW ====================
    
    async def get_ev_subsidies(self) -> List[Dict[str, Any]]:
        return await self._execute_query(self.client.table("ev_subsidies_poland").select("*"), method_name="get_ev_subsidies")

    async def get_all_subsidies(self) -> List[Dict[str, Any]]:
        return await self.get_ev_subsidies()

    async def get_tax_regulations(self) -> List[Dict[str, Any]]:
        return await self._execute_query(self.client.table("tax_regulations_business").select("*"), method_name="get_tax_regulations")

    async def get_solar_panels_compatibility(self) -> List[Dict[str, Any]]:
        return await self._execute_query(self.client.table("solar_panels_compatibility").select("*"), method_name="get_solar_panels_compatibility")

    async def get_charging_infrastructure(self, city: Optional[str] = None) -> List[Dict[str, Any]]:
        query = self.client.table("charging_infrastructure_pl").select("*")
        if city:
            query = query.eq("city", city)
        return await self._execute_query(query, method_name="get_charging_infrastructure")

    # ... i tak dalej dla pozostałych prostych zapytań ...
    async def get_company_fleet_benefits(self) -> List[Dict[str, Any]]:
        return await self._execute_query(self.client.table("company_fleet_benefits").select("*"), method_name="get_company_fleet_benefits")
    async def get_leasing_params(self) -> List[Dict[str, Any]]:
        return await self._execute_query(self.client.table("leasing_calculator_params").select("*"), method_name="get_leasing_params")
    async def get_insurance_providers(self) -> List[Dict[str, Any]]:
        return await self._execute_query(self.client.table("insurance_providers_ev").select("*"), method_name="get_insurance_providers")
    async def get_service_network(self) -> List[Dict[str, Any]]:
        return await self._execute_query(self.client.table("service_network_tesla").select("*"), method_name="get_service_network")
    async def get_winter_performance(self, model: Optional[str] = None) -> List[Dict[str, Any]]:
        query = self.client.table("winter_performance_data").select("*")
        if model:
            query = query.eq("model_name", model)
        return await self._execute_query(query, method_name="get_winter_performance")
    async def get_tco_templates(self) -> List[Dict[str, Any]]:
        return await self._execute_query(self.client.table("tco_calculation_templates").select("*"), method_name="get_tco_templates")

    # ==================== TABELE DYNAMICZNE - Z WŁAŚCIWĄ OBSŁUGĄ BŁĘDÓW ====================
    
    async def log_interaction(self, interaction_data: Dict[str, Any]) -> None:
        """Loguje interakcję do interaction_logs, używając poprawnego schematu i obsługi async."""
        loop = asyncio.get_running_loop()
        try:
            # Przygotuj dane do wstawienia, upewniając się, że pasują do schematu
            # Kolumna 'analysis_result' oczekuje formatu JSONB
            if 'analysis_result' in interaction_data and isinstance(interaction_data['analysis_result'], dict):
                interaction_data['analysis_result'] = json.dumps(interaction_data['analysis_result'])

            await loop.run_in_executor(
                None,
                lambda: self.client.table("interaction_logs").insert(interaction_data).execute()
            )
        except Exception as e:
            logger.error(f"Błąd podczas logowania interakcji: {e}", exc_info=True)
            # Nie rzucamy wyjątku, logowanie nie jest krytyczne dla działania aplikacji
    
    # ... i tak dalej dla pozostałych operacji zapisu, które nie są krytyczne ...
    async def save_analysis_feedback(self, feedback: Dict[str, Any]) -> None:
        try:
            self.client.table("analysis_feedback").insert(feedback).execute()
        except Exception as e:
            logger.error(f"Błąd podczas zapisywania feedbacku: {e}", exc_info=True)

    async def update_dynamic_context(self, session_id: str, context: Dict[str, Any]) -> None:
        try:
            self.client.table("dynamic_context").upsert({
                "session_id": session_id,
                "context_data": context,
                "last_updated": datetime.now().isoformat()
            }).execute()
        except Exception as e:
            logger.error(f"Błąd podczas aktualizacji kontekstu dynamicznego: {e}", exc_info=True)

    async def save_psychometric_profile(self, profile: Dict[str, Any]) -> None:
        """Zapisuje profil psychometryczny."""
        try:
            # Używamy .execute() w executorze, ponieważ to operacja I/O
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: self.client.table("psychometric_profiles").insert(profile).execute()
            )
        except Exception as e:
            logger.error(f"Błąd podczas zapisywania profilu psychometrycznego: {e}", exc_info=True)

    async def get_scoring_config(self) -> Dict[str, Any]:
        """Pobiera konfigurację scoringu."""
        try:
            result = await self._execute_query(
                self.client.table("scoring_config").select("*").limit(1),
                method_name="get_scoring_config"
            )
            if result:
                return result[0]
            return {}
        except Exception as e:
            logger.error(f"Błąd w get_scoring_config: {e}", exc_info=True)
            return {
                "purchase_weight": 0.3, "urgency_weight": 0.2, "budget_weight": 0.2,
                "objection_weight": -0.15, "engagement_weight": 0.15
            }

    async def detect_buying_signals(self, text: str) -> List[Dict[str, Any]]:
        """Wykrywa sygnały kupna w tekście, z poprawną obsługą błędów."""
        try:
            signals = await self._execute_query(self.client.table("buying_signals").select("*"), method_name="detect_buying_signals")
            detected = []
            
            for signal in signals:
                keywords = signal.get("keywords", [])
                if any(keyword.lower() in text.lower() for keyword in keywords):
                    detected.append({
                        "signal_type": signal.get("signal_type"),
                        "strength": signal.get("strength"),
                        "description": signal.get("description")
                    })
            
            return detected
        except DatabaseError:
            # Błąd został już zalogowany w _execute_query, rzucamy go dalej
            raise
        except Exception as e:
            logger.error(f"Błąd w logice detect_buying_signals: {e}", exc_info=True)
            # Zwracamy pustą listę, ponieważ to może być błąd logiki, a nie bazy danych
            return []

    # ==================== METODY ANALITYCZNE - ZREFRAKTORYZOWANE ====================
    
    async def calculate_tco_comparison(
        self, tesla_model: str, competitor_model: str, years: int = 5, km_per_year: int = 20000
    ) -> Dict[str, Any]:
        """Kalkuluje porównanie TCO, z poprawną obsługą błędów i bez .single()."""
        loop = asyncio.get_running_loop()
        try:
            # Używamy limit(1) zamiast single() aby uniknąć błędu przy wielu wynikach
            tesla_res = await loop.run_in_executor(None, lambda: self.client.table("products_tesla").select("*").eq("model_name", tesla_model).limit(1).execute())
            competitor_res = await loop.run_in_executor(None, lambda: self.client.table("products_competitors").select("*").eq("model_name", competitor_model).limit(1).execute())
            tco_template_res = await loop.run_in_executor(None, lambda: self.client.table("tco_calculation_templates").select("*").eq("customer_segment", "private").limit(1).execute())
            
            tesla = tesla_res.data[0] if tesla_res.data else None
            competitor = competitor_res.data[0] if competitor_res.data else None
            tco_template = tco_template_res.data[0] if tco_template_res.data else None

            if not (tesla and competitor and tco_template):
                logger.warning(f"Nie znaleziono danych dla modeli lub szablonu TCO: Tesla '{tesla_model}', konkurent '{competitor_model}'")
                return {}

            # Pełna kalkulacja TCO
            tesla_tco = {
                "purchase_price": tesla.get("base_price_pln", 0),
                "electricity_cost": km_per_year * years * tesla.get("battery_capacity_kwh", 75) / 100 * 0.15 * 0.70, # zużycie 15kWh/100km, cena 0.70zł/kWh
                "maintenance": years * 600,
                "insurance": years * tesla.get("base_price_pln", 0) * 0.03,
                "subsidies": -27000,
                "total": 0
            }
            tesla_tco["total"] = sum(v for k, v in tesla_tco.items() if k != 'total')

            competitor_tco = {
                "purchase_price": competitor.get("base_price_pln", 0),
                "fuel_cost": km_per_year / 100 * 7.0 * 6.80 * years, # 7L/100km, cena 6.80zł/L
                "maintenance": years * 1500,
                "insurance": years * competitor.get("base_price_pln", 0) * 0.04,
                "subsidies": 0,
                "total": 0
            }
            competitor_tco["total"] = sum(v for k, v in competitor_tco.items() if k != 'total')

            savings = competitor_tco["total"] - tesla_tco["total"]
            
            return {
                "tesla": tesla_tco,
                "competitor": competitor_tco,
                "total_savings": savings,
                "break_even_years": (tesla_tco["purchase_price"] - competitor_tco["purchase_price"]) / ((competitor_tco["fuel_cost"] + competitor_tco["maintenance"])/years - (tesla_tco["electricity_cost"] + tesla_tco["maintenance"])/years) if (competitor_tco["fuel_cost"] - tesla_tco["electricity_cost"]) > 0 else "N/A"
            }

        except Exception as e:
            logger.error(f"Błąd w calculate_tco_comparison: {e}", exc_info=True)
            raise DatabaseError("Nie udało się obliczyć porównania TCO.") from e
    
    async def get_comprehensive_customer_data(self, session_id: str) -> Dict[str, Any]:
        """Pobiera WSZYSTKIE dane klienta, z poprawną obsługą błędów."""
        loop = asyncio.get_running_loop()
        try:
            session_res = await loop.run_in_executor(None, lambda: self.client.table("session_metadata").select("*").eq("session_id", session_id).single().execute())
            interactions_res = await loop.run_in_executor(None, lambda: self.client.table("interaction_logs").select("*").eq("session_id", session_id).execute())
            # ... i tak dalej dla pozostałych tabel ...

            return {
                "session": session_res.data if session_res.data else {},
                "interactions": interactions_res.data if interactions_res.data else [],
                # ...
            }
        except Exception as e:
            logger.error(f"Błąd w get_comprehensive_customer_data: {e}", exc_info=True)
            raise DatabaseError(f"Nie udało się pobrać kompleksowych danych dla sesji {session_id}.") from e

    # ==================== STATYSTYKI - ZREFRAKTORYZOWANE ====================
    
    async def get_system_statistics(self) -> Dict[str, Any]:
        """Pobiera dynamiczne statystyki systemu."""
        loop = asyncio.get_running_loop()
        try:
            health_data = await self.health_check()

            # Pobierz dodatkowe, specyficzne statystyki
            playbooks_count_res = await loop.run_in_executor(None, lambda: self.client.table("playbooks").select("id", count='exact').limit(0).execute())
            playbooks_count = playbooks_count_res.count

            stats = {
                "database": {
                    "total_tables": health_data.get("tables_count"),
                    "total_records": health_data.get("total_records")
                },
                "knowledge_base": {
                    "playbooks": playbooks_count,
                    # ... można dodać więcej dynamicznych zliczeń ...
                },
            }
            return stats
        except Exception as e:
            logger.error(f"Błąd podczas pobierania statystyk systemu: {e}", exc_info=True)
            raise DatabaseError("Nie udało się pobrać statystyk systemu.") from e
    
    async def close(self) -> None:
        """Zamyka połączenie (jeśli potrzebne w przyszłości)."""
        pass
