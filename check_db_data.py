#!/usr/bin/env python3
"""Sprawdzenie rzeczywistych danych w bazie"""

import asyncio
from services.database_extended import ExtendedDatabaseService

async def main():
    print("=== SPRAWDZANIE RZECZYWISTYCH DANYCH ===")
    
    db = ExtendedDatabaseService(
        'https://viepqnimxchgoxgijaub.supabase.co',
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpZXBxbmlteGNoZ294Z2lqYXViIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDk4NjU1MywiZXhwIjoyMDcwNTYyNTUzfQ.CniELMUV7u8islNXXJuZKEtFbBVPdX4af-bmQw-q6e4'
    )
    
    # 1. ARCHETYPY
    print("\n=== ARCHETYPY ===")
    try:
        archetypes = await db.get_all_archetypes_with_aliases()
        print(f"Liczba archetypów: {len(archetypes)}")
        for i, arch in enumerate(archetypes[:3]):  # Pokaż pierwsze 3
            print(f"{i+1}. {arch.get('name', 'Unknown')}: {arch.get('description', '')[:100]}...")
            print(f"   ID: {arch.get('id')}, Kolumny: {list(arch.keys())}")
    except Exception as e:
        print(f"Błąd archetypów: {e}")
    
    # 2. DOPŁATY EV
    print("\n=== DOPŁATY EV ===")
    try:
        subsidies = await db.get_ev_subsidies()
        print(f"Liczba dopłat: {len(subsidies)}")
        for i, sub in enumerate(subsidies[:3]):
            print(f"{i+1}. {sub.get('program_name', 'Unknown')}: {sub.get('max_amount', 0)} PLN")
            print(f"   Kolumny: {list(sub.keys())}")
    except Exception as e:
        print(f"Błąd dopłat: {e}")
    
    # 3. PLAYBOOKI
    print("\n=== PLAYBOOKI ===") 
    try:
        playbooks = await db.get_playbooks_enriched()
        print(f"Liczba playbooków: {len(playbooks)}")
        for i, play in enumerate(playbooks[:3]):
            print(f"{i+1}. {play.get('name', 'Unknown')}: {play.get('strategy_type', 'Unknown')}")
            print(f"   ID: {play.get('id')}, Kolumny: {list(play.keys())}")
    except Exception as e:
        print(f"Błąd playbooków: {e}")
    
    # 4. OBIEKCJE  
    print("\n=== OBIEKCJE ===")
    try:
        objections = await db.get_objections_with_archetypes()
        print(f"Liczba obiekcji: {len(objections)}")
        for i, obj in enumerate(objections[:3]):
            print(f"{i+1}. {obj.get('type', 'Unknown')}: {obj.get('description', '')[:80]}...")
            print(f"   ID: {obj.get('id')}, Kolumny: {list(obj.keys())}")
    except Exception as e:
        print(f"Błąd obiekcji: {e}")

    # 5. TESLE
    print("\n=== PRODUKTY TESLA ===")
    try:
        teslas = await db.get_tesla_products_all()
        print(f"Liczba modeli Tesla: {len(teslas)}")
        for i, tesla in enumerate(teslas[:3]):
            print(f"{i+1}. {tesla.get('model', 'Unknown')} {tesla.get('variant', '')}: {tesla.get('price', 0)} PLN")
            print(f"   Zasięg: {tesla.get('range_km', 0)}km, Kolumny: {list(tesla.keys())}")
    except Exception as e:
        print(f"Błąd Tesla: {e}")

if __name__ == "__main__":
    asyncio.run(main())
