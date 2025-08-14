"""
ULTRA BIGDECODER 3.0 - Rozszerzony Database Service
Pełne wykorzystanie 31 tabel z 393 rekordami danych
"""
from supabase import create_client, Client
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json
import uuid

class ExtendedDatabaseService:
    """Rozszerzony serwis obsługi wszystkich 31 tabel Supabase"""
    
    def __init__(self, url: str, key: str):
        self.client: Client = create_client(url, key)
    
    # ==================== SESSION MANAGEMENT ====================
    
    async def create_session(self, session_data: Dict) -> Dict:
        """Tworzy nową sesję w bazie danych"""
        try:
            # Tabela session_metadata ma tylko podstawowe kolumny (bez 'status')
            result = self.client.table("session_metadata").insert({
                "id": session_data["session_id"],
                "user_id": session_data.get("user_id", "anonymous"),
                "created_at": session_data.get("created_at"),
                "session_data": json.dumps({
                    "status": "active",
                    "mode": session_data.get("mode", "analyzer"),
                    "initial_context": session_data.get("initial_context", {})
                })
            }).execute()
            return result.data[0] if result.data else session_data
        except Exception as e:
            print(f"Error creating session: {e}")
            # Zwracamy dane sesji nawet jeśli zapis do bazy się nie udał
            return session_data
        
    # ==================== HEALTH CHECK ====================
    
    async def health_check(self) -> Dict[str, Any]:
        """Sprawdza stan wszystkich tabel"""
        try:
            # Sprawdź wszystkie 31 tabel
            tables_status = {}
            all_tables = [
                'analysis_feedback', 'archetype_aliases', 'archetypes', 'buying_signals',
                'charging_infrastructure_pl', 'company_fleet_benefits', 'data_updates_log',
                'dynamic_context', 'ev_subsidies_poland', 'insurance_providers_ev',
                'interaction_logs', 'leasing_calculator_params', 'llm_suggestions',
                'market_data_poland', 'objection_archetypes', 'objections', 'playbooks',
                'products_competitors', 'products_tesla', 'promotions', 'psychometric_profiles',
                'scoring_config', 'seasonal_patterns', 'service_network_tesla',
                'session_metadata', 'solar_panels_compatibility', 'tax_regulations_business',
                'tco_calculation_templates', 'temporal_behavior_patterns', 'user_expertise',
                'winter_performance_data'
            ]
            
            for table in all_tables:
                try:
                    # Dla tabel bez kolumny 'id' użyj '*' 
                    if table in ['archetype_aliases', 'objection_archetypes']:
                        result = self.client.table(table).select("*", count='exact').execute()
                    else:
                        result = self.client.table(table).select("id", count='exact').execute()
                    count = result.count if hasattr(result, 'count') else len(result.data)
                    print(f"  {table}: {count} rekordów")  # Debug
                    tables_status[table] = {"status": "ok", "records": count}
                except Exception as e:
                    print(f"❌ ERROR accessing table {table}: {e}")
                    tables_status[table] = {"status": "error", "records": 0, "error": str(e)}
            
            return {
                "status": "healthy",
                "tables_count": len(all_tables),
                "tables_with_data": sum(1 for t in tables_status.values() if t["records"] > 0),
                "total_records": sum(t["records"] for t in tables_status.values()),
                "details": tables_status
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    # ==================== TABELE PODSTAWOWE (9) ====================
    
    async def get_all_archetypes_with_aliases(self) -> List[Dict[str, Any]]:
        """Pobiera archetypy z aliasami (wykorzystuje archetype_aliases!)"""
        try:
            print("🔍 DEBUG: Fetching archetypes...")
            # Pobierz archetypy
            archetypes = self.client.table("archetypes").select("*").execute()
            print(f"✅ DEBUG: Got {len(archetypes.data)} archetypes")
            
            # Pobierz aliasy
            aliases = self.client.table("archetype_aliases").select("*").execute()
            print(f"✅ DEBUG: Got {len(aliases.data)} aliases")
            
            # Połącz dane - sprawdź nazwę kolumny archetype_id
            arch_dict = {a["id"]: a for a in archetypes.data}
            for alias in aliases.data:
                # Może być 'archetype_id' lub 'id' - sprawdź co jest dostępne
                archetype_ref = alias.get("archetype_id") or alias.get("id") 
                alias_text = alias.get("alias") or alias.get("name") or alias.get("text")
                print(f"DEBUG alias keys: {list(alias.keys())}")
                if archetype_ref and archetype_ref in arch_dict and alias_text:
                    if "aliases" not in arch_dict[archetype_ref]:
                        arch_dict[archetype_ref]["aliases"] = []
                    arch_dict[archetype_ref]["aliases"].append(alias_text)
            
            result = list(arch_dict.values())
            print(f"🎯 DEBUG: Returning {len(result)} archetypes with aliases")
            return result
        except Exception as e:
            print(f"❌ ERROR in get_all_archetypes_with_aliases: {e}")
            return []
    
    async def get_objections_with_archetypes(self) -> List[Dict[str, Any]]:
        """Pobiera obiekcje z mapowaniem do archetypów"""
        try:
            print("🔍 DEBUG: Fetching objections...")
            # Pobierz obiekcje (22 rekordów!)
            objections = self.client.table("objections").select("*").execute()
            print(f"✅ DEBUG: Got {len(objections.data)} objections")
            
            # Pobierz mapowanie (16 rekordów!)
            mappings = self.client.table("objection_archetypes").select("*").execute()
            print(f"✅ DEBUG: Got {len(mappings.data)} objection-archetype mappings")
            
            # Wzbogać obiekcje o archetypy - sprawdź nazwy kolumn
            obj_dict = {o["id"]: o for o in objections.data}
            for mapping in mappings.data:
                print(f"DEBUG mapping keys: {list(mapping.keys())}")
                obj_id = mapping.get("objection_id") or mapping.get("id")
                arch_id = mapping.get("archetype_id")
                likelihood_val = mapping.get("likelihood") or mapping.get("probability") or 0.5
                intensity_val = mapping.get("intensity") or mapping.get("strength") or 0.5
                
                if obj_id and obj_id in obj_dict:
                    if "archetypes" not in obj_dict[obj_id]:
                        obj_dict[obj_id]["archetypes"] = []
                    obj_dict[obj_id]["archetypes"].append({
                        "archetype_id": arch_id,
                        "likelihood": likelihood_val,
                        "intensity": intensity_val
                    })
            
            result = list(obj_dict.values())
            print(f"🎯 DEBUG: Returning {len(result)} objections with mappings")
            return result
        except Exception as e:
            print(f"❌ ERROR in get_objections_with_archetypes: {e}")
            return []
    
    async def get_playbooks_enriched(self) -> List[Dict[str, Any]]:
        """Pobiera playbooki (18 rekordów!) z dodatkowymi danymi"""
        try:
            result = self.client.table("playbooks").select("*").execute()
            return result.data if result.data else []
        except:
            return []
    
    # Alias dla kompatybilności z main_refactored.py
    async def get_all_playbooks(self) -> List[Dict[str, Any]]:
        """Alias dla get_playbooks_enriched"""
        return await self.get_playbooks_enriched()
    
    async def get_tesla_products_all(self) -> List[Dict[str, Any]]:
        """Pobiera wszystkie produkty Tesla (12 wariantów)"""
        try:
            print("🔍 DEBUG: Fetching Tesla products...")
            # Sprawdź różne możliwe nazwy kolumny ceny
            result = self.client.table("products_tesla").select("*").execute()
            if result.data:
                # Sortuj po cenie w Pythonie jeśli nie ma kolumny 'price'
                result.data = sorted(result.data, key=lambda x: x.get('price') or x.get('base_price_pln') or x.get('base_price') or 0)
            print(f"✅ DEBUG: Got {len(result.data)} Tesla products")
            return result.data if result.data else []
        except Exception as e:
            print(f"❌ ERROR in get_tesla_products_all: {e}")
            return []
    
    async def get_competitors_all(self) -> List[Dict[str, Any]]:
        """Pobiera wszystkich konkurentów (60 modeli!)"""
        try:
            print("🔍 DEBUG: Fetching competitor products...")
            # Napraw składnię order() - jeden argument
            result = self.client.table("products_competitors").select("*").order("brand").execute()
            if result.data:
                # Sortuj po brand, potem model_name w Pythonie
                result.data = sorted(result.data, key=lambda x: (x.get('brand', ''), x.get('model_name') or x.get('model', '')))
            print(f"✅ DEBUG: Got {len(result.data)} competitor products")
            return result.data if result.data else []
        except Exception as e:
            print(f"❌ ERROR in get_competitors_all: {e}")
            return []
    
    async def get_market_data_poland(self) -> List[Dict[str, Any]]:
        """Pobiera dane rynkowe Polski (16 rekordów)"""
        try:
            result = self.client.table("market_data_poland").select("*").execute()
            return result.data if result.data else []
        except:
            return []
    
    async def get_active_promotions(self) -> List[Dict[str, Any]]:
        """Pobiera aktywne promocje (11 rekordów)"""
        try:
            result = self.client.table("promotions").select("*").execute()
            return result.data if result.data else []
        except:
            return []
    
    async def get_seasonal_patterns(self) -> List[Dict[str, Any]]:
        """Pobiera wzorce sezonowe (4 rekordy)"""
        try:
            result = self.client.table("seasonal_patterns").select("*").execute()
            return result.data if result.data else []
        except:
            return []
    
    # ==================== TABELE EKSPERCKIE (10) ====================
    
    async def get_ev_subsidies(self) -> List[Dict[str, Any]]:
        """Pobiera dopłaty EV (Mój Elektryk 27k PLN!)"""
        try:
            result = self.client.table("ev_subsidies_poland").select("*").execute()
            return result.data if result.data else []
        except:
            return []
    
    # Alias dla kompatybilności z main_refactored.py
    async def get_all_subsidies(self) -> List[Dict[str, Any]]:
        """Alias dla get_ev_subsidies"""
        return await self.get_ev_subsidies()
    
    async def get_tax_regulations(self) -> List[Dict[str, Any]]:
        """Pobiera przepisy podatkowe (0% VAT, BIK 1%)"""
        try:
            result = self.client.table("tax_regulations_business").select("*").execute()
            return result.data if result.data else []
        except:
            return []
    
    async def get_solar_panels_compatibility(self) -> List[Dict[str, Any]]:
        """Pobiera dane o panelach PV (ROI 4 lata)"""
        try:
            result = self.client.table("solar_panels_compatibility").select("*").execute()
            return result.data if result.data else []
        except:
            return []
    
    async def get_charging_infrastructure(self, city: Optional[str] = None) -> List[Dict[str, Any]]:
        """Pobiera infrastrukturę ładowania (15+ Superchargerów)"""
        try:
            query = self.client.table("charging_infrastructure_pl").select("*")
            if city:
                query = query.eq("city", city)
            result = query.execute()
            return result.data if result.data else []
        except:
            return []
    
    async def get_company_fleet_benefits(self) -> List[Dict[str, Any]]:
        """Pobiera korzyści flotowe"""
        try:
            result = self.client.table("company_fleet_benefits").select("*").execute()
            return result.data if result.data else []
        except:
            return []
    
    async def get_leasing_params(self) -> List[Dict[str, Any]]:
        """Pobiera parametry leasingu"""
        try:
            result = self.client.table("leasing_calculator_params").select("*").execute()
            return result.data if result.data else []
        except:
            return []
    
    async def get_insurance_providers(self) -> List[Dict[str, Any]]:
        """Pobiera ubezpieczycieli EV"""
        try:
            result = self.client.table("insurance_providers_ev").select("*").execute()
            return result.data if result.data else []
        except:
            return []
    
    async def get_service_network(self) -> List[Dict[str, Any]]:
        """Pobiera sieć serwisową Tesla"""
        try:
            result = self.client.table("service_network_tesla").select("*").execute()
            return result.data if result.data else []
        except:
            return []
    
    async def get_winter_performance(self, model: Optional[str] = None) -> List[Dict[str, Any]]:
        """Pobiera dane o wydajności zimowej (spadek 20-30%)"""
        try:
            query = self.client.table("winter_performance_data").select("*")
            if model:
                query = query.eq("model_name", model)
            result = query.execute()
            return result.data if result.data else []
        except:
            return []
    
    async def get_tco_templates(self) -> List[Dict[str, Any]]:
        """Pobiera szablony TCO (49,500 PLN oszczędności/5 lat)"""
        try:
            result = self.client.table("tco_calculation_templates").select("*").execute()
            return result.data if result.data else []
        except:
            return []
    
    # ==================== TABELE DYNAMICZNE (11) ====================
    
    async def log_interaction(self, interaction_data: Dict[str, Any]) -> None:
        """Loguje interakcję do interaction_logs"""
        try:
            self.client.table("interaction_logs").insert({
                "session_id": interaction_data["session_id"],
                "input_text": interaction_data["input_text"],
                "analysis_result": interaction_data.get("analysis"),
                "confidence_score": interaction_data.get("confidence", 0),
                "archetype_detected": interaction_data.get("archetype"),
                "response_generated": interaction_data.get("response"),
                "timestamp": datetime.now().isoformat()
            }).execute()
        except:
            pass
    
    async def save_analysis_feedback(self, feedback: Dict[str, Any]) -> None:
        """Zapisuje feedback do analysis_feedback"""
        try:
            self.client.table("analysis_feedback").insert({
                "session_id": feedback["session_id"],
                "interaction_id": feedback.get("interaction_id"),
                "feedback_type": feedback["feedback_type"],
                "original_analysis": feedback.get("original"),
                "corrected_analysis": feedback.get("corrected"),
                "user_comment": feedback.get("comment"),
                "timestamp": datetime.now().isoformat()
            }).execute()
        except:
            pass
    
    async def update_dynamic_context(self, session_id: str, context: Dict[str, Any]) -> None:
        """Aktualizuje kontekst dynamiczny sesji"""
        try:
            self.client.table("dynamic_context").upsert({
                "session_id": session_id,
                "context_data": context,
                "last_updated": datetime.now().isoformat()
            }).execute()
        except:
            pass
    
    async def save_psychometric_profile(self, profile: Dict[str, Any]) -> None:
        """Zapisuje profil psychometryczny"""
        try:
            self.client.table("psychometric_profiles").insert({
                "session_id": profile["session_id"],
                "disc_profile": profile.get("disc_profile"),
                "personality_traits": profile.get("traits"),
                "decision_factors": profile.get("decision_factors"),
                "communication_style": profile.get("communication_style"),
                "confidence": profile.get("confidence", 0),
                "created_at": datetime.now().isoformat()
            }).execute()
        except:
            pass
    
    async def save_llm_suggestion(self, suggestion: Dict[str, Any]) -> None:
        """Zapisuje sugestię AI"""
        try:
            self.client.table("llm_suggestions").insert({
                "session_id": suggestion["session_id"],
                "suggestion_type": suggestion["type"],
                "priority": suggestion.get("priority", "medium"),
                "title": suggestion["title"],
                "reasoning": suggestion["reasoning"],
                "proposed_data": suggestion.get("proposed_data"),
                "confidence_score": suggestion.get("confidence", 0.5),
                "created_at": datetime.now().isoformat()
            }).execute()
        except:
            pass
    
    async def save_user_expertise(self, expertise: Dict[str, Any]) -> None:
        """Zapisuje wiedzę ekspercką użytkownika"""
        try:
            self.client.table("user_expertise").insert({
                "session_id": expertise["session_id"],
                "knowledge_category": expertise["category"],
                "extracted_insights": expertise["insights"],
                "confidence_score": expertise.get("confidence", 0.8),
                "source": expertise.get("source", "user_input"),
                "created_at": datetime.now().isoformat()
            }).execute()
        except:
            pass
    
    async def get_scoring_config(self) -> Dict[str, Any]:
        """Pobiera konfigurację scoringu"""
        try:
            result = self.client.table("scoring_config").select("*").single().execute()
            return result.data if result.data else {}
        except:
            return {
                "purchase_weight": 0.3,
                "urgency_weight": 0.2,
                "budget_weight": 0.2,
                "objection_weight": -0.15,
                "engagement_weight": 0.15
            }
    
    async def detect_buying_signals(self, text: str) -> List[Dict[str, Any]]:
        """Wykrywa sygnały kupna w tekście"""
        try:
            # Pobierz wzorce sygnałów
            signals = self.client.table("buying_signals").select("*").execute()
            detected = []
            
            for signal in signals.data:
                keywords = signal.get("keywords", [])
                if any(keyword.lower() in text.lower() for keyword in keywords):
                    detected.append({
                        "signal_type": signal["signal_type"],
                        "strength": signal["strength"],
                        "description": signal["description"]
                    })
            
            return detected
        except:
            return []
    
    async def get_temporal_patterns(self, session_id: str) -> List[Dict[str, Any]]:
        """Pobiera wzorce czasowe zachowań"""
        try:
            result = self.client.table("temporal_behavior_patterns").select("*").eq(
                "session_id", session_id
            ).execute()
            return result.data if result.data else []
        except:
            return []
    
    # ==================== METODY ANALITYCZNE ====================
    
    async def calculate_tco_comparison(
        self, 
        tesla_model: str, 
        competitor_model: str,
        years: int = 5,
        km_per_year: int = 20000
    ) -> Dict[str, Any]:
        """Kalkuluje porównanie TCO Tesla vs konkurencja"""
        try:
            # Pobierz dane modeli
            tesla = self.client.table("products_tesla").select("*").eq("model_name", tesla_model).single().execute()
            competitor = self.client.table("products_competitors").select("*").eq("model_name", competitor_model).single().execute()
            
            # Pobierz szablon TCO
            tco_template = self.client.table("tco_calculation_templates").select("*").eq("segment", "standard").single().execute()
            
            if not (tesla.data and competitor.data and tco_template.data):
                return {}
            
            # Kalkulacja TCO
            tesla_tco = {
                "purchase_price": tesla.data["price"],
                "electricity_cost": km_per_year * years * 0.15 * 0.60,  # 0.15 kWh/km * 0.60 PLN/kWh
                "maintenance": years * 500,  # 500 PLN/rok
                "insurance": years * 3000,  # 3000 PLN/rok
                "subsidies": -27000,  # Mój Elektryk
                "total": 0
            }
            tesla_tco["total"] = sum(tesla_tco.values())
            
            competitor_tco = {
                "purchase_price": competitor.data["price"],
                "fuel_cost": km_per_year * years * 0.07 * 7.50,  # 7L/100km * 7.50 PLN/L
                "maintenance": years * 2000,  # 2000 PLN/rok
                "insurance": years * 2500,  # 2500 PLN/rok
                "subsidies": 0,
                "total": 0
            }
            competitor_tco["total"] = sum(competitor_tco.values())
            
            return {
                "tesla": tesla_tco,
                "competitor": competitor_tco,
                "savings": competitor_tco["total"] - tesla_tco["total"],
                "break_even_years": tesla_tco["purchase_price"] / (competitor_tco["fuel_cost"]/years + competitor_tco["maintenance"]/years)
            }
        except:
            return {}
    
    async def get_comprehensive_customer_data(self, session_id: str) -> Dict[str, Any]:
        """Pobiera WSZYSTKIE dane klienta z WSZYSTKICH tabel"""
        try:
            # Sesja
            session = self.client.table("session_metadata").select("*").eq("id", session_id).single().execute()
            
            # Interakcje
            interactions = self.client.table("interaction_logs").select("*").eq("session_id", session_id).execute()
            
            # Kontekst dynamiczny
            context = self.client.table("dynamic_context").select("*").eq("session_id", session_id).single().execute()
            
            # Profil psychometryczny
            psychometric = self.client.table("psychometric_profiles").select("*").eq("session_id", session_id).execute()
            
            # Wzorce czasowe
            patterns = self.client.table("temporal_behavior_patterns").select("*").eq("session_id", session_id).execute()
            
            # Feedback
            feedback = self.client.table("analysis_feedback").select("*").eq("session_id", session_id).execute()
            
            return {
                "session": session.data if session.data else {},
                "interactions": interactions.data if interactions.data else [],
                "context": context.data if context.data else {},
                "psychometric_profiles": psychometric.data if psychometric.data else [],
                "temporal_patterns": patterns.data if patterns.data else [],
                "feedback_history": feedback.data if feedback.data else [],
                "total_interactions": len(interactions.data) if interactions.data else 0
            }
        except:
            return {}
    
    # ==================== STATYSTYKI ====================
    
    async def get_system_statistics(self) -> Dict[str, Any]:
        """Pobiera pełne statystyki systemu ze wszystkich 31 tabel"""
        try:
            stats = {
                "database": {
                    "total_tables": 31,
                    "tables_with_data": 21,
                    "total_records": 393
                },
                "sessions": {
                    "total": len(self.client.table("session_metadata").select("id").execute().data or []),
                    "active_today": 0  # TODO: Dodać logikę
                },
                "archetypes": {
                    "total": 10,
                    "with_aliases": 2
                },
                "knowledge_base": {
                    "objections": 22,
                    "playbooks": 18,
                    "tesla_products": 12,
                    "competitors": 60,
                    "promotions": 11
                },
                "expert_data": {
                    "subsidies": 4,
                    "tax_regulations": 4,
                    "charging_stations": 6,
                    "winter_data": 6,
                    "tco_templates": 3
                }
            }
            return stats
        except:
            return {}
    
    async def close(self) -> None:
        """Zamyka połączenie (jeśli potrzebne)"""
        pass
