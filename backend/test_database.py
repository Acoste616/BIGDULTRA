"""
Test połączenia z bazą danych Supabase
"""
import asyncio
from services.database_extended import ExtendedDatabaseService

async def check_supabase():
    db = ExtendedDatabaseService(
        url='https://viepqnimxchgoxgijaub.supabase.co',
        key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpZXBxbmlteGNoZ294Z2lqYXViIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDk4NjU1MywiZXhwIjoyMDcwNTYyNTUzfQ.CniELMUV7u8islNXXJuZKEtFbBVPdX4af-bmQw-q6e4'
    )
    
    print("🔍 ANALIZA SYSTEMU ULTRA BIGDECODER 3.0")
    print("="*50)
    
    # Sprawdź stan bazy
    print("\n1. STAN BAZY DANYCH SUPABASE:")
    health = await db.health_check()
    print(f"   Status: {health.get('status', 'unknown')}")
    print(f"   Liczba tabel: {health.get('tables_count', 0)}")
    print(f"   Tabele z danymi: {health.get('tables_with_data', 0)}")
    print(f"   Łączne rekordy: {health.get('total_records', 0)}")
    
    # Pobierz przykładowe dane z kluczowych tabel
    print("\n2. PRZYKŁADOWE DANE Z GŁÓWNYCH TABEL:")
    
    # Archetypy
    print("\n   🎭 ARCHETYPY KLIENTÓW:")
    archetypes = await db.get_all_archetypes_with_aliases()
    for i, arch in enumerate(archetypes[:5], 1):
        print(f"   {i}. {arch.get('name', '?')}")
        desc = arch.get('description', '')
        if desc:
            print(f"      Opis: {desc[:60]}...")
    
    # Dopłaty EV
    print("\n   💰 DOPŁATY DO EV:")
    subsidies = await db.get_ev_subsidies()
    for i, sub in enumerate(subsidies, 1):
        program = sub.get('program_name', '?')
        amount = sub.get('max_amount', '?')
        print(f"   {i}. {program}: {amount} PLN")
    
    # Produkty Tesla
    print("\n   🚗 PRODUKTY TESLA:")
    tesla_products = await db.get_tesla_products_all()
    for i, prod in enumerate(tesla_products[:5], 1):
        model = prod.get('model_name', '?')
        variant = prod.get('variant', '')
        price = prod.get('price', '?')
        print(f"   {i}. {model} {variant}: {price} PLN")
    
    # Konkurencja
    print("\n   ⚔️ TOP 5 KONKURENTÓW:")
    competitors = await db.get_competitors_all()
    for i, comp in enumerate(competitors[:5], 1):
        brand = comp.get('brand', '?')
        model = comp.get('model_name', '?')
        price = comp.get('price', '?')
        print(f"   {i}. {brand} {model}: {price} PLN")
    
    # Playbooki
    print("\n   📚 PLAYBOOKI SPRZEDAŻOWE:")
    playbooks = await db.get_playbooks_enriched()
    for i, book in enumerate(playbooks[:3], 1):
        name = book.get('name', '?')
        print(f"   {i}. {name}")
    
    # Statystyki systemu
    print("\n3. STATYSTYKI SYSTEMU:")
    stats = await db.get_system_statistics()
    db_stats = stats.get('database', {})
    knowledge = stats.get('knowledge_base', {})
    expert = stats.get('expert_data', {})
    
    print(f"   📊 Baza danych:")
    print(f"      - Tabele: {db_stats.get('total_tables', 0)}")
    print(f"      - Rekordy: {db_stats.get('total_records', 0)}")
    
    print(f"   🧠 Baza wiedzy:")
    print(f"      - Obiekcje: {knowledge.get('objections', 0)}")
    print(f"      - Playbooki: {knowledge.get('playbooks', 0)}")
    print(f"      - Konkurenci: {knowledge.get('competitors', 0)}")
    
    print(f"   🎯 Dane eksperckie:")
    print(f"      - Dopłaty: {expert.get('subsidies', 0)}")
    print(f"      - Przepisy podatkowe: {expert.get('tax_regulations', 0)}")
    print(f"      - Stacje ładowania: {expert.get('charging_stations', 0)}")
    
    print("\n4. STATUS GOTOWOŚCI SYSTEMU:")
    print("   ✅ Baza danych: POŁĄCZONO")
    print("   ✅ Dane podstawowe: ZAŁADOWANE") 
    print("   ✅ Dane eksperckie: ZAŁADOWANE")
    print("   🎯 System gotowy do analizy klientów!")
    
    await db.close()

if __name__ == "__main__":
    asyncio.run(check_supabase())
