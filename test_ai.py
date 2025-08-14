import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.config import config
from backend.services.ai.expert_ollama_client import ExpertOllamaClient
import asyncio
import json

# Mock dla ExtendedDatabaseService
class MockDatabaseService:
    async def get_all_archetypes_with_aliases(self):
        return [{"id": "1", "name": "Test Archetype", "description": "Test"}]
    
    async def get_objections_with_archetypes(self):
        return [{"id": "1", "name": "Test Objection", "description": "Test"}]
    
    async def get_playbooks_enriched(self):
        return [{"id": "1", "name": "Test Playbook", "description": "Test"}]
    
    async def get_tesla_products_all(self):
        return [{"id": "1", "model_name": "Model Y", "variant": "RWD"}]
    
    async def get_competitors_all(self):
        return [{"id": "1", "name": "BMW iX", "category": "SUV"}]
    
    async def get_market_data_poland(self):
        return [{"id": "1", "region": "Poland", "data": "Test"}]
    
    async def get_active_promotions(self):
        return [{"id": "1", "name": "Test Promotion", "discount": "10%"}]
    
    async def get_seasonal_patterns(self):
        return [{"id": "1", "season": "Winter", "pattern": "Test"}]
    
    async def get_ev_subsidies(self):
        return [{"id": "1", "program_name": "Mój Elektryk", "max_amount_pln": 27000}]
    
    async def get_tax_regulations(self):
        return [{"id": "1", "regulation": "VAT", "rate": 0}]
    
    async def get_solar_panels_compatibility(self):
        return [{"id": "1", "compatibility": "Full", "daily_range": "40-60km"}]
    
    async def get_charging_infrastructure(self):
        return [{"id": "1", "type": "Supercharger", "count": 15}]
    
    async def get_company_fleet_benefits(self):
        return [{"id": "1", "benefit": "Tax", "value": "100%"}]
    
    async def get_leasing_params(self):
        return [{"id": "1", "type": "Leasing", "rate": "5%"}]
    
    async def get_insurance_providers(self):
        return [{"id": "1", "provider": "Test", "coverage": "Full"}]
    
    async def get_service_network(self):
        return [{"id": "1", "location": "Warsaw", "services": "Full"}]
    
    async def get_winter_performance(self):
        return [{"id": "1", "condition": "Winter", "range_loss": "20-30%"}]
    
    async def get_tco_templates(self):
        return [{"id": "1", "template": "5_year", "savings": "49,500 PLN"}]
    
    async def get_scoring_config(self):
        return {"confidence_threshold": 0.8, "buying_signals": ["test"]}
    
    async def get_comprehensive_customer_data(self, session_id):
        return {"session": {"profile": {}}, "interactions": [], "psychometric_profiles": [], "temporal_patterns": [], "total_interactions": 0}
    
    async def detect_buying_signals(self, text):
        return ["test_signal"]

async def debug_analysis():
    print("🔍 Testowanie połączenia z AI API...")
    print(f"   Base URL: {config.OLLAMA_BASE_URL}")
    print(f"   Model: {config.OLLAMA_MODEL}")
    print(f"   API Key: {config.OLLAMA_API_KEY[:20]}...")
    
    # Użyj mock database service
    mock_db = MockDatabaseService()
    
    client = ExpertOllamaClient(
        base_url=config.OLLAMA_BASE_URL, 
        api_key=config.OLLAMA_API_KEY, 
        model=config.OLLAMA_MODEL,
        db_service=mock_db
    )
    
    print("\n1. Inicjalizacja wiedzy eksperckiej...")
    try:
        await client.initialize_expert_knowledge()
        print("   ✅ Wiedza ekspercka załadowana")
    except Exception as e:
        print(f"   ❌ Błąd inicjalizacji: {e}")
        return
    
    print("\n2. Test analizy klienta...")
    try:
        result = await client.analyze_customer_expert(
            customer_input="Chce Tesla ale martwie sie o zasieg w zimie",
            session_context={"session_id": "test_session"}
        )
        print(f"   ✅ Analiza klienta OK")
        print(f"   📊 Wynik: {json.dumps(result, ensure_ascii=False, indent=2)[:500]}...")
    except Exception as e:
        print(f"   ❌ Błąd analizy: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_analysis())
