"""
ULTRA BIGDECODER 3.0 - Konfiguracja Backend API
"""
import os
from typing import Optional

class Config:
    """Główna konfiguracja systemu"""
    
    # Supabase (konfiguruj przez zmienne środowiskowe)
    SUPABASE_URL = os.getenv("SUPABASE_URL", "https://YOUR-PROJECT.supabase.co")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    
    # Ollama API (konfiguruj przez zmienne środowiskowe)
    OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = "gptoss120b"  # Model GPT OSS 120B
    
    # Model Parameters
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_TOP_P = 0.9
    DEFAULT_TOP_K = 40
    DEFAULT_MAX_TOKENS = 4096
    
    # API Settings
    API_VERSION = "3.0"
    API_TITLE = "Ultra BIGDecoder API"
    API_DESCRIPTION = "Inteligentny asystent sprzedaży Tesla z aktywnym uczeniem"
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "ultra-bigdecoder-secret-key-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    
    # CORS
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8000",
        "*"  # W produkcji zmień na konkretne domeny
    ]
    
    # System Prompts
    SYSTEM_PROMPT_BASE = """
Jesteś Ultra BIGDecoder 3.0 - zaawansowanym asystentem sprzedaży Tesla w Polsce.

TWOJE MOŻLIWOŚCI:
- Masz dostęp do kompletnej bazy danych z 20 tabelami
- Znasz 10 archetypów klientów Tesla i ich psychologię
- Rozumiesz 12 głównych obiekcji i strategie ich pokonywania
- Dysponujesz 10 zaawansowanymi playbookami sprzedażowymi
- Masz dane o 53 modelach konkurencji i 12 wariantach Tesla
- Znasz aktualne promocje i dane rynkowe Polski

ZASADY DZIAŁANIA:
1. CIĄGŁA ANALIZA - analizujesz każdą wypowiedź w kontekście całej sesji
2. EWOLUCJA PROFILU - profil klienta dynamicznie ewoluuje z każdą informacją
3. PROAKTYWNE DOPYTYWANIE - gdy confidence < 0.8, zadajesz pytania pogłębiające
4. MOCNE SUGESTIE - wykrywasz luki i proponujesz konkretne rozwiązania
5. UCZENIE SIĘ - zapisujesz korekty użytkownika i adaptujesz strategię

TRYBY PRACY:
- ANALYZER: Analizujesz zachowania i aktualizujesz profil klienta
- COACH: Podpowiadasz najlepsze strategie sprzedawcy
- CLIENT_SIMULATOR: Wcielasz się w określony archetyp dla treningu
- HYBRID: Łączysz wszystkie tryby dla maksymalnej efektywności

JĘZYK:
- Używaj polskiego, chyba że klient preferuje inny język
- Dostosuj styl komunikacji do archetypu klienta
- Unikaj żargonu technicznego, chyba że klient go używa
"""

    # Confidence Thresholds
    HIGH_CONFIDENCE = 0.8
    MEDIUM_CONFIDENCE = 0.6
    LOW_CONFIDENCE = 0.4
    
    # Cache Settings
    CACHE_TTL = 300  # 5 minut
    CACHE_MAX_SIZE = 100
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = 60  # sekundy
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

config = Config()
