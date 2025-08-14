#!/usr/bin/env python3
"""
ULTRA BIGDECODER 3.0 - Audyt Bazy Danych Supabase
Senior Principal Software Architect & Auditor
"""

import asyncio
import json
from supabase import create_client, Client
import sys
from typing import Dict, List, Any
import logging

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Dane dostępowe Supabase
SUPABASE_URL = "https://viepqnimxchgoxgijaub.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpZXBxbmlteGNoZ294Z2lqYXViIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDk4NjU1MywiZXhwIjoyMDcwNTYyNTUzfQ.CniELMUV7u8islNXXJuZKEtFbBVPdX4af-bmQw-q6e4"

class SupabaseAuditor:
    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.audit_results = {
            "database_schema": {},
            "tables_analysis": {},
            "indexes_analysis": {},
            "security_analysis": {},
            "performance_issues": [],
            "recommendations": []
        }
    
    async def audit_database_schema(self):
        """Audyt schematu bazy danych"""
        logger.info("🔍 Rozpoczynam audyt schematu bazy danych...")
        
        try:
            # Pobierz listę wszystkich tabel
            tables_query = """
            SELECT 
                schemaname,
                tablename,
                tableowner,
                hasindexes,
                hasrules,
                hastriggers
            FROM pg_tables 
            WHERE schemaname NOT IN ('information_schema', 'pg_catalog', 'pg_toast')
            ORDER BY schemaname, tablename;
            """
            
            tables_result = self.client.rpc('exec_sql', {'sql': tables_query}).execute()
            
            if tables_result.data:
                self.audit_results["database_schema"]["tables"] = tables_result.data
                logger.info(f"✅ Znaleziono {len(tables_result.data)} tabel")
            
            # Pobierz informacje o kolumnach
            columns_query = """
            SELECT 
                table_schema,
                table_name,
                column_name,
                data_type,
                is_nullable,
                column_default,
                character_maximum_length
            FROM information_schema.columns
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            ORDER BY table_schema, table_name, ordinal_position;
            """
            
            columns_result = self.client.rpc('exec_sql', {'sql': columns_query}).execute()
            
            if columns_result.data:
                self.audit_results["database_schema"]["columns"] = columns_result.data
                logger.info(f"✅ Znaleziono {len(columns_result.data)} kolumn")
            
        except Exception as e:
            logger.error(f"❌ Błąd podczas audytu schematu: {e}")
            self.audit_results["recommendations"].append({
                "priority": "P0",
                "category": "Database Access",
                "issue": f"Nie można pobrać schematu bazy danych: {e}",
                "recommendation": "Sprawdź uprawnienia service_role key lub połączenie z bazą"
            })
    
    async def audit_tables_data(self):
        """Audyt danych w tabelach"""
        logger.info("📊 Rozpoczynam audyt danych w tabelach...")
        
        # Lista głównych tabel do sprawdzenia (na podstawie README)
        main_tables = [
            'sessions', 'client_profiles', 'archetypes', 'strategies',
            'feedback', 'conversations', 'tesla_models', 'competitors',
            'promotions', 'objections', 'playbooks'
        ]
        
        for table in main_tables:
            try:
                # Sprawdź liczbę rekordów
                count_result = self.client.table(table).select('*', count='exact').execute()
                
                # Pobierz próbkę danych
                sample_result = self.client.table(table).select('*').limit(5).execute()
                
                self.audit_results["tables_analysis"][table] = {
                    "record_count": count_result.count if hasattr(count_result, 'count') else 0,
                    "sample_data": sample_result.data if sample_result.data else [],
                    "status": "accessible" if sample_result.data is not None else "error"
                }
                
                logger.info(f"✅ Tabela {table}: {count_result.count if hasattr(count_result, 'count') else 'N/A'} rekordów")
                
            except Exception as e:
                logger.warning(f"⚠️ Błąd dostępu do tabeli {table}: {e}")
                self.audit_results["tables_analysis"][table] = {
                    "record_count": 0,
                    "sample_data": [],
                    "status": "error",
                    "error": str(e)
                }
    
    async def audit_indexes(self):
        """Audyt indeksów"""
        logger.info("🔍 Rozpoczynam audyt indeksów...")
        
        try:
            indexes_query = """
            SELECT 
                schemaname,
                tablename,
                indexname,
                indexdef
            FROM pg_indexes
            WHERE schemaname NOT IN ('information_schema', 'pg_catalog', 'pg_toast')
            ORDER BY schemaname, tablename, indexname;
            """
            
            indexes_result = self.client.rpc('exec_sql', {'sql': indexes_query}).execute()
            
            if indexes_result.data:
                self.audit_results["indexes_analysis"]["existing_indexes"] = indexes_result.data
                logger.info(f"✅ Znaleziono {len(indexes_result.data)} indeksów")
            
        except Exception as e:
            logger.error(f"❌ Błąd podczas audytu indeksów: {e}")
    
    async def audit_security(self):
        """Audyt bezpieczeństwa"""
        logger.info("🔒 Rozpoczynam audyt bezpieczeństwa...")
        
        try:
            # Sprawdź polityki RLS
            rls_query = """
            SELECT 
                schemaname,
                tablename,
                rowsecurity
            FROM pg_tables
            WHERE schemaname NOT IN ('information_schema', 'pg_catalog', 'pg_toast')
            ORDER BY schemaname, tablename;
            """
            
            rls_result = self.client.rpc('exec_sql', {'sql': rls_query}).execute()
            
            if rls_result.data:
                self.audit_results["security_analysis"]["rls_status"] = rls_result.data
                
                # Sprawdź które tabele nie mają RLS
                tables_without_rls = [table for table in rls_result.data if not table.get('rowsecurity')]
                
                if tables_without_rls:
                    self.audit_results["recommendations"].append({
                        "priority": "P1",
                        "category": "Security",
                        "issue": f"Tabele bez Row Level Security: {[t['tablename'] for t in tables_without_rls]}",
                        "recommendation": "Włącz RLS dla wszystkich tabel zawierających dane użytkowników"
                    })
                
                logger.info(f"✅ Sprawdzono RLS dla {len(rls_result.data)} tabel")
            
        except Exception as e:
            logger.error(f"❌ Błąd podczas audytu bezpieczeństwa: {e}")
    
    async def generate_recommendations(self):
        """Generuj rekomendacje na podstawie audytu"""
        logger.info("💡 Generuję rekomendacje...")
        
        # Sprawdź czy są tabele z dużą liczbą rekordów bez indeksów
        for table_name, table_info in self.audit_results["tables_analysis"].items():
            if table_info.get("record_count", 0) > 1000:
                self.audit_results["recommendations"].append({
                    "priority": "P2",
                    "category": "Performance",
                    "issue": f"Tabela {table_name} ma {table_info['record_count']} rekordów",
                    "recommendation": "Sprawdź czy wszystkie często używane kolumny mają odpowiednie indeksy"
                })
        
        # Sprawdź czy wszystkie krytyczne tabele istnieją
        critical_tables = ['sessions', 'client_profiles', 'archetypes', 'strategies']
        missing_tables = []
        
        for table in critical_tables:
            if table not in self.audit_results["tables_analysis"] or \
               self.audit_results["tables_analysis"][table]["status"] == "error":
                missing_tables.append(table)
        
        if missing_tables:
            self.audit_results["recommendations"].append({
                "priority": "P0",
                "category": "Critical",
                "issue": f"Brakujące lub niedostępne krytyczne tabele: {missing_tables}",
                "recommendation": "Utwórz brakujące tabele lub sprawdź uprawnienia dostępu"
            })
    
    async def run_full_audit(self):
        """Uruchom pełny audyt"""
        logger.info("🚀 Rozpoczynam pełny audyt bazy danych Supabase...")
        
        await self.audit_database_schema()
        await self.audit_tables_data()
        await self.audit_indexes()
        await self.audit_security()
        await self.generate_recommendations()
        
        logger.info("✅ Audyt zakończony!")
        return self.audit_results
    
    def save_audit_report(self, filename="supabase_audit_report.json"):
        """Zapisz raport audytu do pliku"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.audit_results, f, indent=2, ensure_ascii=False)
        logger.info(f"📄 Raport audytu zapisany do: {filename}")

async def main():
    """Główna funkcja audytu"""
    auditor = SupabaseAuditor()
    
    try:
        results = await auditor.run_full_audit()
        auditor.save_audit_report()
        
        # Wyświetl podsumowanie
        print("\n" + "="*60)
        print("📊 PODSUMOWANIE AUDYTU BAZY DANYCH SUPABASE")
        print("="*60)
        
        # Tabele
        tables_count = len(results.get("database_schema", {}).get("tables", []))
        print(f"📋 Liczba tabel: {tables_count}")
        
        # Rekomendacje
        recommendations = results.get("recommendations", [])
        if recommendations:
            print(f"\n⚠️ ZNALEZIONE PROBLEMY ({len(recommendations)}):")
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. [{rec['priority']}] {rec['category']}: {rec['issue']}")
                print(f"   💡 {rec['recommendation']}\n")
        else:
            print("✅ Brak krytycznych problemów!")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Błąd podczas audytu: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(main())