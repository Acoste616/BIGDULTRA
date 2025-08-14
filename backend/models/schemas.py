"""
ULTRA BIGDECODER 3.0 - Modele danych (Pydantic)
Schematy dla API requests/responses
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# ==================== ENUMS ====================

class SuggestionType(str, Enum):
    KRYTYCZNA = "KRYTYCZNA"
    WAŻNA = "WAŻNA"
    UŻYTECZNA = "UŻYTECZNA"

class FeedbackType(str, Enum):
    CORRECTION = "correction"
    RATING = "rating"
    COMMENT = "comment"
    BUG_REPORT = "bug_report"

class SessionStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class AnalysisMode(str, Enum):
    ANALYZER = "analyzer"
    COACH = "coach"
    CLIENT_SIMULATOR = "client_simulator"
    HYBRID = "hybrid"
    CONTINUOUS = "continuous"  # Ciągła analiza po każdym wpisie

# ==================== REQUEST MODELS ====================

class SessionCreateRequest(BaseModel):
    """Request tworzenia nowej sesji"""
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    initial_context: Optional[str] = None

class CustomerAnalysisRequest(BaseModel):
    """Request analizy wypowiedzi klienta"""
    session_id: Optional[str] = None
    input_text: str = Field(..., min_length=1, max_length=5000)
    mode: AnalysisMode = AnalysisMode.ANALYZER
    include_enriched_data: bool = True
    
    @validator('input_text')
    def validate_input(cls, v):
        if not v.strip():
            raise ValueError("Input nie może być pusty")
        return v.strip()

class SuggestionRequest(BaseModel):
    """Request utworzenia sugestii AI"""
    session_id: str
    suggestion_type: SuggestionType
    priority: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=200)
    reasoning: str
    proposed_data: Optional[Dict[str, Any]] = None
    confidence_score: float = Field(..., ge=0.0, le=1.0)

class FeedbackRequest(BaseModel):
    """Request przesłania feedbacku"""
    session_id: str
    feedback_type: FeedbackType
    content: str = Field(..., min_length=1)
    rating: Optional[int] = Field(None, ge=1, le=5)
    metadata: Optional[Dict[str, Any]] = None

class StrategyGenerateRequest(BaseModel):
    """Request generowania strategii"""
    session_id: str
    mode: AnalysisMode = AnalysisMode.COACH
    context: Optional[Dict[str, Any]] = None
    focus_areas: Optional[List[str]] = None

class QuestionAnswerRequest(BaseModel):
    """ULTRA 3.0: Request odpowiedzi na pytanie priorytetowe"""
    session_id: str
    question_text: str = Field(..., min_length=5, max_length=200)
    answer_text: str = Field(..., min_length=1, max_length=1000)
    was_critical: bool = Field(False, description="Czy to było pytanie critical")
    
    @validator('answer_text')
    def validate_answer(cls, v):
        if not v.strip():
            raise ValueError("Odpowiedź nie może być pusta")
        return v.strip()

# ==================== ULTRA 3.0 MODELS ====================

class PriorityQuestion(BaseModel):
    """ULTRA 3.0: Pytanie z priorytetem i flagą critical"""
    text: str = Field(..., min_length=5, max_length=200)
    critical: bool = Field(False, description="True jeśli pytanie jest kluczowe dla analizy (confidence < 0.7)")
    reason: str = Field(..., min_length=5, max_length=500, description="Powód zadania pytania")
    
    @validator('text')
    def validate_question_text(cls, v):
        if not v.strip().endswith('?'):
            return v.strip() + '?'
        return v.strip()

# ==================== RESPONSE MODELS ====================

class SessionResponse(BaseModel):
    """Response z danymi sesji"""
    session_id: str
    created_at: str
    status: SessionStatus
    metadata: Optional[Dict[str, Any]] = None

class ArchetypeInfo(BaseModel):
    """Informacje o archetypie"""
    id: int
    name: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    description: Optional[str] = None
    key_traits: Optional[List[str]] = None

class ObjectionInfo(BaseModel):
    """Informacje o obiekcji"""
    id: int
    type: str
    text: str
    hidden: bool = False
    severity: Optional[str] = None
    rebuttal_strategy: Optional[Dict[str, Any]] = None

class StrategyInfo(BaseModel):
    """Informacje o strategii"""
    playbook_id: int
    approach: str
    key_points: List[str]
    estimated_effectiveness: Optional[float] = None
    alternative_approaches: Optional[List[str]] = None

class CustomerAnalysisResponse(BaseModel):
    """ULTRA 3.0: Response z analizą klienta - separacja mechanizmów"""
    session_id: Optional[str]
    archetype: Optional[ArchetypeInfo]
    objections: List[ObjectionInfo] = []
    strategy: Optional[StrategyInfo]
    questions: List[str] = []  # Backward compatibility
    purchase_probability: float = Field(0.0, ge=0.0, le=1.0)
    next_actions: List[str] = []
    enriched_data: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None
    confidence_score: Optional[float] = None
    
    # ULTRA 3.0: Nowe pola z separacją mechanizmów
    client_response: Optional[str] = Field(None, description="Bezpośrednia odpowiedź DO KLIENTA na ostatnią wiadomość")
    quick_reply: Optional[str] = Field(None, description="Coaching DLA SPRZEDAWCY - jak prowadzić, co podkreślić")
    priority_questions: Optional[List[PriorityQuestion]] = Field(default_factory=list, description="Pytania z priorytetem i flagą critical")
    
    # Pola backward compatibility
    deep_questions: Optional[List[str]] = None
    archetypes_top3: Optional[List[Dict[str, Any]]] = None
    scores: Optional[Dict[str, Any]] = None
    
    # ULTRA 3.0: Metadane
    ultra3_version: Optional[bool] = Field(True, description="Oznacza że używa architektury Ultra 3.0")
    history_entries: Optional[int] = Field(0, description="Liczba wpisów w historii konwersacji")
    
    @validator('client_response')
    def validate_client_response(cls, v):
        if v and len(v.strip()) < 10:
            raise ValueError("client_response musi mieć co najmniej 10 znaków")
        return v.strip() if v else v
    
    @validator('priority_questions')
    def validate_priority_questions(cls, v):
        if v and len(v) > 5:
            raise ValueError("Maksymalnie 5 pytań priorytetowych")
        return v

class DashboardStats(BaseModel):
    """Statystyki dla dashboardu"""
    total_sessions: int = 0
    active_sessions: int = 0
    total_interactions: int = 0
    average_confidence: float = 0.0
    top_archetypes: List[Dict[str, Any]] = []
    top_objections: List[Dict[str, Any]] = []
    conversion_rate: float = 0.0
    timestamp: str

# ==================== DATABASE MODELS ====================

class Archetype(BaseModel):
    """Model archetypu z bazy"""
    id: int
    name: str
    description: str
    key_traits: List[str]
    communication_style: Dict[str, Any]
    decision_factors: List[str]
    typical_objections: List[int]

class Objection(BaseModel):
    """Model obiekcji z bazy"""
    id: int
    name: str
    description: str
    category: str
    severity: str
    rebuttal_strategy: Dict[str, Any]

class Playbook(BaseModel):
    """Model playbooka z bazy"""
    id: int
    name: str
    target_archetype_id: Optional[int]
    target_objection_id: Optional[int]
    strategy_type: str
    strategy_details: Dict[str, Any]
    success_rate: Optional[float]

class Product(BaseModel):
    """Model produktu"""
    id: int
    brand: str
    model_name: str
    variant: Optional[str]
    price_pln: Optional[float]
    range_km: Optional[int]
    acceleration_0_100: Optional[float]
    top_speed: Optional[int]
    battery_kwh: Optional[float]
    availability: Optional[str]

# ==================== WEBSOCKET MODELS ====================

class WSMessage(BaseModel):
    """Wiadomość WebSocket"""
    type: str
    session_id: Optional[str]
    data: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class WSAnalysisRequest(BaseModel):
    """Request analizy przez WebSocket"""
    type: str = "analyze"
    input: str
    context: Optional[Dict[str, Any]] = None

class WSAnalysisResponse(BaseModel):
    """Response analizy przez WebSocket"""
    type: str = "analysis"
    data: CustomerAnalysisResponse
    
class WSStrategyRequest(BaseModel):
    """Request strategii przez WebSocket"""
    type: str = "strategy"
    profile: Dict[str, Any]
    mode: AnalysisMode = AnalysisMode.COACH

class WSStrategyResponse(BaseModel):
    """Response strategii przez WebSocket"""
    type: str = "strategy"
    data: str

# ==================== ERROR MODELS ====================

class ErrorResponse(BaseModel):
    """Model błędu API"""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class ValidationErrorResponse(BaseModel):
    """Model błędu walidacji"""
    error: str = "validation_error"
    message: str
    field_errors: Dict[str, List[str]]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
