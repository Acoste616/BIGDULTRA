"""
Backend Services
"""

# Importy są opcjonalne - moduły mogą być importowane bezpośrednio
try:
    from .ollama_client import OllamaClient
except ImportError:
    OllamaClient = None

try:
    from .database_extended import ExtendedDatabaseService
except ImportError:
    ExtendedDatabaseService = None

__all__ = ["OllamaClient", "ExtendedDatabaseService"]
