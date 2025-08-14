"""
Skrypt do sprawdzenia rzeczywistego stanu danych w Supabase
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from supabase import create_client
import json
from datetime import datetime

# Konfiguracja z backend/config.py
SUPABASE_URL = "https://viepqnimxchgoxgijaub.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpZXBxbmlteGNoZ294Z2lqYXViIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDk4NjU1MywiZXhwIjoyMDcwNTYyNTUzfQ.CniELMUV7u8islNXXJuZKEtFbBVPdX4af-bmQw-q6e4"

def check_database():
    """Sprawdza stan wszystkich tabel w bazie"""
    
    print("🔍 SPRAWDZANIE STANU BAZY DANYCH SUPABASE")
    print("=" * 60)
    
    try:
        # Połączenie z Supabase
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Połączono z Supabase\n")
        
        # Lista tabel do sprawdzenia
        tables_to_check = [
            # Tabele podstawowe
            'archetypes',
            'objections', 
            'playbooks',
            'products_tesla',
            'products_competitors',
            'market_data_poland',
            'promotions',
            'seasonal_patterns',
            'objection_archetypes',
            
            # Tabele eksperckie
            'ev_subsidies_poland',
            'tax_regulations_business',
            'solar_panels_compatibility',
            'charging_infrastructure_pl',
            'company_fleet_benefits',
            'leasing_calculator_params',
            'insurance_providers_ev',
            'service_network_tesla',
            'winter_performance_data',
            'tco_calculation_templates',
            
            # Tabele dynamiczne
            'session_metadata',
            'interaction_logs',
            'analysis_feedback',
            'dynamic_context',
            'psychometric_profiles',
            'llm_suggestions',
            'user_expertise',
            'data_updates_log',
            'scoring_config',
            'buying_signals',
            'temporal_behavior_patterns'
        ]
        
        results = {}
        total_records = 0
        
        print("📊 STAN TABEL:\n")
        
        for table in tables_to_check:
            try:
                # Pobierz dane z tabeli
                response = client.table(table).select("*").execute()
                count = len(response.data) if response.data else 0
                results[table] = {
                    'count': count,
                    'exists': True,
                    'sample': response.data[0] if response.data else None
                }
                total_records += count
                
                # Wyświetl status
                status = "✅" if count > 0 else "⚠️"
                print(f"{status} {table:30} | {count:4} rekordów")
                
                # Dla tabel z danymi, pokaż przykład
                if count > 0 and response.data:
                    sample = response.data[0]
                    if 'name' in sample:
                        print(f"   └─ Przykład: {sample.get('name', '')}")
                    elif 'program_name' in sample:
                        print(f"   └─ Przykład: {sample.get('program_name', '')}")
                    elif 'model_name' in sample:
                        print(f"   └─ Przykład: {sample.get('model_name', '')}")
                        
            except Exception as e:
                results[table] = {
                    'count': 0,
                    'exists': False,
                    'error': str(e)
                }
                print(f"❌ {table:30} | Błąd: {str(e)[:50]}")
        
        print("\n" + "=" * 60)
        print(f"📈 PODSUMOWANIE:")
        print(f"   - Sprawdzonych tabel: {len(tables_to_check)}")
        print(f"   - Tabel z danymi: {sum(1 for r in results.values() if r['count'] > 0)}")
        print(f"   - Łączna liczba rekordów: {total_records}")
        
        # Sprawdź krytyczne tabele
        print("\n🔴 KRYTYCZNE TABELE:")
        critical_tables = ['archetypes', 'objections', 'playbooks', 'products_tesla']
        for table in critical_tables:
            if table in results:
                count = results[table]['count']
                if count == 0:
                    print(f"   ❌ {table} - BRAK DANYCH!")
                else:
                    print(f"   ✅ {table} - {count} rekordów")
        
        # Zapisz raport
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tables': len(tables_to_check),
            'total_records': total_records,
            'details': results
        }
        
        with open('database/supabase_data_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print("\n✅ Raport zapisany w database/supabase_data_report.json")
        
        # Szczegółowa analiza archetypów jeśli istnieją
        if results.get('archetypes', {}).get('count', 0) > 0:
            print("\n📋 ARCHETYPY W BAZIE:")
            archetypes = client.table('archetypes').select("*").execute()
            for arch in archetypes.data[:5]:  # Pokaż pierwsze 5
                print(f"   - {arch.get('name', 'N/A')}: {arch.get('description', '')[:50]}...")
        
        return results
        
    except Exception as e:
        print(f"\n❌ BŁĄD POŁĄCZENIA: {e}")
        print("\nSprawdź czy:")
        print("1. Klucze API są poprawne")
        print("2. Tabele zostały utworzone w Supabase")
        print("3. Masz dostęp do internetu")
        return None

if __name__ == "__main__":
    check_database()
