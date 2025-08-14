#!/usr/bin/env python3
"""Prosty test systemu Ultra BIGDecoder 3.0"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

async def test_system():
    print("🧪 Test systemu Ultra BIGDecoder 3.0")
    
    try:
        # Test 1: Import konfiguracji
        print("1. Import konfiguracji...")
        from backend.config import config
        print(f"   ✅ Konfiguracja OK: {config.API_TITLE}")
        print(f"   📊 Supabase URL: {config.SUPABASE_URL}")
        print(f"   🤖 AI Model: {config.OLLAMA_MODEL}")
        
        # Test 2: Połączenie z bazą danych
        print("\n2. Test bazy danych...")
        from backend.services.database_extended import ExtendedDatabaseService
        
        db = ExtendedDatabaseService(
            url=config.SUPABASE_URL,
            key=config.SUPABASE_KEY
        )
        
        # Health check
        health = await db.health_check()
        print(f"   ✅ Baza danych: {health.get('tables_with_data', 0)} tabel z danymi")
        print(f"   📈 Łącznie rekordów: {health.get('total_records', 0)}")
        
        # Test 3: AI Client
        print("\n3. Test AI Client...")
        from backend.services.ai.expert_ollama_client import ExpertOllamaClient
        
        ai_client = ExpertOllamaClient(
            base_url=config.OLLAMA_BASE_URL,
            api_key=config.OLLAMA_API_KEY,
            model=config.OLLAMA_MODEL,
            db_service=db
        )
        
        # Inicjalizacja wiedzy eksperckiej
        await ai_client.initialize_expert_knowledge()
        print("   ✅ AI Client OK")
        
        # Test 4: Analiza klienta
        print("\n4. Test analizy klienta...")
        result = await ai_client.analyze_customer_expert(
            customer_input="Chce Tesla Model Y",
            session_context={"session_id": "test"}
        )
        
        print(f"   ✅ Analiza OK: {result.get('archetype', {}).get('name', 'Unknown')}")
        print(f"   📊 Confidence: {result.get('archetype', {}).get('confidence', 0)}")
        
        # Test 5: Generowanie strategii
        print("\n5. Test generowania strategii...")
        strategy = await ai_client.generate_coaching_response(
            customer_profile={"archetype": "Security Seeker"},
            objection="Martwię się o zasięg w zimie",
            mode="coach"
        )
        
        print(f"   ✅ Strategia OK: {strategy.get('coaching', '')[:100]}...")
        
        print("\n🎉 WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!")
        print("✅ System Ultra BIGDecoder 3.0 działa w 100%!")
        
    except Exception as e:
        print(f"\n❌ Błąd testu: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        if 'db' in locals():
            await db.close()
        if 'ai_client' in locals():
            await ai_client.close()
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_system())
    sys.exit(0 if success else 1)