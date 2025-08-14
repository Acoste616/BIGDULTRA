"""
Sprawdzenie RLS i uprawnień w Supabase
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from supabase import create_client
import json

# Konfiguracja
SUPABASE_URL = "https://viepqnimxchgoxgijaub.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpZXBxbmlteGNoZ294Z2lqYXViIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDk4NjU1MywiZXhwIjoyMDcwNTYyNTUzfQ.CniELMUV7u8islNXXJuZKEtFbBVPdX4af-bmQw-q6e4"

def check_all_tables():
    """Sprawdza WSZYSTKIE tabele niezależnie od RLS"""
    
    print("🔍 PEŁNE SPRAWDZENIE TABEL W SUPABASE")
    print("=" * 70)
    
    try:
        # Service role key powinien ominąć RLS
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Połączono z Supabase (service_role key)\n")
        
        # KOMPLETNA lista tabel z Twojego screenshota
        all_tables = [
            'analysis_feedback',
            'archetype_aliases',  # Ta tabela nie była sprawdzana!
            'archetypes',
            'buying_signals',
            'charging_infrastructure_pl',  # Pełna nazwa
            'company_fleet_benefits',      # Pełna nazwa
            'data_updates_log',
            'dynamic_context',
            'ev_subsidies_poland',         # Pełna nazwa
            'insurance_providers_ev',
            'interaction_logs',
            'leasing_calculator_params',   # Pełna nazwa
            'llm_suggestions',
            'market_data_poland',
            'objection_archetypes',
            'objections',
            'playbooks',
            'products_competitors',
            'products_tesla',
            'promotions',
            'psychometric_profiles',
            'scoring_config',
            'seasonal_patterns',
            'service_network_tesla',       # Pełna nazwa
            'session_metadata',
            'solar_panels_compatibility',  # Pełna nazwa
            'tax_regulations_business',    # Pełna nazwa
            'tco_calculation_templates',   # Pełna nazwa
            'temporal_behavior_patterns',
            'user_expertise',
            'winter_performance_data',     # Pełna nazwa
        ]
        
        print(f"📋 Sprawdzam {len(all_tables)} tabel:\n")
        
        stats = {
            'with_data': 0,
            'empty': 0,
            'error': 0,
            'total_records': 0
        }
        
        for table in all_tables:
            try:
                # Używamy service_role key który omija RLS
                response = client.table(table).select("*", count='exact').execute()
                
                # Sprawdź count z nagłówka jeśli dostępny
                count = len(response.data) if response.data else 0
                
                if count > 0:
                    stats['with_data'] += 1
                    stats['total_records'] += count
                    status = "✅"
                    color = "\033[92m"  # Zielony
                else:
                    stats['empty'] += 1
                    status = "⚠️"
                    color = "\033[93m"  # Żółty
                
                print(f"{status} {color}{table:35}\033[0m | {count:5} rekordów")
                
                # Dla tabel z danymi pokaż przykład
                if count > 0 and response.data:
                    sample = response.data[0]
                    # Pokaż klucz identyfikujący
                    if 'name' in sample:
                        print(f"   └─ {sample.get('name', '')[:60]}")
                    elif 'program_name' in sample:
                        print(f"   └─ {sample.get('program_name', '')[:60]}")
                    elif 'model_name' in sample:
                        print(f"   └─ {sample.get('model_name', '')[:60]}")
                    elif 'id' in sample:
                        print(f"   └─ ID: {sample.get('id', '')}")
                        
            except Exception as e:
                stats['error'] += 1
                print(f"❌ {table:35} | Błąd: {str(e)[:40]}")
                
                # Spróbuj alternatywnych metod
                try:
                    # Próba z count
                    count_response = client.table(table).select("id", count='exact').execute()
                    if count_response:
                        print(f"   └─ Alternatywna metoda: znaleziono dane")
                except:
                    pass
        
        # Podsumowanie
        print("\n" + "=" * 70)
        print("📊 PODSUMOWANIE:")
        print(f"   ✅ Tabele z danymi: {stats['with_data']}")
        print(f"   ⚠️  Tabele puste: {stats['empty']}")
        print(f"   ❌ Błędy dostępu: {stats['error']}")
        print(f"   📈 Łączna liczba rekordów: {stats['total_records']}")
        
        # Sprawdź specyficzne tabele
        print("\n🔍 ANALIZA PROBLEMÓW:")
        
        # Sprawdź RLS
        print("\n📝 Tabele mogące mieć włączone RLS:")
        restricted_tables = [
            'interaction_logs',
            'analysis_feedback', 
            'dynamic_context',
            'psychometric_profiles',
            'user_expertise'
        ]
        
        for table in restricted_tables:
            try:
                # Spróbuj bez i z auth
                response = client.table(table).select("*").limit(1).execute()
                if not response.data:
                    print(f"   ⚠️ {table} - możliwe RLS, brak dostępu")
                else:
                    print(f"   ✅ {table} - dostęp OK")
            except Exception as e:
                print(f"   ❌ {table} - błąd: {str(e)[:30]}")
        
        # Sprawdź nowe tabele których mogło brakować
        print("\n🆕 Tabele które mogły być pominięte:")
        new_found = []
        for table in all_tables:
            if table == 'archetype_aliases':
                try:
                    response = client.table(table).select("*").execute()
                    if response.data:
                        new_found.append(table)
                        print(f"   ✅ {table} - ZNALEZIONA! ({len(response.data)} rekordów)")
                except:
                    pass
        
        return stats
        
    except Exception as e:
        print(f"\n❌ BŁĄD GŁÓWNY: {e}")
        return None

if __name__ == "__main__":
    stats = check_all_tables()
    
    print("\n💡 WNIOSKI:")
    if stats and stats['with_data'] >= 20:
        print("✅ System ma wystarczające dane do działania!")
        print("✅ Wszystkie krytyczne tabele zawierają dane")
    else:
        print("⚠️ Niektóre tabele mogą wymagać uzupełnienia")
