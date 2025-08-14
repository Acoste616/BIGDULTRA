"""
ULTRA BIGDECODER 3.0 - Expert Ollama Client
Pełna integracja z gpt-oss:120b + wykorzystanie 31 tabel danych
"""
from ollama import Client
import json
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
from cachetools import TTLCache
import sys
import os

# Dodaj ścieżkę do backend
backend_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

try:
    from prompts.expert_system_prompt import EXPERT_SYSTEM_PROMPT, ANALYSIS_PROMPT
except ImportError:
    # Fallback prompt jeśli nie można załadować
    EXPERT_SYSTEM_PROMPT = """Jesteś Ultra BIGDecoder 3.0 - ekspertem sprzedaży Tesla."""
    ANALYSIS_PROMPT = """Analizuj z SEPARACJĄ mechanizmów."""

from ..database_extended import ExtendedDatabaseService

class ExpertOllamaClient:
    """Ekspertowy klient AI wykorzystujący pełną wiedzę z 31 tabel"""
    
    def __init__(self, base_url: str, api_key: str, model: str, db_service: ExtendedDatabaseService):
        self.base_url = base_url
        self.api_key = api_key
        # Popraw nazwę modelu na gpt-oss:120b
        self.model = "gpt-oss:120b" if "gpt" in model.lower() or "120" in model else model
        self.db_service = db_service
        
        # Oficjalny klient Ollama
        self.client = Client(
            host=base_url,
            headers={'Authorization': api_key}
        )
        
        # Cache z TTL
        self.cache = TTLCache(maxsize=200, ttl=300)
        
        # Załaduj dane eksperckie przy starcie
        self.expert_data = {}
        
        # Śledzenie ewolucji archetypu dla każdej sesji
        self.archetype_evolution = {}
        
        # Historia konwersacji dla każdej sesji (Ultra 3.0)
        self.conversation_histories = {}
        
    async def initialize_expert_knowledge(self):
        """Ładuje wszystkie dane eksperckie z 31 tabel"""
        try:
            # Podstawowe dane (9 tabel)
            self.expert_data["archetypes"] = await self.db_service.get_all_archetypes_with_aliases()
            self.expert_data["objections"] = await self.db_service.get_objections_with_archetypes()
            self.expert_data["playbooks"] = await self.db_service.get_playbooks_enriched()
            self.expert_data["tesla_products"] = await self.db_service.get_tesla_products_all()
            self.expert_data["competitors"] = await self.db_service.get_competitors_all()
            self.expert_data["market_data"] = await self.db_service.get_market_data_poland()
            self.expert_data["promotions"] = await self.db_service.get_active_promotions()
            self.expert_data["seasonal"] = await self.db_service.get_seasonal_patterns()
            
            # Dane eksperckie (10 tabel)
            self.expert_data["subsidies"] = await self.db_service.get_ev_subsidies()
            self.expert_data["tax_regulations"] = await self.db_service.get_tax_regulations()
            self.expert_data["solar_panels"] = await self.db_service.get_solar_panels_compatibility()
            self.expert_data["charging_infra"] = await self.db_service.get_charging_infrastructure()
            self.expert_data["fleet_benefits"] = await self.db_service.get_company_fleet_benefits()
            self.expert_data["leasing"] = await self.db_service.get_leasing_params()
            self.expert_data["insurance"] = await self.db_service.get_insurance_providers()
            self.expert_data["service_network"] = await self.db_service.get_service_network()
            self.expert_data["winter_data"] = await self.db_service.get_winter_performance()
            self.expert_data["tco_templates"] = await self.db_service.get_tco_templates()
            
            # Konfiguracja scoringu
            self.expert_data["scoring_config"] = await self.db_service.get_scoring_config()
            
            print(f"✅ Załadowano wiedzę ekspercką: {sum(len(v) if isinstance(v, list) else 1 for v in self.expert_data.values())} rekordów z 31 tabel")
            
        except Exception as e:
            print(f"⚠️ Błąd ładowania wiedzy eksperckiej: {e}")
    
    def _build_enriched_system_prompt(self, session_context: Dict[str, Any]) -> str:
        """Buduje wzbogacony prompt z pełną wiedzą ekspercką"""
        
        # Rozpocznij od podstawowego prompta eksperckiego
        prompt = EXPERT_SYSTEM_PROMPT
        
        # Dodaj aktualny kontekst sesji
        if session_context:
            prompt += f"\n\n🔍 KONTEKST SESJI:\n"
            if "profile" in session_context:
                prompt += f"- Profil klienta: {json.dumps(session_context['profile'], ensure_ascii=False)}\n"
            if "history" in session_context:
                prompt += f"- Historia: {len(session_context.get('history', []))} interakcji\n"
        
        # Dodaj kluczowe dane z bazy
        prompt += "\n\n📊 AKTUALNE DANE Z BAZY (31 TABEL, 393 REKORDY):\n"
        
        # Archetypy z aliasami
        if self.expert_data.get("archetypes"):
            prompt += f"\n🎭 ARCHETYPY KLIENTÓW ({len(self.expert_data['archetypes'])}):\n"
            for arch in self.expert_data["archetypes"]:
                aliases = arch.get("aliases", [])
                prompt += f"- {arch['name']}: {arch.get('description', '')}"
                if aliases:
                    prompt += f" (aliasy: {', '.join(aliases)})"
                prompt += "\n"
        
        # Obiekcje z mapowaniem
        if self.expert_data.get("objections"):
            prompt += f"\n❌ OBIEKCJE ({len(self.expert_data['objections'])}):\n"
            for obj in self.expert_data["objections"][:5]:  # Top 5
                prompt += f"- {obj.get('type', '')}: {obj.get('description', '')}\n"
        
        # Aktualne promocje
        if self.expert_data.get("promotions"):
            prompt += f"\n🎁 AKTUALNE PROMOCJE ({len(self.expert_data['promotions'])}):\n"
            for promo in self.expert_data["promotions"][:3]:
                prompt += f"- {promo.get('name', '')}: {promo.get('discount_amount', '')} PLN\n"
        
        # Dopłaty
        if self.expert_data.get("subsidies"):
            prompt += f"\n💰 DOPŁATY EV:\n"
            for subsidy in self.expert_data["subsidies"]:
                prompt += f"- {subsidy.get('program_name', '')}: do {subsidy.get('max_amount', '')} PLN\n"
        
        # Przepisy podatkowe
        if self.expert_data.get("tax_regulations"):
            prompt += f"\n📋 PRZEPISY PODATKOWE:\n"
            for reg in self.expert_data["tax_regulations"]:
                prompt += f"- {reg.get('regulation_type', '')}: {reg.get('benefit_description', '')}\n"
        
        return prompt
    
    def _split_customer_input_ultra3(self, customer_input: str, session_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        ULTRA 3.0: Dzieli customer_input na history i last_message
        """
        session_id = session_context.get("session_id", "unknown")
        
        # Pobierz historię konwersacji dla tej sesji
        if session_id not in self.conversation_histories:
            self.conversation_histories[session_id] = []
        
        history = self.conversation_histories[session_id]
        
        # Sprawdź czy to odpowiedź na pytanie (zawiera "ODPOWIEDŹ:")
        if "ODPOWIEDŹ:" in customer_input.upper():
            # To jest odpowiedź na pytanie - dodaj do historii i oznacz
            parts = customer_input.split(":")
            if len(parts) > 1:
                answer = ":".join(parts[1:]).strip()
                history.append({
                    "type": "question_answer", 
                    "content": answer,
                    "timestamp": datetime.now().isoformat()
                })
                last_message = f"Klient odpowiedział: {answer}"
            else:
                last_message = customer_input
        else:
            # Zwykła obserwacja - dodaj do historii
            history.append({
                "type": "observation",
                "content": customer_input,
                "timestamp": datetime.now().isoformat()
            })
            last_message = customer_input
        
        # Ogranicz historię do ostatnich 10 wpisów (performance)
        if len(history) > 10:
            history = history[-10:]
            self.conversation_histories[session_id] = history
        
        # Zbuduj string historii dla prompt
        history_text = ""
        for entry in history[:-1]:  # Wszystko oprócz ostatniego (last_message)
            if entry["type"] == "observation":
                history_text += f"- Obserwacja: {entry['content']}\n"
            elif entry["type"] == "question_answer":
                history_text += f"- Odpowiedź na pytanie: {entry['content']}\n"
        
        return {
            "history": history_text.strip(),
            "last_message": last_message,
            "conversation_entries": len(history)
        }
    
    async def analyze_customer_expert(
        self,
        customer_input: str,
        session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Główna funkcja analizy wykorzystująca pełną wiedzę z 31 tabel
        """
        
        # ULTRA 3.0: Podziel input na historię i ostatnią wiadomość
        input_split = self._split_customer_input_ultra3(customer_input, session_context or {})
        history = input_split["history"]
        last_message = input_split["last_message"]
        
        print(f"🔍 ULTRA 3.0: Historia ({input_split['conversation_entries']} wpisów): {history[:100]}...")
        print(f"🎯 ULTRA 3.0: Ostatnia wiadomość: {last_message}")
        
        # Sprawdź cache - używaj tylko last_message dla cache key
        cache_key = hashlib.md5(f"{last_message}_{history}".encode()).hexdigest()
        if cache_key in self.cache:
            print(f"💾 ULTRA 3.0: Cache hit")
            return self.cache[cache_key]
        
        # Pobierz kompleksowe dane klienta jeśli jest sesja
        if session_context and session_context.get("session_id"):
            full_customer_data = await self.db_service.get_comprehensive_customer_data(
                session_context["session_id"]
            )
            session_context["full_data"] = full_customer_data
        
        # Wykryj sygnały kupna z ostatniej wiadomości
        buying_signals = await self.db_service.detect_buying_signals(last_message)
        
        # Zbuduj wzbogacony prompt systemowy
        system_prompt = self._build_enriched_system_prompt(session_context)
        
        # ULTRA 3.0: Użyj nowego ANALYSIS_PROMPT z separacją
        analysis_prompt = ANALYSIS_PROMPT.format(
            history=history,
            last_input=last_message
        )
        
        # Dodaj kontekst sygnałów kupna
        analysis_prompt += f"""

WYKRYTE SYGNAŁY KUPNA: {json.dumps(buying_signals, ensure_ascii=False)}

ZASADY ULTRA 3.0:
- Historia = kontekst ogólny
- Last_input = focus odpowiedzi
- Client_response = konkretna odpowiedź DO KLIENTA na ostatnią wiadomość
- Quick_reply = coaching DLA SPRZEDAWCY na podstawie całości
- Priority_questions: critical=true jeśli confidence < 0.7
- Dane: 27k PLN dopłaty, 0% VAT, 225k amortyzacja
"""
        
        try:
            # Użyj oficjalnego klienta Ollama
            print(f"🔍 DEBUG: Calling Ollama API with model: {self.model}")
            
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": analysis_prompt
                }
            ]
            
            # Wywołaj chat API (nie stream dla JSON response)
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": 0.7,
                    "num_predict": 2000
                },
                format="json"  # Wymusza odpowiedź JSON
            )
            
            # Ollama zwraca odpowiedź w response['message']['content']
            if response and 'message' in response:
                content = response['message'].get('content', '{}')
                print(f"✅ ULTRA 3.0: Got response from Ollama")
                try:
                    analysis = json.loads(content)
                    print(f"🎯 ULTRA 3.0: JSON parsed successfully")
                    
                    # Waliduj nowe pola Ultra 3.0
                    if "client_response" not in analysis:
                        analysis["client_response"] = f"Dzięki za informację o: {last_message[:50]}..."
                    if "priority_questions" not in analysis:
                        analysis["priority_questions"] = []
                    
                    # Waliduj structure priority_questions
                    for i, q in enumerate(analysis.get("priority_questions", [])):
                        if isinstance(q, str):
                            # Konwertuj stary format na nowy
                            analysis["priority_questions"][i] = {
                                "text": q,
                                "critical": False,
                                "reason": "Pytanie pogłębiające"
                            }
                        elif isinstance(q, dict) and "critical" not in q:
                            q["critical"] = False
                            
                except json.JSONDecodeError as e:
                    print(f"⚠️ ULTRA 3.0: JSON parsing failed: {e}")
                    # Fallback structure z nowym formatem
                    analysis = {
                        "archetype": {"name": "Unknown", "confidence": 0.0},
                        "client_response": f"Dzięki za informację: {last_message}",
                        "quick_reply": "COACHING: Potrzebuj więcej informacji o kliencie.",
                        "priority_questions": [
                            {"text": "Jaki jest Pana budżet?", "critical": True, "reason": "Brak danych o budżecie"}
                        ],
                        "confidence": 0.2,
                        "ultra3_fallback": True
                    }
                
                # Wzbogać analizę o dane z bazy
                analysis = await self._enrich_analysis_with_db_data(analysis)
                
                # EWOLUCJA ARCHETYPU - śledź historię zmian
                session_id = session_context.get("session_id") if session_context else "unknown"
                if session_id not in self.archetype_evolution:
                    self.archetype_evolution[session_id] = []
                
                # Dodaj aktualny archetyp do historii
                if analysis.get("archetype"):
                    self.archetype_evolution[session_id].append({
                        "name": analysis["archetype"].get("name", "Unknown"),
                        "confidence": analysis.get("confidence", 0),
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Dodaj historię ewolucji do odpowiedzi
                    analysis["archetype_evolution"] = self.archetype_evolution[session_id][-5:]  # Ostatnie 5 zmian
                
                # Zapisz w cache
                self.cache[cache_key] = analysis
                
                # ULTRA 3.0: Loguj interakcję z nowym formatem
                await self.db_service.log_interaction({
                    "session_id": session_context.get("session_id") if session_context else None,
                    "input_text": customer_input,
                    "last_message": last_message,
                    "history_entries": input_split["conversation_entries"],
                    "analysis": analysis,
                    "confidence": analysis.get("confidence", 0),
                    "archetype": analysis.get("archetype"),
                    "client_response": analysis.get("client_response"),
                    "coaching_reply": analysis.get("quick_reply"),
                    "priority_questions": analysis.get("priority_questions", []),
                    "ultra3_version": True
                })
                
                return analysis
            else:
                print(f"❌ No response from Ollama API")
                raise Exception(f"No response from Ollama API")
                
        except Exception as e:
            print(f"❌ ULTRA 3.0: Błąd analizy: {e}")
            # ULTRA 3.0: Fallback z nowym formatem
            return await self._fallback_analysis_ultra3(last_message, history, buying_signals)
    
    async def _enrich_analysis_with_db_data(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Wzbogaca analizę o pełne dane z bazy"""
        
        # Wzbogać archetyp
        if analysis.get("archetype") and analysis["archetype"].get("id"):
            arch_id = analysis["archetype"]["id"]
            for arch in self.expert_data.get("archetypes", []):
                if arch["id"] == arch_id:
                    analysis["archetype"]["full_data"] = arch
                    break
        
        # Wzbogać obiekcje
        if analysis.get("objections"):
            for i, obj in enumerate(analysis["objections"]):
                if obj.get("id"):
                    for db_obj in self.expert_data.get("objections", []):
                        if db_obj["id"] == obj["id"]:
                            analysis["objections"][i]["full_data"] = db_obj
                            break
        
        # Dodaj dane o promocjach
        analysis["available_promotions"] = self.expert_data.get("promotions", [])[:3]
        
        # Dodaj dane o dopłatach
        analysis["subsidies"] = self.expert_data.get("subsidies", [])
        
        # Dodaj porównanie TCO jeśli wspomina o kosztach
        if any(word in analysis.get("quick_reply", "").lower() for word in ["koszt", "cena", "drogo", "tani"]):
            tco_comparison = await self.db_service.calculate_tco_comparison(
                "Model 3", "BMW 320i", years=5, km_per_year=20000
            )
            if tco_comparison:
                analysis["tco_comparison"] = tco_comparison
        
        return analysis
    
    async def _fallback_analysis_ultra3(self, last_message: str, history: str, buying_signals: List) -> Dict[str, Any]:
        """ULTRA 3.0: Analiza awaryjna z separacją mechanizmów"""
        
        # Prosta analiza słów kluczowych z ostatniej wiadomości
        text_lower = last_message.lower()
        
        # Wykryj archetyp
        archetype = {"id": 1, "name": "Unknown", "confidence": 0.3}
        
        if any(word in text_lower for word in ["rodzina", "dzieci", "bezpiecz"]):
            archetype = {"id": 5, "name": "Family Guardian", "confidence": 0.7}
        elif any(word in text_lower for word in ["cena", "koszt", "drogo", "tani"]):
            archetype = {"id": 8, "name": "Value Optimizer", "confidence": 0.7}
        elif any(word in text_lower for word in ["szybk", "przyspiesz", "moc"]):
            archetype = {"id": 6, "name": "Performance Driver", "confidence": 0.7}
        elif any(word in text_lower for word in ["ekolog", "środowisk", "emisj"]):
            archetype = {"id": 2, "name": "Eco-Tech Pragmatist", "confidence": 0.7}
        
        # Wykryj obiekcje
        objections = []
        if "drogo" in text_lower or "cena" in text_lower:
            objections.append({
                "id": 1,
                "type": "price_concern",
                "intensity": 0.8,
                "rebuttal": "Tesla Model 3 z dopłatą Mój Elektryk (27,000 PLN) kosztuje mniej niż BMW serii 3"
            })
        
        if "zasięg" in text_lower or "daleko" in text_lower:
            objections.append({
                "id": 2,
                "type": "range_anxiety", 
                "intensity": 0.7,
                "rebuttal": "Model 3 Long Range ma zasięg 629km - więcej niż większość aut spalinowych"
            })
        
        # ULTRA 3.0: Separacja odpowiedzi
        client_response = f"Rozumiem Pana obawy. Tesla Model 3 z dopłatą 27,000 PLN to bardzo atrakcyjna opcja."
        quick_reply = "COACHING: Podkreśl konkretne oszczędności - TCO 49,500 PLN/5 lat i dopłatę Mój Elektryk."
        
        # ULTRA 3.0: Priority questions z critical flag
        priority_questions = [
            {"text": "Jaki jest Pana budżet na samochód?", "critical": True, "reason": "Brak danych o budżecie - kluczowe dla dopasowania modelu"},
            {"text": "Ile kilometrów średnio pokonuje Pan rocznie?", "critical": False, "reason": "Do kalkulacji TCO"},
            {"text": "Czy rozważa Pan zakup przez firmę?", "critical": True, "reason": "0% VAT i korzyści podatkowe dla firm"}
        ]
        
        # Dodatkowe pytania jeśli confidence < 0.7
        if archetype["confidence"] < 0.7:
            priority_questions.insert(0, {"text": "Co jest dla Pana najważniejsze w nowym samochodzie?", "critical": True, "reason": "Brak jasnego archetypu - potrzebujemy więcej informacji"})
        
        return {
            "archetype": archetype,
            "objections": objections,
            "client_response": client_response,
            "quick_reply": quick_reply,
            "priority_questions": priority_questions,
            "purchase_probability": 0.4,
            "churn_risk": 0.3,
            "strategy": {
                "playbook_id": 1,
                "approach": "educational",
                "key_points": ["Dopłaty", "TCO", "Korzyści podatkowe"]
            },
            "next_actions": ["Prezentacja TCO", "Kalkulacja oszczędności"],
            "buying_signals": buying_signals,
            "confidence": archetype["confidence"],
            "ultra3_fallback": True,
            "history_considered": bool(history)
        }
    
    async def generate_coaching_response(
        self,
        customer_profile: Dict[str, Any],
        objection: Optional[str] = None,
        mode: str = "coach"
    ) -> Dict[str, Any]:
        """Generuje odpowiedź coachingową dla sprzedawcy"""
        
        system_prompt = self._build_enriched_system_prompt({"profile": customer_profile})
        
        coach_prompt = f"""
TRYB: {mode.upper()}
PROFIL KLIENTA: {json.dumps(customer_profile, ensure_ascii=False)}
OBIEKCJA: {objection if objection else "Brak"}

Jako ekspert sprzedaży, podpowiedz sprzedawcy:
1. Jak najlepiej odpowiedzieć na tę obiekcję
2. Jakie argumenty użyć (z danymi)
3. Jaki playbook zastosować
4. Następne kroki

Odpowiedz po polsku, konkretnie, z danymi liczbowymi.
"""
        
        try:
            response = await self.client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": coach_prompt}
                    ],
                    "temperature": 0.6,
                    "max_tokens": 1000
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "coaching": result["choices"][0]["message"]["content"],
                    "mode": mode,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                raise Exception(f"API error: {response.status_code}")
                
        except Exception as e:
            return {
                "coaching": "Pokaż klientowi kalkulator TCO i wspomnij o dopłacie 27,000 PLN.",
                "mode": mode,
                "error": str(e)
            }
    
    async def close(self):
        """Zamyka połączenie klienta Ollama (obsługa sync/async)."""
        try:
            # Preferuj async jeśli dostępne
            aclose = getattr(self.client, "aclose", None)
            if callable(aclose):
                await aclose()
                return
            # Fallback na sync close
            close = getattr(self.client, "close", None)
            if callable(close):
                close()
        except Exception:
            # Bezpieczny no-op
            pass
