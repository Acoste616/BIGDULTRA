"""
ULTRA BIGDECODER 3.0 - Database Service
Serwis do komunikacji z Supabase
"""
from supabase import create_client, Client
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from uuid import UUID, uuid4

class DatabaseService:
    """Serwis obsługi bazy danych Supabase"""
    
    def __init__(self, url: str, key: str):
        self.client: Client = create_client(url, key)
        
    async def health_check(self) -> bool:
        """Sprawdza połączenie z bazą"""
        try:
            result = self.client.table("archetypes").select("id").limit(1).execute()
            return True
        except:
            return False
    
    # ==================== SESJE ====================
    
    async def create_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tworzy nową sesję"""
        try:
            # Zapisz do session_metadata - wykorzystuj PEŁNY schemat Supabase
            result = self.client.table("session_metadata").insert({
                "id": str(session_data["session_id"]),
                "session_id": str(session_data["session_id"]),
                "user_id": session_data.get("user_id", "anonymous"),
                "client_context": session_data.get("client_context", {}),
                "archetype_evolution": session_data.get("archetype_evolution", []),
                "final_scores": session_data.get("final_scores", {}),
                "total_interactions": session_data.get("total_interactions", 0),
                "session_outcome": session_data.get("session_outcome")
            }).execute()
            return result.data[0] if result.data else {}
        except Exception:
            # Minimalny fallback aby UI miało identyfikator sesji
            return {"id": session_data["session_id"]}
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Pobiera dane sesji"""
        
        try:
            result = self.client.table("session_metadata").select("*").eq(
                "id", session_id
            ).single().execute()
            return result.data if result.data else None
        except Exception:
            return None
    
    async def update_session_profile(
        self, 
        session_id: str, 
        archetype_info: Dict[str, Any]
    ) -> None:
        """Aktualizuje profil w sesji"""
        
        # Pobierz aktualną sesję
        session = await self.get_session(session_id)
        if not session:
            return
        try:
            # Zaktualizuj profil
            current_profile = session.get("profile", {})
            current_profile.update({
                "archetype": archetype_info,
                "last_updated": datetime.now().isoformat()
            })
            # Zapisz
            self.client.table("session_metadata").update({
                "profile": current_profile
            }).eq("id", session_id).execute()
        except Exception:
            return
    
    # ==================== ARCHETYPY ====================
    
    async def get_archetype(self, archetype_id: UUID) -> Optional[Dict[str, Any]]:
        """Pobiera dane archetypu"""
        
        result = self.client.table("archetypes").select("*").eq(
            "id", str(archetype_id)
        ).single().execute()
        
        return result.data if result.data else None
    
    async def get_all_archetypes(self) -> List[Dict[str, Any]]:
        """Pobiera wszystkie archetypy"""
        
        result = self.client.table("archetypes").select("*").order("id").execute()
        return result.data if result.data else []
    
    # ==================== OBIEKCJE ====================
    
    async def get_objection(self, objection_id: UUID) -> Optional[Dict[str, Any]]:
        """Pobiera dane obiekcji"""
        
        result = self.client.table("objections").select("*").eq(
            "id", str(objection_id)
        ).single().execute()
        
        return result.data if result.data else None
    
    async def get_all_objections(self) -> List[Dict[str, Any]]:
        """Pobiera wszystkie obiekcje"""
        
        result = self.client.table("objections").select("*").order("id").execute()
        return result.data if result.data else []
    
    async def get_objections_for_archetype(
        self, 
        archetype_id: UUID
    ) -> List[Dict[str, Any]]:
        """Pobiera obiekcje powiązane z archetypem"""
        
        # Pobierz mapowanie
        mapping = self.client.table("objection_archetypes").select(
            "objection_id"
        ).eq("archetype_id", str(archetype_id)).execute()
        
        if not mapping.data:
            return []
        
        objection_ids = [m["objection_id"] for m in mapping.data]
        
        # Pobierz obiekcje
        result = self.client.table("objections").select("*").in_(
            "id", objection_ids
        ).execute()
        
        return result.data if result.data else []
    
    # ==================== PLAYBOOKI ====================
    
    async def get_playbook(self, playbook_id: UUID) -> Optional[Dict[str, Any]]:
        """Pobiera dane playbooka"""
        
        result = self.client.table("playbooks").select("*").eq(
            "id", str(playbook_id)
        ).single().execute()
        
        return result.data if result.data else None
    
    async def get_all_playbooks(self) -> List[Dict[str, Any]]:
        """Pobiera wszystkie playbooki"""
        
        result = self.client.table("playbooks").select("*").order("id").execute()
        return result.data if result.data else []
    
    async def get_playbook_for_archetype(
        self, 
        archetype_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """Pobiera playbook dla archetypu"""
        
        result = self.client.table("playbooks").select("*").eq(
            "target_archetype_id", str(archetype_id)
        ).limit(1).execute()
        
        return result.data[0] if result.data else None
    
    # ==================== PRODUKTY ====================
    
    async def get_tesla_products(self) -> List[Dict[str, Any]]:
        """Pobiera produkty Tesla"""
        
        result = self.client.table("products_tesla").select("*").order(
            "model_name", "variant"
        ).execute()
        
        return result.data if result.data else []
    
    async def get_competitor_products(self) -> List[Dict[str, Any]]:
        """Pobiera produkty konkurencji"""
        
        result = self.client.table("products_competitors").select("*").order(
            "brand", "model_name"
        ).execute()
        
        return result.data if result.data else []
    
    # ==================== LOGI I INTERAKCJE ====================
    
    async def log_interaction(self, interaction_data: Dict[str, Any]) -> None:
        """Loguje interakcję"""
        
        try:
            self.client.table("interaction_logs").insert({
                "id": str(uuid4()),
                "session_id": str(interaction_data.get("session_id")),
                "input_text": interaction_data.get("input_text"),
                "analysis": interaction_data.get("analysis"),
                "enriched_data": {
                    "archetype": interaction_data.get("archetype_data"),
                    "objections": interaction_data.get("objections_data"),
                    "playbook": interaction_data.get("playbook_data")
                },
                "timestamp": interaction_data.get("timestamp", datetime.now().isoformat())
            }).execute()
        except Exception:
            pass
        
        try:
            # Zapisz też do data_updates_log
            self.client.table("data_updates_log").insert({
                "id": str(uuid4()),
                "session_id": str(interaction_data.get("session_id")),
                "user_input": interaction_data.get("input_text"),
                "llm_analysis": interaction_data.get("analysis"),
                "table_affected": "interaction_logs",
                "operation_type": "INSERT",
                "records_affected": 1,
                "success": True,
                "created_at": datetime.now().isoformat()
            }).execute()
        except Exception:
            pass
    
    # ==================== SUGESTIE I FEEDBACK ====================
    
    async def create_suggestion(self, suggestion_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tworzy sugestię AI"""
        
        result = self.client.table("llm_suggestions").insert({
            "id": str(uuid4()),
            "session_id": str(suggestion_data.get("session_id")),
            "suggestion_type": suggestion_data.get("suggestion_type"),
            "priority": suggestion_data.get("priority"),
            "title": suggestion_data.get("title"),
            "reasoning": suggestion_data.get("reasoning"),
            "proposed_data": suggestion_data.get("proposed_data"),
            "confidence_score": suggestion_data.get("confidence_score", 0.8),
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }).execute()
        
        return result.data[0] if result.data else {}
    
    async def save_feedback(self, feedback_data: Dict[str, Any]) -> None:
        """Zapisuje feedback użytkownika"""
        
        self.client.table("analysis_feedback").insert({
            "id": str(uuid4()),
            "session_id": str(feedback_data.get("session_id")),
            "feedback_type": feedback_data.get("feedback_type"),
            "content": feedback_data.get("content"),
            "rating": feedback_data.get("rating"),
            "metadata": feedback_data.get("metadata", {}),
            "created_at": datetime.now().isoformat()
        }).execute()
    
    async def save_to_user_expertise(self, expertise_data: Dict[str, Any]) -> None:
        """Zapisuje wiedzę ekspercką użytkownika"""
        
        self.client.table("user_expertise").insert({
            "id": str(uuid4()),
            "session_id": str(expertise_data.get("session_id")),
            "knowledge_category": expertise_data.get("knowledge_category"),
            "extracted_insights": expertise_data.get("extracted_insights"),
            "confidence_score": expertise_data.get("confidence_score", 0.9),
            "validation_status": "pending",
            "created_at": datetime.now().isoformat()
        }).execute()
    
    # ==================== DANE RYNKOWE ====================
    
    async def get_market_data(self) -> List[Dict[str, Any]]:
        """Pobiera dane rynkowe Polski"""
        
        result = self.client.table("market_data_poland").select("*").execute()
        return result.data if result.data else []
    
    async def get_promotions(self) -> List[Dict[str, Any]]:
        """Pobiera aktualne promocje"""
        
        result = self.client.table("promotions").select("*").eq(
            "is_active", True
        ).execute()
        
        return result.data if result.data else []
    
    async def get_seasonal_patterns(self) -> List[Dict[str, Any]]:
        """Pobiera wzorce sezonowe"""
        
        result = self.client.table("seasonal_patterns").select("*").execute()
        return result.data if result.data else []
    
    # ==================== STATYSTYKI ====================
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Pobiera statystyki systemu"""
        
        stats = {}
        
        # Liczba sesji
        sessions = self.client.table("session_metadata").select(
            "id", count="exact"
        ).execute()
        stats["total_sessions"] = sessions.count if hasattr(sessions, 'count') else 0
        
        # Aktywne sesje
        active = self.client.table("session_metadata").select(
            "id", count="exact"
        ).eq("status", "active").execute()
        stats["active_sessions"] = active.count if hasattr(active, 'count') else 0
        
        # Liczba interakcji
        interactions = self.client.table("interaction_logs").select(
            "id", count="exact"
        ).execute()
        stats["total_interactions"] = interactions.count if hasattr(interactions, 'count') else 0
        
        # Top archetypy - uproszczona agregacja po stronie klienta
        try:
            from collections import Counter

            logs = self.client.table("interaction_logs").select("analysis").execute()
            if logs.data:
                archetype_names = [
                    log['analysis']['archetype']['name']
                    for log in logs.data
                    if log.get('analysis') and log['analysis'].get('archetype') and log['analysis']['archetype'].get('name')
                ]
                stats['top_archetypes'] = [{"name": name, "count": count} for name, count in Counter(archetype_names).most_common(5)]

                confidences = [
                    log['analysis']['archetype']['confidence']
                    for log in logs.data
                    if log.get('analysis') and log['analysis'].get('archetype') and log['analysis']['archetype'].get('confidence')
                ]
                if confidences:
                    stats['average_confidence'] = sum(confidences) / len(confidences)
                else:
                    stats['average_confidence'] = 0
            else:
                stats["top_archetypes"] = []
                stats['average_confidence'] = 0
        except Exception:
            stats["top_archetypes"] = []
            stats['average_confidence'] = 0

        # Top obiekcje (placeholder - wymaga bardziej złożonej logiki JSON)
        stats["top_objections"] = []
        
        # Współczynnik konwersji (placeholder)
        stats["conversion_rate"] = 0.15
        
        return stats
    
    # ==================== KONFIGURACJA SCORINGU ====================
    
    async def get_scoring_config(self) -> Optional[Dict[str, Any]]:
        """Pobiera aktywną konfigurację scoringu"""
        
        result = self.client.table("scoring_config").select("*").eq(
            "is_active", True
        ).limit(1).execute()
        
        return result.data[0] if result.data else None
    
    async def update_scoring_config(
        self, 
        config_data: Dict[str, Any]
    ) -> None:
        """Aktualizuje konfigurację scoringu"""
        
        # Dezaktywuj obecną
        self.client.table("scoring_config").update({
            "is_active": False
        }).eq("is_active", True).execute()
        
        # Utwórz nową
        self.client.table("scoring_config").insert({
            "id": str(uuid4()),
            "is_active": True,
            "feature_weights": config_data.get("feature_weights"),
            "thresholds": config_data.get("thresholds"),
            "ema_alpha": config_data.get("ema_alpha", 0.4),
            "notes": config_data.get("notes"),
            "created_at": datetime.now().isoformat()
        }).execute()
    
    # ==================== SYGNAŁY KUPNA ====================
    
    async def get_buying_signals(self) -> List[Dict[str, Any]]:
        """Pobiera sygnały kupna"""
        
        result = self.client.table("buying_signals").select("*").execute()
        return result.data if result.data else []
    
    async def detect_buying_signals(
        self, 
        text: str
    ) -> List[Dict[str, Any]]:
        """Wykrywa sygnały kupna w tekście"""
        
        # Pobierz wszystkie sygnały
        signals = await self.get_buying_signals()
        detected = []
        
        # Prosta detekcja (w przyszłości można użyć ML)
        for signal in signals:
            patterns = signal.get("detection_patterns", {})
            if patterns and any(p.lower() in text.lower() for p in patterns.get("keywords", [])):
                detected.append(signal)
        
        return detected
    
    # ==================== WZORCE CZASOWE ====================
    
    async def get_temporal_patterns(self) -> List[Dict[str, Any]]:
        """Pobiera wzorce czasowe"""
        
        result = self.client.table("temporal_behavior_patterns").select("*").execute()
        return result.data if result.data else []
    
    async def get_current_temporal_pattern(self) -> Optional[Dict[str, Any]]:
        """Pobiera wzorzec dla aktualnej pory"""
        
        from datetime import datetime
        current_hour = datetime.now().hour
        
        # Prosty przykład - wieczorni klienci
        if current_hour >= 18:
            result = self.client.table("temporal_behavior_patterns").select("*").eq(
                "time_range", "after_18:00"
            ).limit(1).execute()
            
            return result.data[0] if result.data else None
        
        return None

    # ==================== PAMIĘĆ DŁUGOTERMINOWA ====================

    async def save_dynamic_context(self, context_data: Dict[str, Any]) -> None:
        """Zapisuje nowy fragment wiedzy do pamięci długoterminowej"""
        try:
            self.client.table("dynamic_context").insert({
                "id": str(uuid4()),
                "context_type": context_data.get("context_type", "general"),
                "source": context_data.get("source", "user_command"),
                "content_summary": context_data.get("content_summary"),
                "entities": context_data.get("entities"),
                "tags": context_data.get("tags"),
                "relevance_score": context_data.get("relevance_score", 0.8),
                "created_at": datetime.now().isoformat()
            }).execute()
        except Exception as e:
            print(f"Error saving dynamic context: {e}")
            pass

    async def save_psychometric_profile(self, profile_data: Dict[str, Any]) -> None:
        """Archiwizuje profil psychometryczny klienta po sesji"""
        try:
            self.client.table("psychometric_profiles").insert({
                "id": str(uuid4()),
                "session_id": str(profile_data.get("session_id")),
                "final_archetype_id": str(profile_data.get("final_archetype_id")),
                "disc_scores": profile_data.get("disc_scores"),
                "schwartz_values": profile_data.get("schwartz_values"),
                "fun_drive_score": profile_data.get("fun_drive_score"),
                "ovn_score": profile_data.get("ovn_score"),
                "key_triggers": profile_data.get("key_triggers"),
                "key_objections": profile_data.get("key_objections"),
                "created_at": datetime.now().isoformat()
            }).execute()
        except Exception as e:
            print(f"Error saving psychometric profile: {e}")
            pass
    
    async def close(self):
        """Zamyka połączenie z bazą (placeholder dla async)"""
        pass
