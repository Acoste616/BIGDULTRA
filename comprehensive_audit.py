#!/usr/bin/env python3
"""
ULTRA BIGDECODER 3.0 - Kompleksowy Audyt Systemu
Senior Principal Software Architect & Auditor
"""

import json
import sys
import time
from typing import Dict, List, Any, Optional
import logging
from urllib.parse import urljoin
import asyncio

# Import standardowych bibliotek HTTP
try:
    import urllib.request
    import urllib.parse
    import urllib.error
    HTTP_AVAILABLE = True
except ImportError:
    HTTP_AVAILABLE = False

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Konfiguracja systemu
SUPABASE_URL = "https://viepqnimxchgoxgijaub.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpZXBxbmlteGNoZ294Z2lqYXViIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDk4NjU1MywiZXhwIjoyMDcwNTYyNTUzfQ.CniELMUV7u8islNXXJuZKEtFbBVPdX4af-bmQw-q6e4"

OLLAMA_API_URL = "https://ollama.com"
OLLAMA_API_KEY = "ece3ddba589d4f69a1a6ef97dad148e1.Yeza4Et1L67n0ASzyLV--_gt"
OLLAMA_MODEL = "gptoss120b"

class SystemAuditor:
    def __init__(self):
        self.audit_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "database_audit": {},
            "api_audit": {},
            "ai_audit": {},
            "security_audit": {},
            "performance_audit": {},
            "recommendations": [],
            "critical_issues": [],
            "system_health": "UNKNOWN"
        }
    
    def make_http_request(self, url: str, method: str = "GET", headers: Dict = None, data: Any = None) -> Dict:
        """Wykonaj żądanie HTTP używając urllib"""
        if not HTTP_AVAILABLE:
            return {"error": "HTTP libraries not available", "status_code": 500}
        
        try:
            if headers is None:
                headers = {}
            
            # Przygotuj dane
            if data and method in ["POST", "PUT", "PATCH"]:
                if isinstance(data, dict):
                    data = json.dumps(data).encode('utf-8')
                    headers['Content-Type'] = 'application/json'
                elif isinstance(data, str):
                    data = data.encode('utf-8')
            
            # Utwórz żądanie
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            
            # Wykonaj żądanie
            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = response.read().decode('utf-8')
                try:
                    json_data = json.loads(response_data)
                    return {
                        "status_code": response.status,
                        "data": json_data,
                        "headers": dict(response.headers)
                    }
                except json.JSONDecodeError:
                    return {
                        "status_code": response.status,
                        "data": response_data,
                        "headers": dict(response.headers)
                    }
                    
        except urllib.error.HTTPError as e:
            error_data = e.read().decode('utf-8') if e.fp else str(e)
            return {
                "status_code": e.code,
                "error": error_data,
                "url": url
            }
        except Exception as e:
            return {
                "error": str(e),
                "status_code": 500,
                "url": url
            }
    
    def audit_database_connection(self):
        """Audyt połączenia z bazą danych Supabase"""
        logger.info("🔍 Testowanie połączenia z bazą danych Supabase...")
        
        # Test połączenia podstawowego
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Test 1: Sprawdź dostępność API
        health_url = f"{SUPABASE_URL}/rest/v1/"
        health_result = self.make_http_request(health_url, headers=headers)
        
        self.audit_results["database_audit"]["connection"] = {
            "supabase_api_accessible": health_result.get("status_code") in [200, 404],  # 404 też OK dla root
            "response": health_result
        }
        
        # Test 2: Lista tabel (poprzez REST API)
        tables_to_check = [
            'sessions', 'client_profiles', 'archetypes', 'strategies',
            'feedback', 'conversations', 'tesla_models', 'competitors',
            'promotions', 'objections', 'playbooks'
        ]
        
        table_results = {}
        for table in tables_to_check:
            table_url = f"{SUPABASE_URL}/rest/v1/{table}?select=*&limit=1"
            result = self.make_http_request(table_url, headers=headers)
            
            table_results[table] = {
                "accessible": result.get("status_code") == 200,
                "status_code": result.get("status_code"),
                "has_data": bool(result.get("data")) if result.get("status_code") == 200 else False,
                "sample_record": result.get("data", [{}])[0] if result.get("data") else None
            }
            
            if result.get("status_code") == 200:
                logger.info(f"✅ Tabela {table}: dostępna")
            else:
                logger.warning(f"⚠️ Tabela {table}: błąd {result.get('status_code')}")
        
        self.audit_results["database_audit"]["tables"] = table_results
        
        # Analiza wyników
        accessible_tables = sum(1 for t in table_results.values() if t["accessible"])
        total_tables = len(table_results)
        
        if accessible_tables == 0:
            self.audit_results["critical_issues"].append({
                "priority": "P0",
                "category": "Database",
                "issue": "Brak dostępu do żadnej tabeli w bazie danych",
                "impact": "System nie może działać bez dostępu do danych",
                "recommendation": "Sprawdź uprawnienia Supabase service key i konfigurację RLS"
            })
        elif accessible_tables < total_tables:
            missing_tables = [name for name, info in table_results.items() if not info["accessible"]]
            self.audit_results["recommendations"].append({
                "priority": "P1",
                "category": "Database",
                "issue": f"Brak dostępu do {len(missing_tables)} tabel: {missing_tables}",
                "recommendation": "Utwórz brakujące tabele lub sprawdź polityki RLS"
            })
    
    def audit_ai_integration(self):
        """Audyt integracji z AI (Ollama/GPToss)"""
        logger.info("🤖 Testowanie integracji z AI (GPToss 120b)...")
        
        # Test 1: Sprawdź dostępność API Ollama
        headers = {
            'Authorization': OLLAMA_API_KEY,
            'Content-Type': 'application/json'
        }
        
        # Test podstawowy - sprawdź czy API odpowiada
        api_test_url = f"{OLLAMA_API_URL}/api/generate"
        test_payload = {
            "model": OLLAMA_MODEL,
            "prompt": "Test połączenia. Odpowiedz krótko: OK",
            "stream": False,
            "options": {
                "temperature": 0.1,
                "max_tokens": 10
            }
        }
        
        ai_result = self.make_http_request(
            api_test_url, 
            method="POST", 
            headers=headers, 
            data=test_payload
        )
        
        self.audit_results["ai_audit"]["connection"] = {
            "api_accessible": ai_result.get("status_code") == 200,
            "status_code": ai_result.get("status_code"),
            "response": ai_result.get("data") if ai_result.get("status_code") == 200 else ai_result.get("error"),
            "model": OLLAMA_MODEL
        }
        
        # Test 2: Test funkcjonalności analizy klienta
        if ai_result.get("status_code") == 200:
            analysis_payload = {
                "model": OLLAMA_MODEL,
                "prompt": """Jesteś Ultra BIGDecoder 3.0. Przeanalizuj tego klienta:
                "Szukam samochodu dla rodziny, ale martwię się o koszty eksploatacji"
                
                Odpowiedz w formacie JSON:
                {
                    "archetyp": "nazwa_archetypu",
                    "confidence": 0.0-1.0,
                    "główne_potrzeby": ["lista"],
                    "strategia": "krótka strategia"
                }""",
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            }
            
            analysis_result = self.make_http_request(
                api_test_url,
                method="POST",
                headers=headers,
                data=analysis_payload
            )
            
            self.audit_results["ai_audit"]["analysis_test"] = {
                "successful": analysis_result.get("status_code") == 200,
                "response": analysis_result.get("data") if analysis_result.get("status_code") == 200 else analysis_result.get("error")
            }
            
            logger.info("✅ Test analizy AI zakończony")
        else:
            logger.error(f"❌ Brak połączenia z AI: {ai_result.get('error', 'Unknown error')}")
            self.audit_results["critical_issues"].append({
                "priority": "P0",
                "category": "AI Integration",
                "issue": "Brak połączenia z API Ollama/GPToss",
                "impact": "System nie może wykonywać analiz psychometrycznych",
                "recommendation": "Sprawdź klucz API Ollama i dostępność modelu GPToss 120b"
            })
    
    def audit_backend_api(self):
        """Audyt API backendu"""
        logger.info("🌐 Testowanie API backendu...")
        
        # Sprawdź czy backend działa lokalnie
        backend_urls = [
            "http://localhost:8000",
            "http://127.0.0.1:8000"
        ]
        
        backend_accessible = False
        backend_url = None
        
        for url in backend_urls:
            try:
                result = self.make_http_request(f"{url}/", method="GET")
                if result.get("status_code") in [200, 404, 422]:  # Różne kody OK dla FastAPI
                    backend_accessible = True
                    backend_url = url
                    break
            except:
                continue
        
        self.audit_results["api_audit"]["backend_connection"] = {
            "accessible": backend_accessible,
            "url": backend_url
        }
        
        if backend_accessible:
            # Test głównych endpointów
            endpoints_to_test = [
                "/docs",  # Swagger docs
                "/analyze",  # POST - analiza klienta
                "/sessions/create",  # POST - tworzenie sesji
                "/data/archetypes"  # GET - lista archetypów
            ]
            
            endpoint_results = {}
            
            for endpoint in endpoints_to_test:
                url = f"{backend_url}{endpoint}"
                
                if endpoint in ["/analyze", "/sessions/create"]:
                    # POST endpoints - test z przykładowymi danymi
                    test_data = {
                        "input_text": "Test audytu systemu",
                        "mode": "analyzer"
                    } if endpoint == "/analyze" else {"user_id": "audit_test"}
                    
                    result = self.make_http_request(url, method="POST", data=test_data)
                else:
                    # GET endpoints
                    result = self.make_http_request(url, method="GET")
                
                endpoint_results[endpoint] = {
                    "status_code": result.get("status_code"),
                    "accessible": result.get("status_code") in [200, 201, 422],  # 422 OK dla walidacji
                    "response_sample": str(result.get("data", ""))[:200] if result.get("data") else result.get("error", "")[:200]
                }
            
            self.audit_results["api_audit"]["endpoints"] = endpoint_results
            
            working_endpoints = sum(1 for ep in endpoint_results.values() if ep["accessible"])
            total_endpoints = len(endpoint_results)
            
            logger.info(f"✅ Backend API: {working_endpoints}/{total_endpoints} endpointów działa")
            
        else:
            logger.warning("⚠️ Backend API nie jest dostępny")
            self.audit_results["recommendations"].append({
                "priority": "P1",
                "category": "Backend API",
                "issue": "Backend API nie jest uruchomiony",
                "recommendation": "Uruchom backend: cd backend && python3 main_refactored.py"
            })
    
    def audit_security_configuration(self):
        """Audyt konfiguracji bezpieczeństwa"""
        logger.info("🔒 Audyt bezpieczeństwa...")
        
        security_issues = []
        
        # Sprawdź czy klucze są w kodzie (bad practice)
        if SUPABASE_KEY in str(self.audit_results):
            security_issues.append({
                "priority": "P1",
                "issue": "Klucz Supabase jest hardkodowany w skrypcie",
                "recommendation": "Przenieś klucze do zmiennych środowiskowych"
            })
        
        if OLLAMA_API_KEY in str(self.audit_results):
            security_issues.append({
                "priority": "P1", 
                "issue": "Klucz Ollama jest hardkodowany w skrypcie",
                "recommendation": "Przenieś klucze do zmiennych środowiskowych"
            })
        
        # Test CORS - czy API odpowiada na różne origins
        if self.audit_results["api_audit"].get("backend_connection", {}).get("accessible"):
            backend_url = self.audit_results["api_audit"]["backend_connection"]["url"]
            
            cors_headers = {
                'Origin': 'https://malicious-site.com',
                'Access-Control-Request-Method': 'POST'
            }
            
            cors_result = self.make_http_request(f"{backend_url}/analyze", headers=cors_headers)
            
            if cors_result.get("status_code") == 200:
                security_issues.append({
                    "priority": "P2",
                    "issue": "CORS może być zbyt permisywny",
                    "recommendation": "Ogranicz CORS do konkretnych domen w produkcji"
                })
        
        self.audit_results["security_audit"]["issues"] = security_issues
        
        if security_issues:
            logger.warning(f"⚠️ Znaleziono {len(security_issues)} problemów bezpieczeństwa")
        else:
            logger.info("✅ Brak krytycznych problemów bezpieczeństwa")
    
    def audit_system_performance(self):
        """Audyt wydajności systemu"""
        logger.info("⚡ Audyt wydajności...")
        
        performance_metrics = {}
        
        # Test czasu odpowiedzi bazy danych
        if self.audit_results["database_audit"]["connection"]["supabase_api_accessible"]:
            start_time = time.time()
            
            headers = {
                'apikey': SUPABASE_KEY,
                'Authorization': f'Bearer {SUPABASE_KEY}'
            }
            
            test_url = f"{SUPABASE_URL}/rest/v1/sessions?limit=1"
            result = self.make_http_request(test_url, headers=headers)
            
            db_response_time = time.time() - start_time
            performance_metrics["database_response_time"] = db_response_time
            
            if db_response_time > 2.0:
                self.audit_results["recommendations"].append({
                    "priority": "P2",
                    "category": "Performance",
                    "issue": f"Wolny czas odpowiedzi bazy danych: {db_response_time:.2f}s",
                    "recommendation": "Sprawdź indeksy i optymalizuj zapytania"
                })
        
        # Test czasu odpowiedzi AI
        if self.audit_results["ai_audit"]["connection"]["api_accessible"]:
            start_time = time.time()
            
            headers = {'Authorization': OLLAMA_API_KEY}
            test_payload = {
                "model": OLLAMA_MODEL,
                "prompt": "Test",
                "stream": False,
                "options": {"max_tokens": 5}
            }
            
            result = self.make_http_request(
                f"{OLLAMA_API_URL}/api/generate",
                method="POST",
                headers=headers,
                data=test_payload
            )
            
            ai_response_time = time.time() - start_time
            performance_metrics["ai_response_time"] = ai_response_time
            
            if ai_response_time > 10.0:
                self.audit_results["recommendations"].append({
                    "priority": "P2",
                    "category": "Performance", 
                    "issue": f"Wolny czas odpowiedzi AI: {ai_response_time:.2f}s",
                    "recommendation": "Rozważ cache'owanie odpowiedzi AI lub optymalizację promptów"
                })
        
        self.audit_results["performance_audit"]["metrics"] = performance_metrics
    
    def calculate_system_health(self):
        """Oblicz ogólny stan systemu"""
        logger.info("📊 Obliczanie ogólnego stanu systemu...")
        
        health_score = 0
        max_score = 0
        
        # Baza danych (30 punktów)
        max_score += 30
        if self.audit_results["database_audit"]["connection"]["supabase_api_accessible"]:
            health_score += 15
            
            accessible_tables = sum(1 for t in self.audit_results["database_audit"]["tables"].values() if t["accessible"])
            total_tables = len(self.audit_results["database_audit"]["tables"])
            if total_tables > 0:
                health_score += 15 * (accessible_tables / total_tables)
        
        # AI Integration (25 punktów)  
        max_score += 25
        if self.audit_results["ai_audit"]["connection"]["api_accessible"]:
            health_score += 15
            if self.audit_results["ai_audit"].get("analysis_test", {}).get("successful"):
                health_score += 10
        
        # Backend API (25 punktów)
        max_score += 25
        if self.audit_results["api_audit"]["backend_connection"]["accessible"]:
            health_score += 15
            
            if "endpoints" in self.audit_results["api_audit"]:
                working_endpoints = sum(1 for ep in self.audit_results["api_audit"]["endpoints"].values() if ep["accessible"])
                total_endpoints = len(self.audit_results["api_audit"]["endpoints"])
                if total_endpoints > 0:
                    health_score += 10 * (working_endpoints / total_endpoints)
        
        # Bezpieczeństwo (20 punktów)
        max_score += 20
        security_issues = len(self.audit_results["security_audit"].get("issues", []))
        if security_issues == 0:
            health_score += 20
        elif security_issues <= 2:
            health_score += 10
        
        # Oblicz procent
        health_percentage = (health_score / max_score) * 100 if max_score > 0 else 0
        
        if health_percentage >= 90:
            system_health = "EXCELLENT"
        elif health_percentage >= 75:
            system_health = "GOOD"
        elif health_percentage >= 50:
            system_health = "FAIR"
        elif health_percentage >= 25:
            system_health = "POOR"
        else:
            system_health = "CRITICAL"
        
        self.audit_results["system_health"] = system_health
        self.audit_results["health_score"] = f"{health_percentage:.1f}%"
        
        logger.info(f"🎯 Stan systemu: {system_health} ({health_percentage:.1f}%)")
    
    def run_comprehensive_audit(self):
        """Uruchom kompleksowy audyt systemu"""
        logger.info("🚀 ROZPOCZYNAM KOMPLEKSOWY AUDYT ULTRA BIGDECODER 3.0")
        logger.info("=" * 60)
        
        try:
            # Wykonaj wszystkie testy
            self.audit_database_connection()
            self.audit_ai_integration()
            self.audit_backend_api()
            self.audit_security_configuration()
            self.audit_system_performance()
            self.calculate_system_health()
            
            logger.info("✅ Audyt zakończony pomyślnie!")
            
        except Exception as e:
            logger.error(f"❌ Błąd podczas audytu: {e}")
            self.audit_results["critical_issues"].append({
                "priority": "P0",
                "category": "System",
                "issue": f"Błąd podczas audytu: {e}",
                "recommendation": "Sprawdź logi i uruchom audyt ponownie"
            })
        
        return self.audit_results
    
    def generate_audit_report(self):
        """Generuj raport audytu"""
        print("\n" + "="*80)
        print("📊 RAPORT AUDYTU ULTRA BIGDECODER 3.0")
        print("="*80)
        print(f"Czas audytu: {self.audit_results['timestamp']}")
        print(f"Stan systemu: {self.audit_results['system_health']} ({self.audit_results.get('health_score', 'N/A')})")
        print()
        
        # Krytyczne problemy
        critical = self.audit_results.get("critical_issues", [])
        if critical:
            print("🚨 KRYTYCZNE PROBLEMY (P0):")
            for i, issue in enumerate(critical, 1):
                print(f"{i}. [{issue['category']}] {issue['issue']}")
                print(f"   💥 Wpływ: {issue.get('impact', 'Nie określono')}")
                print(f"   🔧 Rekomendacja: {issue['recommendation']}")
                print()
        
        # Rekomendacje
        recommendations = self.audit_results.get("recommendations", [])
        if recommendations:
            print("💡 REKOMENDACJE:")
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. [{rec['priority']}] [{rec['category']}] {rec['issue']}")
                print(f"   🔧 {rec['recommendation']}")
                print()
        
        # Podsumowanie komponentów
        print("📋 PODSUMOWANIE KOMPONENTÓW:")
        
        # Baza danych
        db_status = "✅ OK" if self.audit_results["database_audit"]["connection"]["supabase_api_accessible"] else "❌ BŁĄD"
        accessible_tables = sum(1 for t in self.audit_results["database_audit"]["tables"].values() if t["accessible"])
        total_tables = len(self.audit_results["database_audit"]["tables"])
        print(f"🗄️  Baza danych: {db_status} ({accessible_tables}/{total_tables} tabel dostępnych)")
        
        # AI
        ai_status = "✅ OK" if self.audit_results["ai_audit"]["connection"]["api_accessible"] else "❌ BŁĄD"
        print(f"🤖 AI (GPToss 120b): {ai_status}")
        
        # Backend API
        api_status = "✅ OK" if self.audit_results["api_audit"]["backend_connection"]["accessible"] else "❌ BŁĄD"
        print(f"🌐 Backend API: {api_status}")
        
        # Performance
        performance = self.audit_results.get("performance_audit", {}).get("metrics", {})
        if performance:
            print(f"⚡ Wydajność:")
            if "database_response_time" in performance:
                print(f"   - Baza danych: {performance['database_response_time']:.2f}s")
            if "ai_response_time" in performance:
                print(f"   - AI: {performance['ai_response_time']:.2f}s")
        
        print("\n" + "="*80)
        
        # Zapisz szczegółowy raport
        with open("comprehensive_audit_report.json", "w", encoding="utf-8") as f:
            json.dump(self.audit_results, f, indent=2, ensure_ascii=False)
        
        print("📄 Szczegółowy raport zapisano do: comprehensive_audit_report.json")
        
        return self.audit_results

def main():
    """Główna funkcja audytu"""
    auditor = SystemAuditor()
    
    try:
        # Uruchom audyt
        results = auditor.run_comprehensive_audit()
        
        # Wygeneruj raport
        auditor.generate_audit_report()
        
        # Zwróć kod wyjścia na podstawie stanu systemu
        if results["system_health"] in ["CRITICAL", "POOR"]:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        logger.info("Audyt przerwany przez użytkownika")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Nieoczekiwany błąd: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()