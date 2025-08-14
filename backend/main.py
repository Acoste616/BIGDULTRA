"""
ULTRA BIGDECODER 3.0 - FastAPI Backend
Główna aplikacja API
"""
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import json
from uuid import UUID, uuid4
from typing import Dict, Any, Optional, List
from datetime import datetime

# Import konfiguracji i serwisów
from config import config
from services.ollama_client import OllamaClient
from services.database import DatabaseService
from models.schemas import (
    CustomerAnalysisRequest,
    CustomerAnalysisResponse,
    SessionCreateRequest,
    SessionResponse,
    SuggestionRequest,
    FeedbackRequest
)

# Globalne instancje
ollama_client: Optional[OllamaClient] = None
db_service: Optional[DatabaseService] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Zarządzanie cyklem życia aplikacji"""
    global ollama_client, db_service
    
    # Startup
    print("🚀 Uruchamianie Ultra BIGDecoder 3.0...")
    
    # Inicjalizacja Ollama z poprawną konfiguracją
    ollama_client = OllamaClient(
        base_url=config.OLLAMA_BASE_URL,
        api_key=config.OLLAMA_API_KEY,
        model=config.OLLAMA_MODEL
    )
    
    # Inicjalizacja bazy danych
    db_service = DatabaseService(
        url=config.SUPABASE_URL,
        key=config.SUPABASE_KEY
    )
    
    print("✅ System gotowy do pracy!")
    
    yield
    
    # Shutdown
    print("🔄 Zamykanie systemu...")
    if ollama_client:
        await ollama_client.close()
    if db_service:
        await db_service.close()
    print("👋 System zamknięty")

# Inicjalizacja FastAPI
app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    """Endpoint główny - status API"""
    return {
        "name": config.API_TITLE,
        "version": config.API_VERSION,
        "status": "operational",
        "model": config.OLLAMA_MODEL,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Sprawdzenie zdrowia systemu"""
    
    health_status = {
        "api": "healthy",
        "database": "unknown",
        "ollama": "unknown",
        "timestamp": datetime.now().isoformat()
    }
    
    # Sprawdź bazę danych
    try:
        if db_service:
            await db_service.health_check()
            health_status["database"] = "healthy"
    except:
        health_status["database"] = "unhealthy"
    
    # Sprawdź Ollama (lekki check zamiast generowania odpowiedzi)
    try:
        if ollama_client:
            is_available = await ollama_client.check_availability()
            health_status["ollama"] = "healthy" if is_available else "unhealthy"
    except:
        health_status["ollama"] = "unhealthy"
    
    # Określ ogólny status
    if "unhealthy" in health_status.values():
        return JSONResponse(status_code=503, content=health_status)
    
    return health_status

# ==================== SESJE ====================

@app.post("/sessions/create", response_model=SessionResponse)
async def create_session(request: SessionCreateRequest):
    """Tworzy nową sesję sprzedażową"""
    
    session_id = str(uuid.uuid4())
    
    # Zapisz w bazie
    session_data = {
        "session_id": session_id,
        "user_id": request.user_id,
        "metadata": request.metadata or {},
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    await db_service.create_session(session_data)
    
    return SessionResponse(
        session_id=session_id,
        created_at=session_data["created_at"],
        status="active"
    )

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Pobiera dane sesji"""
    
    session = await db_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sesja nie znaleziona")
    
    return session

# ==================== ANALIZA KLIENTA ====================

@app.post("/analyze", response_model=CustomerAnalysisResponse)
async def analyze_customer(request: CustomerAnalysisRequest):
    """
    Główny endpoint analizy klienta
    Analizuje wypowiedź i zwraca pełną strategię
    """
    
    if not ollama_client:
        raise HTTPException(status_code=503, detail="Ollama nie jest dostępna")
    
    try:
        # Pobierz kontekst sesji
        session_context = {}
        if request.session_id:
            session = await db_service.get_session(request.session_id)
            if session:
                session_context = {
                    "profile": session.get("profile", {}),
                    "history": []  # Historia przechowywana w interaction_logs
                }
        
        # Pobierz dane z bazy, aby przekazać je do AI jako kontekst
        all_archetypes = await db_service.get_all_archetypes()
        all_objections = await db_service.get_all_objections()
        all_playbooks = await db_service.get_all_playbooks()

        # Dodaj dane do kontekstu sesji
        session_context['db_data'] = {
            "archetypes": all_archetypes,
            "objections": all_objections,
            "playbooks": all_playbooks
        }
        if request.newest_input:
            session_context['newest_input'] = request.newest_input

        # Analiza przez Ollama - Używamy V2 dla lepszej jakości
        analysis = await ollama_client.analyze_customer_v2(
            customer_input=request.input_text,
            session_context=session_context
        )

        # Sprawdź czy AI zasugerowało nowy archetyp
        if analysis.get("new_archetype_suggestion"):
            suggestion = analysis["new_archetype_suggestion"]
            await db_service.create_suggestion({
                "session_id": request.session_id,
                "suggestion_type": "KRYTYCZNA",
                "priority": "Wysoki",
                "title": f"Nowy sub-archetyp: {suggestion.get('new_name')}",
                "reasoning": suggestion.get('reasoning'),
                "proposed_data": suggestion,
                "confidence_score": analysis.get("archetype", {}).get("confidence", 0.5)
            })
        
        # Pobierz dane z bazy dla wzbogacenia
        archetype_data = None
        if analysis.get("archetype", {}).get("id"):
            try:
                archetype_id = UUID(analysis["archetype"]["id"])
                archetype_data = await db_service.get_archetype(archetype_id)
            except (ValueError, TypeError):
                pass  # Ignore if ID is not a valid UUID
        
        objections_data = []
        for obj in analysis.get("objections", []):
            if obj.get("id"):
                try:
                    objection_id = UUID(obj["id"])
                    obj_data = await db_service.get_objection(objection_id)
                    if obj_data:
                        objections_data.append(obj_data)
                except (ValueError, TypeError):
                    continue
        
        playbook_data = None
        if analysis.get("strategy", {}).get("playbook_id"):
            try:
                playbook_id = UUID(analysis["strategy"]["playbook_id"])
                playbook_data = await db_service.get_playbook(playbook_id)
            except (ValueError, TypeError):
                pass
        
        # Zapisz analizę w interaction_logs
        await db_service.log_interaction({
            "session_id": request.session_id,
            "input_text": request.input_text,
            "analysis": analysis,
            "archetype_data": archetype_data,
            "objections_data": objections_data,
            "playbook_data": playbook_data,
            "timestamp": datetime.now().isoformat()
        })
        
        # Aktualizuj profil w sesji
        if request.session_id:
            await db_service.update_session_profile(
                request.session_id,
                analysis.get("archetype", {})
            )
        
        # Zbuduj strukturę zgodną z BIGDECODER.md oraz wymogami frontendu
        archetype_obj = analysis.get("archetype") or {}
        confidence = archetype_obj.get("confidence") or analysis.get("confidence") or 0.0

        # Konwersja do top3 (na razie pojedynczy wynik jako Top1)
        archetypes_top3 = []
        if archetype_obj.get("name"):
            archetypes_top3.append({
                "id": archetype_obj.get("id"),
                "name": archetype_obj.get("name"),
                "confidence": confidence
            })

        # Jeżeli brak id archetypu, nie wypełniaj pola archetype (walidacja Pydantic)
        archetype_for_schema = None
        if isinstance(archetype_obj, dict) and archetype_obj.get("id") is not None:
            archetype_for_schema = archetype_obj

        # Mapa metryk do sekcji scores używanej przez UI
        scores = {}
        if "purchase_probability" in analysis:
            # Front oczekuje procentów; backend trzyma 0..1
            try:
                scores["purchase_likelihood"] = float(analysis.get("purchase_probability", 0.0)) * 100.0
            except Exception:
                scores["purchase_likelihood"] = 0
        if "churn_risk" in analysis:
            try:
                scores["churn_risk"] = float(analysis.get("churn_risk", 0.0)) * 100.0
            except Exception:
                scores["churn_risk"] = 0

        # Przygotuj bezpieczne pola zgodne z Pydantic (unikaj niepełnych modeli)
        objections_for_schema = []
        strategy_for_schema = None

        return CustomerAnalysisResponse(
            session_id=request.session_id,
            archetype=archetype_for_schema,
            objections=objections_for_schema,
            strategy=strategy_for_schema,
            questions=analysis.get("questions", []),
            purchase_probability=analysis.get("purchase_probability", 0.0),
            next_actions=analysis.get("next_actions", []),
            enriched_data={
                "archetype_details": archetype_data,
                "objections_details": objections_data,
                "playbook_details": playbook_data
            },
            confidence_score=confidence,
            quick_reply=analysis.get("response") or analysis.get("quick_reply"),
            deep_questions=analysis.get("questions") or analysis.get("deep_questions"),
            archetypes_top3=archetypes_top3 or None,
            scores=scores or None
        )
        
    except Exception as e:
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
    """Generuje strategię sprzedażową"""
    
    # Pobierz profil klienta
    session = await db_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sesja nie znaleziona")
    
    profile = session.get("profile", {})
    last_objection = session.get("last_objection")
    
    # Generuj strategię
    strategy = await ollama_client.generate_response(
        customer_profile=profile,
        objection=last_objection,
        mode=mode
    )
    
    return {
        "session_id": session_id,
        "mode": mode,
        "strategy": strategy,
        "timestamp": datetime.now().isoformat()
    }

# ==================== SUGESTIE I FEEDBACK ====================

@app.post("/suggestions/create")
async def create_suggestion(request: SuggestionRequest):
    """Tworzy sugestię AI dla użytkownika"""
    
    suggestion_data = {
        "session_id": request.session_id,
        "suggestion_type": request.suggestion_type,
        "priority": request.priority,
        "title": request.title,
        "reasoning": request.reasoning,
        "proposed_data": request.proposed_data,
        "confidence_score": request.confidence_score
    }
    
    result = await db_service.create_suggestion(suggestion_data)
    
    return {
        "success": True,
        "suggestion_id": result.get("id"),
        "message": "Sugestia utworzona"
    }

@app.post("/feedback/submit")
async def submit_feedback(request: FeedbackRequest):
    """Przyjmuje feedback użytkownika"""
    
    feedback_data = {
        "session_id": request.session_id,
        "feedback_type": request.feedback_type,
        "content": request.content,
        "rating": request.rating,
        "metadata": request.metadata
    }
    
    await db_service.save_feedback(feedback_data)
    
    # Jeśli to korekta, zaktualizuj model
    if request.feedback_type == "correction":
        await db_service.save_to_user_expertise({
            "session_id": request.session_id,
            "knowledge_category": "user_correction",
            "extracted_insights": {
                "original": request.metadata.get("original"),
                "corrected": request.content
            },
            "confidence_score": 1.0
        })
    
    return {
        "success": True,
        "message": "Feedback zapisany"
    }

# ==================== DANE I STATYSTYKI ====================

@app.get("/data/archetypes")
async def get_archetypes():
    """Pobiera listę archetypów"""
    archetypes = await db_service.get_all_archetypes()
    return {"archetypes": archetypes}

@app.get("/data/objections")
async def get_objections():
    """Pobiera listę obiekcji"""
    objections = await db_service.get_all_objections()
    return {"objections": objections}

@app.get("/data/playbooks")
async def get_playbooks():
    """Pobiera listę playbooków"""
    playbooks = await db_service.get_all_playbooks()
    return {"playbooks": playbooks}

@app.get("/data/products/tesla")
async def get_tesla_products():
    """Pobiera produkty Tesla"""
    products = await db_service.get_tesla_products()
    return {"products": products}

@app.get("/data/products/competitors")
async def get_competitor_products():
    """Pobiera produkty konkurencji"""
    products = await db_service.get_competitor_products()
    return {"products": products}

@app.get("/data/market-data")
async def get_market_data():
    """Pobiera dane rynkowe"""
    market_data = await db_service.get_market_data()
    return {"market_data": market_data}

@app.get("/data/promotions")
async def get_promotions():
    """Pobiera aktywne promocje"""
    promotions = await db_service.get_promotions()
    return {"promotions": promotions}

@app.get("/data/seasonal-patterns")
async def get_seasonal_patterns():
    """Pobiera wzorce sezonowe"""
    patterns = await db_service.get_seasonal_patterns()
    return {"seasonal_patterns": patterns}

@app.get("/data/buying-signals")
async def get_buying_signals():
    """Pobiera sygnały kupna"""
    signals = await db_service.get_buying_signals()
    return {"buying_signals": signals}

@app.get("/data/scoring-config")
async def get_scoring_config():
    """Pobiera aktywną konfigurację scoringu"""
    config = await db_service.get_scoring_config()
    if not config:
        raise HTTPException(status_code=404, detail="Aktywna konfiguracja scoringu nie znaleziona")
    return {"scoring_config": config}

@app.get("/stats/dashboard")
async def get_dashboard_stats():
    """Pobiera statystyki dla dashboardu"""
    
    stats = await db_service.get_statistics()
    
    return {
        "total_sessions": stats.get("total_sessions", 0),
        "active_sessions": stats.get("active_sessions", 0),
        "total_interactions": stats.get("total_interactions", 0),
        "average_confidence": stats.get("average_confidence", 0),
        "top_archetypes": stats.get("top_archetypes", []),
        "top_objections": stats.get("top_objections", []),
        "conversion_rate": stats.get("conversion_rate", 0),
        "timestamp": datetime.now().isoformat()
    }

# ==================== WEBSOCKET DLA REAL-TIME ====================

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket dla komunikacji real-time"""
    
    await websocket.accept()
    
    try:
        while True:
            # Odbierz wiadomość
            data = await websocket.receive_json()
            
            # Przetwórz
            if data.get("type") == "analyze":
                analysis = await ollama_client.analyze_customer(
                    customer_input=data.get("input"),
                    session_context={"session_id": session_id}
                )
                
                # Wyślij odpowiedź
                await websocket.send_json({
                    "type": "analysis",
                    "data": analysis
                })
                
            elif data.get("type") == "strategy":
                strategy = await ollama_client.generate_response(
                    customer_profile=data.get("profile", {}),
                    mode=data.get("mode", "coach")
                )
                
                await websocket.send_json({
                    "type": "strategy",
                    "data": strategy
                })
                
    except WebSocketDisconnect:
        print(f"WebSocket rozłączony: {session_id}")

# ==================== URUCHOMIENIE ====================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
