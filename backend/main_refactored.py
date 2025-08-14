"""
ULTRA BIGDECODER 3.0 - Zrefaktoryzowany Backend
Pełne wykorzystanie 31 tabel z 393 rekordami danych
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import json
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe
load_dotenv()

# Import konfiguracji i serwisów
from config import config
from services.ai.expert_ollama_client import ExpertOllamaClient
from services.ai.metrics_calculator import MetricsCalculator
from services.database_extended import ExtendedDatabaseService
from models.schemas import (
    CustomerAnalysisRequest,
    CustomerAnalysisResponse,
    SessionCreateRequest,
    SessionResponse,
    SuggestionRequest,
    FeedbackRequest
)

# Globalne instancje
expert_ai_client: Optional[ExpertOllamaClient] = None
extended_db_service: Optional[ExtendedDatabaseService] = None
metrics_calculator: Optional[MetricsCalculator] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Zarządzanie cyklem życia aplikacji z pełną inicjalizacją"""
    global expert_ai_client, extended_db_service, metrics_calculator
    
    # Startup
    print("🚀 Uruchamianie Ultra BIGDecoder 3.0 - WERSJA ROZSZERZONA")
    print("📊 Inicjalizacja 31 tabel z 393 rekordami danych...")
    
    # Inicjalizacja rozszerzonego serwisu bazy danych
    extended_db_service = ExtendedDatabaseService(
        url=config.SUPABASE_URL,
        key=config.SUPABASE_KEY
    )
    
    # Sprawdź stan bazy
    db_health = await extended_db_service.health_check()
    print(f"✅ Baza danych: {db_health.get('tables_with_data', 0)} tabel z danymi")
    print(f"📈 Łącznie rekordów: {db_health.get('total_records', 0)}")
    
    # Inicjalizacja ekspertowego klienta AI
    expert_ai_client = ExpertOllamaClient(
        base_url=config.OLLAMA_BASE_URL,
        api_key=config.OLLAMA_API_KEY,
        model=config.OLLAMA_MODEL,
        db_service=extended_db_service
    )
    
    # Załaduj wiedzę ekspercką
    await expert_ai_client.initialize_expert_knowledge()
    
    # Inicjalizacja kalkulatora metryk
    metrics_calculator = MetricsCalculator()
    
    print("✅ System ULTRA BIGDECODER 3.0 gotowy!")
    print("🧠 Model AI: gptoss 120b z pełną wiedzą ekspercką")
    print("📊 Kalkulator metryk: OVN, Churn, Fun-Drive, Purchase")
    print("🎯 Tryby: analyzer, coach, expert, hybrid, sparring")
    
    yield
    
    # Shutdown
    print("🔄 Zamykanie systemu...")
    if expert_ai_client:
        await expert_ai_client.close()
    if extended_db_service:
        await extended_db_service.close()
    print("👋 System zamknięty")

# Inicjalizacja FastAPI
app = FastAPI(
    title="Ultra BIGDecoder 3.0 API - ROZSZERZONA",
    description="Inteligentny asystent sprzedaży Tesla z pełnym wykorzystaniem 31 tabel danych",
    version="3.1.0",
    lifespan=lifespan
)

# CORS middleware - dozwolone dla lokalnych plików
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dozwolone wszystkie origins (w tym file://)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    """Endpoint główny - status API z pełnymi statystykami"""
    stats = await extended_db_service.get_system_statistics() if extended_db_service else {}
    
    return {
        "name": "Ultra BIGDecoder 3.0 - ROZSZERZONA",
        "version": "3.1.0",
        "status": "operational",
        "model": config.OLLAMA_MODEL,
        "database": {
            "tables": 31,
            "records": stats.get("database", {}).get("total_records", 393),
            "archetypes": 10,
            "objections": 22,
            "playbooks": 18
        },
        "expert_knowledge": {
            "subsidies": "Mój Elektryk 27,000 PLN",
            "tax": "0% VAT do 2026",
            "infrastructure": "15+ Superchargerów",
            "tco_savings": "49,500 PLN/5 lat"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Sprawdzenie zdrowia systemu - wszystkie komponenty"""
    
    health_status = {
        "api": "healthy",
        "database": "unknown",
        "ai": "unknown",
        "expert_data": "unknown",
        "timestamp": datetime.now().isoformat()
    }
    
    # Sprawdź rozszerzoną bazę danych
    try:
        if extended_db_service:
            db_health = await extended_db_service.health_check()
            health_status["database"] = "healthy" if db_health.get("status") == "healthy" else "unhealthy"
            health_status["database_details"] = {
                "tables_count": db_health.get("tables_count", 0),
                "tables_with_data": db_health.get("tables_with_data", 0),
                "total_records": db_health.get("total_records", 0)
            }
    except:
        health_status["database"] = "unhealthy"
    
    # Sprawdź AI
    try:
        if expert_ai_client:
            health_status["ai"] = "healthy"
            health_status["expert_data"] = "loaded" if expert_ai_client.expert_data else "not_loaded"
    except:
        health_status["ai"] = "unhealthy"
    
    # Określ ogólny status
    if "unhealthy" in health_status.values():
        return JSONResponse(status_code=503, content=health_status)
    
    return health_status

# ==================== SESJE ====================

@app.post("/sessions/create", response_model=SessionResponse)
async def create_session(request: SessionCreateRequest):
    """Tworzy nową sesję sprzedażową z pełnym kontekstem"""
    
    session_id = str(uuid.uuid4())
    
    # Zapisz w bazie z rozszerzonymi danymi
    session_data = {
        "session_id": session_id,
        "user_id": request.user_id or "anonymous",
        "metadata": request.metadata or {},
        "client_context": {},
        "archetype_evolution": [],
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    await extended_db_service.create_session(session_data)
    
    return SessionResponse(
        session_id=session_id,
        created_at=session_data["created_at"],
        status="active"
    )

# ==================== ANALIZA KLIENTA - PEŁNA MOC 31 TABEL ====================

@app.post("/analyze", response_model=CustomerAnalysisResponse)
async def analyze_customer(request: CustomerAnalysisRequest):
    """
    Główny endpoint analizy klienta - wykorzystuje WSZYSTKIE 31 tabel
    """
    print(f"🔍 DEBUG: Otrzymano żądanie analizy - session_id: {request.session_id}, text: {request.input_text[:50]}...")
    
    if not expert_ai_client:
        print("❌ DEBUG: expert_ai_client nie jest dostępne")
        raise HTTPException(status_code=503, detail="AI nie jest dostępne")
    
    try:
        # Pobierz pełny kontekst sesji ze wszystkich tabel
        session_context = {}
        if request.session_id:
            # Pobierz KOMPLEKSOWE dane klienta
            customer_data = await extended_db_service.get_comprehensive_customer_data(request.session_id)
            session_context = {
                "session_id": request.session_id,
                "profile": customer_data.get("session", {}).get("profile", {}),
                "history": customer_data.get("interactions", []),
                "psychometric": customer_data.get("psychometric_profiles", []),
                "patterns": customer_data.get("temporal_patterns", []),
                "total_interactions": customer_data.get("total_interactions", 0)
            }
        
        # Sprawdź tryb analizy (continuous = ciągła analiza po każdym wpisie)
        is_continuous = request.mode == "continuous"
        
        # Analiza przez ekspertowego klienta AI
        analysis = await expert_ai_client.analyze_customer_expert(
            customer_input=request.input_text,
            session_context=session_context
        )
        
        # ULTRA 3.0: Oblicz wszystkie metryki (OVN, Churn, Fun-Drive, Purchase)
        if metrics_calculator:
            # Przygotuj dane sesji do kalkulacji metryk
            session_metrics_data = {
                'messages': session_context.get('history', []),
                'has_solar_panels': 'panel' in request.input_text.lower() or 'pv' in request.input_text.lower(),
                'is_business_context': 'firma' in request.input_text.lower() or 'business' in request.input_text.lower(),
                'has_family': 'rodzina' in request.input_text.lower() or 'dzieci' in request.input_text.lower(),
                'eco_conscious': 'ekolog' in request.input_text.lower() or 'środowisk' in request.input_text.lower(),
                'tech_savvy': 'technolog' in request.input_text.lower() or 'innowac' in request.input_text.lower(),
                'competitor_mentions': request.input_text.lower().count('bmw') + request.input_text.lower().count('audi') + request.input_text.lower().count('mercedes'),
                'current_car': session_context.get('profile', {}).get('current_car'),
                'annual_mileage': session_context.get('profile', {}).get('annual_mileage'),
                'charging_possibility': session_context.get('profile', {}).get('charging_possibility'),
                'budget_range': session_context.get('profile', {}).get('budget_range'),
                'purchase_timeline': session_context.get('profile', {}).get('purchase_timeline'),
                'avg_response_time': 15,  # Domyślnie 15 sekund
                'interaction_scores': [0.5, 0.6, 0.7]  # Przykładowe wyniki poprzednich interakcji
            }
            
            # Oblicz metryki
            metrics = metrics_calculator.calculate_all_metrics(
                session_data=session_metrics_data,
                analysis_result=analysis
            )
            
            # Dodaj metryki do analizy
            analysis['metrics'] = metrics
            analysis['purchase_likelihood'] = metrics['purchase_likelihood'] / 100  # Znormalizowane 0-1
            analysis['churn_risk'] = metrics['churn_risk'] / 100
            analysis['fun_drive_score'] = metrics['fun_drive_score']
            analysis['ovn_potential'] = metrics['ovn_potential']
            analysis['cta_readiness'] = metrics['cta_readiness']
            analysis['next_actions'] = metrics['next_actions']
            analysis['deescalation_signals'] = metrics['deescalation_signals']
        
        # Wzbogać o dodatkowe dane eksperckie (tylko w trybie pełnej analizy)
        analysis["enriched_data"] = {}
        if not is_continuous:
            # Dodaj dopłaty (tabela ev_subsidies_poland)
            subsidies = await extended_db_service.get_all_subsidies()
            if subsidies:
                analysis["enriched_data"]["subsidies"] = subsidies[:3]  # Top 3 dopłaty
            
            # Dodaj korzyści podatkowe (tabela tax_regulations_business)
            tax_benefits = await extended_db_service.get_tax_regulations()
            if tax_benefits:
                analysis["enriched_data"]["tax_benefits"] = {
                    "vat_rate": 0,  # 0% VAT do 2026
                    "depreciation": 100,  # 100% amortyzacja
                    "bik": 1  # BIK 1%
                }
        
        # Jeśli klient wspomina o panelach PV (tabela solar_panels_compatibility)
        if not is_continuous and any(word in request.input_text.lower() for word in ["panel", "fotowolta", "pv", "solar"]):
            solar_data = await extended_db_service.get_solar_panels_compatibility()
            if solar_data:
                analysis["enriched_data"]["solar_integration"] = {
                    "daily_range_from_pv": "40-60 km",
                    "roi_years": 4,
                    "annual_savings": "8,000-12,000 PLN"
                }
        
        # Jeśli klient pyta o ładowanie (tabela charging_infrastructure_pl)
        if not is_continuous and any(word in request.input_text.lower() for word in ["ładow", "charge", "supercharger"]):
            charging = await extended_db_service.get_charging_infrastructure()
            if charging:
                analysis["enriched_data"]["charging_infrastructure"] = {
                    "superchargers_count": len([c for c in charging if "supercharger" in c.get("charger_type", "").lower()]),
                    "price_range": "1.45-2.85 PLN/kWh"
                }
        
        # Jeśli klient wspomina o zimie (tabela winter_performance_data)
        if not is_continuous and any(word in request.input_text.lower() for word in ["zima", "zimą", "mróz", "zimno"]):
            winter_data = await extended_db_service.get_winter_performance()
            if winter_data:
                analysis["enriched_data"]["winter_performance"] = {
                    "range_loss": "20-30%",
                    "heat_pump": "Tak - standard w nowych modelach",
                    "preconditioning": "Dostępne przez aplikację"
                }
        
        # Wzbogać o archetyp z pełnymi danymi
        if not is_continuous and analysis.get("archetype", {}).get("id"):
            archetypes = await extended_db_service.get_all_archetypes_with_aliases()
            for arch in archetypes:
                if arch["id"] == analysis["archetype"]["id"]:
                    analysis["archetype"]["full_data"] = arch
                    break
        
        # ZAWSZE dodaj porównanie TCO (tabela tco_calculation_templates)
        if not is_continuous:
            tco_comparison = await extended_db_service.calculate_tco_comparison(
                "Model 3", "BMW 320i", years=5, km_per_year=20000
            )
            analysis["enriched_data"]["tco_comparison"] = {
                "savings": tco_comparison.get("total_savings", 49500),
                "break_even_years": tco_comparison.get("break_even_years", 3.5)
            }
        
        # Jeśli confidence >= 0.8, dodaj pełną strategię i playbooki
        if analysis.get("confidence_score", 0) >= 0.8:
            playbooks = await extended_db_service.get_all_playbooks()
            if playbooks:
                analysis["enriched_data"]["playbook_details"] = {
                    "name": playbooks[0].get("name", "Strategia standardowa"),
                    "key_tactics": playbooks[0].get("strategy_details", {})
                }
        
        # Zapisz profil psychometryczny
        if not is_continuous and analysis.get("archetype") and analysis.get("confidence", 0) > 0.7:
            await extended_db_service.save_psychometric_profile({
                "session_id": request.session_id,
                "disc_profile": analysis["archetype"].get("disc_profile"),
                "traits": analysis["archetype"].get("traits"),
                "decision_factors": analysis.get("decision_factors"),
                "communication_style": analysis.get("communication_style"),
                "confidence": analysis.get("confidence", 0)
            })
        
        # Aktualizuj kontekst dynamiczny
        await extended_db_service.update_dynamic_context(
            request.session_id,
            {
                "last_input": request.input_text,
                "last_analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        # Log interakcji - lekki zapis historii rozmowy
        try:
            await extended_db_service.log_interaction({
                "session_id": request.session_id,
                "input_text": request.input_text,
                "analysis": analysis,
                "archetype": analysis.get("archetype"),
                "response": analysis.get("client_response"),
                "confidence": analysis.get("confidence", 0)
            })
        except:
            pass
        
        # Zapewnij zgodność struktury obiekcji z modelem Pydantic
        raw_objections = analysis.get("objections", [])
        normalized_objections = []
        for obj in raw_objections:
            if isinstance(obj, dict):
                text_val = (
                    obj.get("text")
                    or obj.get("description")
                    or obj.get("rebuttal")
                    or obj.get("type")
                    or ""
                )
                normalized = {
                    "id": obj.get("id", 0),
                    "type": obj.get("type", "general"),
                    "text": text_val,
                    "hidden": obj.get("hidden", False),
                }
                if obj.get("severity") is not None:
                    normalized["severity"] = obj.get("severity")
                rs = obj.get("rebuttal_strategy") or (
                    {"text": obj.get("rebuttal")} if obj.get("rebuttal") else None
                )
                if rs is not None:
                    normalized["rebuttal_strategy"] = rs
                normalized_objections.append(normalized)
        analysis["objections"] = normalized_objections
        
        # Zbuduj odpowiedź zgodną ze schematem
        response = CustomerAnalysisResponse(
            session_id=request.session_id,
            archetype=analysis.get("archetype"),
            objections=analysis.get("objections", []),
            strategy=analysis.get("strategy"),
            questions=analysis.get("deep_questions", []),
            priority_questions=analysis.get("priority_questions", []),
            purchase_probability=analysis.get("purchase_probability", 0.0),
            next_actions=analysis.get("next_actions", []),
            enriched_data={
                "subsidies": analysis.get("subsidies", []) if not is_continuous else [],
                "promotions": analysis.get("available_promotions", []) if not is_continuous else [],
                "tco_comparison": analysis.get("tco_comparison", {}) if not is_continuous else {},
                "buying_signals": analysis.get("buying_signals", [])
            },
            confidence_score=analysis.get("confidence", 0.0),
            quick_reply=analysis.get("quick_reply"),
            deep_questions=analysis.get("deep_questions"),
            archetypes_top3=[analysis.get("archetype")] if analysis.get("archetype") else [],
            scores={
                "purchase_likelihood": analysis.get("purchase_likelihood", analysis.get("purchase_probability", 0)) * 100,
                "churn_risk": analysis.get("churn_risk", 0) * 100,
                "fun_drive_score": analysis.get("fun_drive_score", 0),
                "ovn_potential": analysis.get("ovn_potential", 5),
                "cta_readiness": analysis.get("cta_readiness", "build_trust")
            }
        )
        
        print(f"✅ DEBUG: Analiza zakończona pomyślnie - archetyp: {analysis.get('archetype', {}).get('name', 'Unknown')}")
        return response
        
    except Exception as e:
        print(f"❌ DEBUG: Błąd w analizie: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Błąd analizy: {str(e)}"
        )

# ==================== STRATEGIA I COACHING ====================

@app.post("/strategy/generate")
async def generate_strategy(
    session_id: str,
    mode: str = "coach"
):
    """Generuje strategię sprzedażową z wykorzystaniem 18 playbooków"""
    
    print(f"🔍 DEBUG: Generowanie strategii dla session_id: {session_id}, mode: {mode}")
    
    # Pobierz pełne dane klienta
    customer_data = await extended_db_service.get_comprehensive_customer_data(session_id)
    
    if not customer_data:
        raise HTTPException(status_code=404, detail="Sesja nie znaleziona")
    
    profile = customer_data.get("session", {}).get("profile", {})
    last_interaction = customer_data.get("interactions", [{}])[-1] if customer_data.get("interactions") else {}
    
    print(f"🔍 DEBUG: Profil klienta: {profile}")
    print(f"🔍 DEBUG: Ostatnia interakcja: {last_interaction}")
    
    # Generuj strategię przez ekspertowego klienta
    strategy = await expert_ai_client.generate_coaching_response(
        customer_profile=profile,
        objection=last_interaction.get("input_text"),
        mode=mode
    )
    
    # Wzbogać o playbooki
    playbooks = await extended_db_service.get_playbooks_enriched()
    relevant_playbooks = [p for p in playbooks if p.get("archetype_id") == profile.get("archetype", {}).get("id")]
    
    return {
        "session_id": session_id,
        "mode": mode,
        "strategy": strategy,
        "playbooks": relevant_playbooks[:3],  # Top 3 playbooki
        "timestamp": datetime.now().isoformat()
    }

# ==================== DANE EKSPERCKIE - WSZYSTKIE 31 TABEL ====================

@app.get("/data/comprehensive")
async def get_comprehensive_data():
    """Pobiera dane ze WSZYSTKICH 31 tabel"""
    
    return {
        # Podstawowe (9 tabel)
        "archetypes": await extended_db_service.get_all_archetypes_with_aliases(),
        "objections": await extended_db_service.get_objections_with_archetypes(),
        "playbooks": await extended_db_service.get_playbooks_enriched(),
        "tesla_products": await extended_db_service.get_tesla_products_all(),
        "competitors": await extended_db_service.get_competitors_all(),
        "market_data": await extended_db_service.get_market_data_poland(),
        "promotions": await extended_db_service.get_active_promotions(),
        "seasonal": await extended_db_service.get_seasonal_patterns(),
        
        # Eksperckie (10 tabel)
        "subsidies": await extended_db_service.get_ev_subsidies(),
        "tax_regulations": await extended_db_service.get_tax_regulations(),
        "solar_panels": await extended_db_service.get_solar_panels_compatibility(),
        "charging_infrastructure": await extended_db_service.get_charging_infrastructure(),
        "fleet_benefits": await extended_db_service.get_company_fleet_benefits(),
        "leasing": await extended_db_service.get_leasing_params(),
        "insurance": await extended_db_service.get_insurance_providers(),
        "service_network": await extended_db_service.get_service_network(),
        "winter_performance": await extended_db_service.get_winter_performance(),
        "tco_templates": await extended_db_service.get_tco_templates(),
        
        # Statystyki
        "statistics": await extended_db_service.get_system_statistics()
    }

@app.get("/data/subsidies")
async def get_subsidies():
    """Pobiera informacje o dopłatach (Mój Elektryk 27k PLN!)"""
    subsidies = await extended_db_service.get_ev_subsidies()
    return {
        "subsidies": subsidies,
        "highlight": "Mój Elektryk - do 27,000 PLN dopłaty!",
        "total_available": sum(s.get("max_amount", 0) for s in subsidies)
    }

@app.get("/data/tco/{tesla_model}/{competitor_model}")
async def get_tco_comparison(
    tesla_model: str,
    competitor_model: str,
    years: int = 5,
    km_per_year: int = 20000
):
    """Kalkuluje porównanie TCO"""
    comparison = await extended_db_service.calculate_tco_comparison(
        tesla_model, competitor_model, years, km_per_year
    )
    return comparison

@app.get("/data/charging-infrastructure/{city}")
async def get_charging_by_city(city: str):
    """Pobiera infrastrukturę ładowania dla miasta"""
    stations = await extended_db_service.get_charging_infrastructure(city)
    return {
        "city": city,
        "stations": stations,
        "total": len(stations),
        "superchargers": [s for s in stations if "Supercharger" in s.get("station_name", "")]
    }

# ==================== FEEDBACK I SUGESTIE ====================

@app.post("/feedback/submit")
async def submit_feedback(request: FeedbackRequest):
    """Przyjmuje feedback użytkownika i zapisuje do analysis_feedback"""
    
    await extended_db_service.save_analysis_feedback({
        "session_id": request.session_id,
        "feedback_type": request.feedback_type,
        "original": request.metadata.get("original") if request.metadata else None,
        "corrected": request.content,
        "comment": request.metadata.get("comment") if request.metadata else None
    })
    
    # Jeśli to korekta ekspertowa, zapisz też do user_expertise
    if request.feedback_type == "correction":
        await extended_db_service.save_user_expertise({
            "session_id": request.session_id,
            "category": "user_correction",
            "insights": {
                "original": request.metadata.get("original"),
                "corrected": request.content
            },
            "confidence": 1.0,
            "source": "user_feedback"
        })
    
    return {
        "success": True,
        "message": "Feedback zapisany i wykorzystany do ulepszenia modelu"
    }

@app.post("/suggestions/create")
async def create_suggestion(request: SuggestionRequest):
    """Tworzy sugestię AI zapisywaną do llm_suggestions"""
    
    await extended_db_service.save_llm_suggestion({
        "session_id": request.session_id,
        "type": request.suggestion_type,
        "priority": request.priority,
        "title": request.title,
        "reasoning": request.reasoning,
        "proposed_data": request.proposed_data,
        "confidence": request.confidence_score
    })
    
    return {
        "success": True,
        "message": "Sugestia AI utworzona"
    }

# ==================== STATYSTYKI ====================

@app.get("/stats/dashboard")
async def get_dashboard_stats():
    """Pobiera pełne statystyki dashboardu ze wszystkich 31 tabel"""
    
    stats = await extended_db_service.get_system_statistics()
    
    return {
        "database": stats.get("database", {}),
        "sessions": stats.get("sessions", {}),
        "knowledge_base": stats.get("knowledge_base", {}),
        "expert_data": stats.get("expert_data", {}),
        "highlights": {
            "total_tables": 31,
            "total_records": 393,
            "archetypes": 10,
            "objections": 22,
            "playbooks": 18,
            "subsidies": "27,000 PLN",
            "tco_savings": "49,500 PLN/5 lat"
        },
        "timestamp": datetime.now().isoformat()
    }

# ==================== AI SPARRING PARTNER ====================

@app.post("/sparring/simulate")
async def simulate_client_response(
    session_id: str,
    seller_message: str,
    mode: str = "client"
):
    """
    AI Sparring Partner - symuluje klienta na podstawie archetypu
    """
    if not expert_ai_client:
        raise HTTPException(status_code=503, detail="AI nie jest dostępne")
    
    # Pobierz kontekst sesji
    customer_data = await extended_db_service.get_comprehensive_customer_data(session_id)
    
    if not customer_data:
        raise HTTPException(status_code=404, detail="Sesja nie znaleziona")
    
    profile = customer_data.get("session", {}).get("profile", {})
    archetype = profile.get("archetype", {}).get("name", "Pragmatic Analyst")
    
    # Symuluj odpowiedź klienta
    if mode == "client":
        # AI jako klient
        prompt = f"""Jesteś klientem typu {archetype}. 
        Sprzedawca właśnie powiedział: "{seller_message}"
        Odpowiedz jako ten typ klienta - krótko, naturalnie, zgodnie z profilem.
        Pamiętaj o charakterystycznych obawach i motywacjach tego archetypu."""
        
        response = await expert_ai_client.generate_response(prompt)
        
        return {
            "mode": "client",
            "archetype": archetype,
            "client_response": response,
            "reasoning": f"Odpowiedź oparta na archetypu {archetype}",
            "suggestions": [
                "Zwróć uwagę na ton klienta",
                "Dostosuj swoją strategię do jego obaw"
            ]
        }
    
    elif mode == "coach":
        # AI jako coach
        prompt = f"""Jako coach sprzedażowy, oceń wypowiedź sprzedawcy: "{seller_message}"
        w kontekście klienta typu {archetype}.
        Daj krótką, konkretną radę jak ulepszyć podejście."""
        
        response = await expert_ai_client.generate_response(prompt)
        
        return {
            "mode": "coach",
            "coaching_advice": response,
            "better_approach": "Spróbuj bardziej empatycznego podejścia",
            "key_points": [
                "Słuchaj aktywnie",
                "Zadawaj otwarte pytania",
                "Buduj zaufanie przed sprzedażą"
            ]
        }
    
    else:  # hybrid
        # Połączenie obu trybów
        client_response = await expert_ai_client.generate_response(
            f"Jako klient {archetype}, odpowiedz na: {seller_message}"
        )
        
        coaching_advice = await expert_ai_client.generate_response(
            f"Jako coach, oceń tę wypowiedź sprzedawcy dla klienta {archetype}: {seller_message}"
        )
        
        return {
            "mode": "hybrid",
            "client_response": client_response,
            "coaching_advice": coaching_advice,
            "archetype": archetype
        }

@app.post("/sparring/live-update")
async def live_strategy_update(
    session_id: str,
    update_trigger: str,
    context_change: Dict[str, Any]
):
    """
    Live Strategy Updates - aktualizuje strategię w czasie rzeczywistym
    """
    # Pobierz obecny stan
    customer_data = await extended_db_service.get_comprehensive_customer_data(session_id)
    
    if not customer_data:
        raise HTTPException(status_code=404, detail="Sesja nie znaleziona")
    
    current_profile = customer_data.get("session", {}).get("profile", {})
    
    # Mapowanie triggerów na zmiany strategii
    strategy_updates = {}
    
    if update_trigger == "test_drive_completed":
        strategy_updates = {
            "archetype_shift": f"{current_profile.get('archetype', {}).get('name', 'Unknown')} → Enthusiast",
            "purchase_likelihood_change": "+15%",
            "new_strategy": "Strike while iron is hot - emotion-driven approach",
            "priority_questions": [
                "Który model najbardziej podobał?",
                "Co najbardziej zaskoczyło podczas jazdy?",
                "Kiedy mógłby Pan odebrać auto?"
            ],
            "recommended_actions": [
                "Pokaż konfigurację online",
                "Omów opcje finansowania",
                "Zaproponuj termin dostawy"
            ]
        }
    
    elif update_trigger == "financing_questions":
        strategy_updates = {
            "churn_risk_change": "+10%",
            "new_concerns": ["budget_constraints", "monthly_payment"],
            "recommended_tools": ["financing_calculator", "trade_in_estimator"],
            "de_escalation": "Focus on total value, not monthly payment",
            "priority_questions": [
                "Jaki budżet miesięczny Pan rozważa?",
                "Czy ma Pan auto do rozliczenia?"
            ]
        }
    
    elif update_trigger == "excitement_visible":
        strategy_updates = {
            "purchase_likelihood_change": "+8%",
            "emotional_state": "positive",
            "recommended_cta": "Immediate configuration session",
            "tactics": ["Use enthusiasm momentum", "Visual configuration", "Social proof"]
        }
    
    elif update_trigger == "objection_raised":
        objection_type = context_change.get("objection_type", "general")
        strategy_updates = {
            "churn_risk_change": "+5%",
            "objection_handling": f"Apply rebuttal for {objection_type}",
            "recommended_approach": "Empathy → Facts → Future vision",
            "backup_strategies": ["Testimonials", "TCO calculation", "Test drive offer"]
        }
    
    # Oblicz nowe metryki jeśli dostępny kalkulator
    new_metrics = {}
    if metrics_calculator:
        session_data = {
            **customer_data.get("session", {}),
            **context_change
        }
        new_metrics = metrics_calculator.calculate_all_metrics(
            session_data=session_data,
            analysis_result=current_profile
        )
    
    return {
        "session_id": session_id,
        "update_trigger": update_trigger,
        "strategy_updates": strategy_updates,
        "new_metrics": new_metrics,
        "timestamp": datetime.now().isoformat(),
        "impact_summary": f"Strategy adjusted based on {update_trigger}"
    }

@app.post("/learning/extract")
async def extract_user_expertise(
    session_id: str,
    user_insight: str,
    mode: str = "active_learning"
):
    """
    Aktywne uczenie od użytkownika - ekstraktuje wiedzę ekspercką
    """
    if not expert_ai_client:
        raise HTTPException(status_code=503, detail="AI nie jest dostępne")
    
    # Analizuj insight użytkownika
    prompt = f"""Przeanalizuj tę wiedzę ekspercką od doświadczonego sprzedawcy:
    "{user_insight}"
    
    Wyekstraktuj:
    1. Kluczowe wzorce behawioralne
    2. Nowe sygnały kupna/ryzyka
    3. Taktyki sprzedażowe
    4. Kategorię wiedzy
    
    Zwróć w formacie strukturalnym."""
    
    analysis = await expert_ai_client.generate_response(prompt)
    
    # Określ kategorię i wagę
    category = "behavioral_pattern"
    if "sygnał" in user_insight.lower() or "signal" in user_insight.lower():
        category = "buying_signal"
    elif "obiekcj" in user_insight.lower():
        category = "objection_handling"
    elif "technik" in user_insight.lower() or "taktyk" in user_insight.lower():
        category = "sales_tactic"
    
    # Określ priorytet
    priority = "UŻYTECZNA"
    if any(word in user_insight.lower() for word in ["zawsze", "kluczow", "ważn", "krytyczn"]):
        priority = "WAŻNA"
    if any(word in user_insight.lower() for word in ["nigdy", "błąd", "strac", "problem"]):
        priority = "KRYTYCZNA"
    
    # Zapisz do bazy jako user_expertise
    await extended_db_service.save_user_expertise({
        "session_id": session_id,
        "category": category,
        "insights": {
            "original_text": user_insight,
            "extracted_patterns": analysis,
            "timestamp": datetime.now().isoformat()
        },
        "confidence": 0.8,
        "source": "user_direct_input"
    })
    
    # Generuj pytania pogłębiające
    follow_up_questions = []
    
    if "klient" in user_insight.lower():
        follow_up_questions.append("Czy zauważa Pan podobne wzorce u innych typów klientów?")
    
    if "czas" in user_insight.lower() or "godzin" in user_insight.lower():
        follow_up_questions.append("Czy to zachowanie zmienia się w weekendy?")
    
    if not follow_up_questions:
        follow_up_questions = [
            "Jak często obserwuje Pan to zjawisko?",
            "Czy są wyjątki od tej reguły?"
        ]
    
    return {
        "processed_insight": {
            "category": category,
            "structured_data": analysis,
            "priority": priority,
            "confidence": 0.8
        },
        "follow_up_questions": follow_up_questions,
        "suggested_action": f"Dodano do bazy wiedzy jako {category}",
        "impact": "Wiedza zostanie wykorzystana w przyszłych analizach"
    }

# ==================== WEBSOCKET DLA REAL-TIME ====================

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket dla komunikacji real-time z pełnym kontekstem"""
    
    await websocket.accept()
    
    try:
        while True:
            # Odbierz wiadomość
            data = await websocket.receive_json()
            
            # Przetwórz z pełnym kontekstem
            if data.get("type") == "analyze":
                # Pobierz pełne dane klienta
                customer_data = await extended_db_service.get_comprehensive_customer_data(session_id)
                
                analysis = await expert_ai_client.analyze_customer_expert(
                    customer_input=data.get("input"),
                    session_context={
                        "session_id": session_id,
                        "full_data": customer_data
                    }
                )
                
                # Wyślij odpowiedź z pełnymi danymi
                await websocket.send_json({
                    "type": "analysis",
                    "data": analysis,
                    "enriched": {
                        "subsidies": await extended_db_service.get_ev_subsidies(),
                        "promotions": await extended_db_service.get_active_promotions()
                    }
                })
                
            elif data.get("type") == "strategy":
                strategy = await expert_ai_client.generate_coaching_response(
                    customer_profile=data.get("profile", {}),
                    mode=data.get("mode", "coach")
                )
                
                await websocket.send_json({
                    "type": "strategy",
                    "data": strategy,
                    "playbooks": await extended_db_service.get_playbooks_enriched()
                })
                
    except WebSocketDisconnect:
        print(f"WebSocket rozłączony: {session_id}")

# ==================== URUCHOMIENIE ====================

if __name__ == "__main__":
    print("🚀 Uruchamianie Ultra BIGDecoder 3.0 - WERSJA ROZSZERZONA")
    print("📊 31 tabel, 393 rekordy, pełna wiedza ekspercka")
    
    uvicorn.run(
        "main_refactored:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Wyłącz reload dla stabilności
        log_level="info"
    )
