"""
ULTRA BIGDECODER 3.0 - Konfiguracja Backend API
"""
import os
from typing import Optional

class Config:
    """Główna konfiguracja systemu"""
    
    # Supabase (konfiguruj przez zmienne środowiskowe)
    SUPABASE_URL = os.getenv("SUPABASE_URL", "https://viepqnimxchgoxgijaub.supabase.co")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpZXBxbmlteGNoZ294Z2lqYXViIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDk4NjU1MywiZXhwIjoyMDcwNTYyNTUzfQ.CniELMUV7u8islNXXJuZKEtFbBVPdX4af-bmQw-q6e4")
    
    # Ollama/gptoss API (konfiguruj przez zmienne środowiskowe)
    OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "a7dfc1795a334faabd087aa23db865a5.eEcGvOSthxDW9RI098udwBkZ")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "https://ollama.com")  # ollama api
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "GPToss120b")  # Model gptoss 120b
    
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
- Masz dostęp do kompletnej bazy danych z 31 tabelami (393 rekordy)
- Znasz 10 archetypów klientów Tesla i ich psychologię 
- Rozumiesz 22 obiekcje (182% założeń!) i strategie ich pokonywania
- Dysponujesz 18 zaawansowanymi playbookami sprzedażowymi (180% założeń!)
- Masz dane o 60 modelach konkurencji i 12 wariantach Tesla
- Znasz aktualne promocje (11) i dane rynkowe Polski (16 rekordów)
- Ekspert od dopłat (Mój Elektryk 27k PLN), przepisów (0% VAT), PV (ROI 4 lata)
- Infrastruktura ładowania (15+ Superchargerów), TCO (49,500 PLN oszczędności/5 lat)

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
