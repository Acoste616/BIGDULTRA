#!/usr/bin/env python3
"""
ULTRA BIGDECODER 3.0 - Skrypt uruchomieniowy
"""
import sys
import os
from pathlib import Path

# Dodaj ścieżkę do backendu
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    # Ustaw zmienne środowiskowe jeśli nie ma .env i nie są ustawione w środowisku
    if not os.path.exists(".env"):
        print("⚠️ Brak pliku .env - sprawdzam zmienne środowiskowe...")
        if "SUPABASE_URL" not in os.environ:
            os.environ["SUPABASE_URL"] = "https://idcwfdhpjgtpvuvbpfvp.supabase.co"
        if "SUPABASE_KEY" not in os.environ:
            os.environ["SUPABASE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlkY3dmZGhwamd0cHZ1dmJwZnZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQwMTQzMDcsImV4cCI6MjA0OTU5MDMwN30.RM9iyaZFJdztGUMXq2MQW8W1b37AcW4p9EJ8hAMmPYE"
        if "OLLAMA_API_KEY" not in os.environ:
            os.environ["OLLAMA_API_KEY"] = "44f238f9fd6f4c4f9048fce51c52d45e.0AFg36FTByB3_Oc9KcpNqWQW"
        if "OLLAMA_BASE_URL" not in os.environ:
            os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                  ULTRA BIGDECODER 3.0                        ║
║              Inteligentny Asystent Sprzedaży Tesla           ║
╚══════════════════════════════════════════════════════════════╝

🚀 Uruchamianie systemu...
    """)
    
    import uvicorn
    
    # Konfiguracja
    config = {
        "app": "main:app",
        "host": "0.0.0.0",
        "port": 8000,
        "reload": True,
        "log_level": "info"
    }
    
    # Tryb produkcyjny jeśli podano argument
    if len(sys.argv) > 1 and sys.argv[1] == "production":
        print("🏭 Tryb produkcyjny")
        config["reload"] = False
        config["workers"] = 4
        config["log_level"] = "warning"
    else:
        print("🔧 Tryb developerski")
    
    print(f"""
📡 API będzie dostępne pod:
   - http://localhost:8000
   - http://localhost:8000/docs (Swagger UI)
   - http://localhost:8000/redoc (ReDoc)

🔌 WebSocket endpoint:
   - ws://localhost:8000/ws/{{session_id}}

Naciśnij Ctrl+C aby zatrzymać serwer
    """)
    
    # Uruchom serwer
    uvicorn.run(**config)
