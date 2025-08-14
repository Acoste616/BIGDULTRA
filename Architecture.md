# 🏗️ ARCHITEKTURA ULTRA BIGDECODER 3.0

**Data:** 14 stycznia 2025  
**Wersja systemu:** 3.1.0  
**Status:** 🔴 POOR (40.5%) - Wymaga napraw  
**Model architektury:** C4 (Context, Container, Component, Code)

---

## 📋 SPIS TREŚCI

1. [Context Diagram (C1)](#c1-context-diagram)
2. [Container Diagram (C2)](#c2-container-diagram) 
3. [Component Diagram (C3)](#c3-component-diagram)
4. [Code Diagram (C4)](#c4-code-diagram)
5. [Deployment Architecture](#deployment-architecture)
6. [Data Architecture](#data-architecture)
7. [Security Architecture](#security-architecture)
8. [Proposed Improvements](#proposed-improvements)

---

## C1: CONTEXT DIAGRAM

### System Context
```
                    🏢 Tesla Sales Team
                           |
                           | Uses for customer analysis
                           ↓
    ┌─────────────────────────────────────────────────────┐
    │                                                     │
    │            ULTRA BIGDECODER 3.0                     │
    │        Inteligentny Asystent Sprzedaży              │
    │                                                     │
    │  • Analiza psychometryczna klientów                 │
    │  • Generowanie strategii sprzedażowych              │
    │  • Real-time coaching dla sprzedawców               │
    │  • Zbijanie obiekcji w czasie rzeczywistym          │
    │                                                     │
    └─────────────────────────────────────────────────────┘
                           |
           ┌───────────────┼───────────────┐
           |               |               |
           ↓               ↓               ↓
    🤖 GPToss AI     🗄️ Supabase DB   📊 Tesla Data
    (120b params)    (PostgreSQL)     (Models, Pricing)
    
    - Analiza NLP    - User sessions  - Product catalog
    - Generowanie    - Client profiles - Competitor data  
      strategii      - Conversations  - Market insights
    - Klasyfikacja   - Feedback data  - Pricing & promo
      archetypów     - Analytics      - Regulations
```

### External Dependencies
- **GPToss AI API:** Główny silnik analizy i generowania strategii
- **Supabase:** Baza danych i backend-as-a-service
- **Tesla Product Data:** Modele, ceny, specyfikacje (external API)
- **Polish EV Market Data:** Dopłaty, przepisy, infrastruktura

---

## C2: CONTAINER DIAGRAM

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────────────┐
│                        ULTRA BIGDECODER 3.0                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐  │
│  │   WEB BROWSER   │    │   MOBILE APP    │    │  SALES DESKTOP  │  │
│  │                 │    │   (Future)      │    │   (Future)      │  │
│  │ • HTML5/CSS3    │    │ • React Native  │    │ • Electron      │  │
│  │ • JavaScript    │    │ • TypeScript    │    │ • TypeScript    │  │
│  │ • Tailwind CSS  │    │ • Native APIs   │    │ • Desktop APIs  │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘  │
│           │                       │                       │         │
│           └───────────────────────┼───────────────────────┘         │
│                                   │                                 │
│                         HTTPS/WebSocket                             │
│                                   │                                 │
│  ┌─────────────────────────────────┼─────────────────────────────────┐  │
│  │                    BACKEND API LAYER                           │  │
│  │                                                                │  │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │  │
│  │  │   FASTAPI APP   │    │   WEBSOCKET     │    │   SCHEDULER  │ │  │
│  │  │                 │    │   HANDLER       │    │   (Future)   │ │  │
│  │  │ • REST API      │    │ • Real-time     │    │ • Batch jobs │ │  │
│  │  │ • Validation    │    │   updates       │    │ • Reports    │ │  │
│  │  │ • Auth/CORS     │    │ • Live coaching │    │ • Cleanup    │ │  │
│  │  │ • Health checks │    │ • Notifications │    │ • Analytics  │ │  │
│  │  └─────────────────┘    └─────────────────┘    └──────────────┘ │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                   │                                 │
│  ┌─────────────────────────────────┼─────────────────────────────────┐  │
│  │                   BUSINESS LOGIC LAYER                         │  │
│  │                                                                │  │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │  │
│  │  │   AI SERVICE    │    │  DATA SERVICE   │    │   METRICS    │ │  │
│  │  │                 │    │                 │    │   SERVICE    │ │  │
│  │  │ • Client analysis│   │ • CRUD ops      │    │ • OVN calc   │ │  │
│  │  │ • Strategy gen  │    │ • Session mgmt  │    │ • Churn risk │ │  │
│  │  │ • Archetype det │    │ • Profile mgmt  │    │ • Fun-Drive  │ │  │
│  │  │ • Objection     │    │ • Data enrichm. │    │ • Purchase   │ │  │
│  │  │   handling      │    │ • Caching       │    │   likelihood │ │  │
│  │  └─────────────────┘    └─────────────────┘    └──────────────┘ │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                   │                                 │
│  ┌─────────────────────────────────┼─────────────────────────────────┐  │
│  │                     DATA LAYER                                  │  │
│  │                                                                │  │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │  │
│  │  │  SUPABASE DB    │    │   REDIS CACHE   │    │  FILE STORE  │ │  │
│  │  │                 │    │   (Future)      │    │  (Future)    │ │  │
│  │  │ • PostgreSQL    │    │ • AI responses  │    │ • Logs       │ │  │
│  │  │ • 11 tables     │    │ • Session data  │    │ • Reports    │ │  │
│  │  │ • RLS policies  │    │ • Frequent      │    │ • Exports    │ │  │
│  │  │ • Indexes       │    │   queries       │    │ • Backups    │ │  │
│  │  └─────────────────┘    └─────────────────┘    └──────────────┘ │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SERVICES                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐  │
│  │   GPTOSS AI     │    │  TESLA APIs     │    │  MARKET DATA    │  │
│  │                 │    │   (Future)      │    │                 │  │
│  │ • 120b params   │    │ • Inventory     │    │ • EV subsidies  │  │
│  │ • NLP analysis  │    │ • Pricing       │    │ • Tax benefits  │  │
│  │ • Text generation│   │ • Availability  │    │ • Competitors   │  │
│  │ • Classification │    │ • Configurator  │    │ • Regulations   │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Container Status
| Container | Status | Issues | Priority |
|-----------|--------|---------|----------|
| Web Browser | ✅ Working | Monolithic HTML | P2 |
| Backend API | ❌ Down | Missing deps | P0 |
| AI Service | ❌ Down | Model unavailable | P0 |
| Data Service | ⚠️ Partial | Missing tables | P0 |
| Supabase DB | ⚠️ Partial | 7/11 tables missing | P0 |

---

## C3: COMPONENT DIAGRAM - BACKEND API

### FastAPI Application Components
```
┌─────────────────────────────────────────────────────────────────────┐
│                         FASTAPI APPLICATION                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                      API ENDPOINTS                             │ │
│  │                                                                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ │
│  │  │   ANALYZE    │  │   SESSIONS   │  │    HEALTH    │         │ │
│  │  │              │  │              │  │              │         │ │
│  │  │ POST /analyze│  │ POST /create │  │ GET /health  │         │ │
│  │  │ • Input text │  │ • Session ID │  │ • DB status  │         │ │
│  │  │ • Mode select│  │ • User ID    │  │ • AI status  │         │ │
│  │  │ • Context    │  │ • Metadata   │  │ • Metrics    │         │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │ │
│  │                                                                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ │
│  │  │   STRATEGY   │  │   FEEDBACK   │  │  WEBSOCKET   │         │ │
│  │  │              │  │              │  │              │         │ │
│  │  │ POST /gen    │  │ POST /submit │  │ WS /ws/{id}  │         │ │
│  │  │ • Generate   │  │ • Rating     │  │ • Real-time  │         │ │
│  │  │ • Validate   │  │ • Comments   │  │ • Live coach │         │ │
│  │  │ • Store      │  │ • Learn      │  │ • Updates    │         │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                   │                                 │
│  ┌─────────────────────────────────┼─────────────────────────────────┐ │
│  │                    MIDDLEWARE LAYER                             │ │
│  │                                                                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ │
│  │  │     CORS     │  │  VALIDATION  │  │   LOGGING    │         │ │
│  │  │              │  │              │  │              │         │ │
│  │  │ • Origins    │  │ • Pydantic   │  │ • Structured │         │ │
│  │  │ • Methods    │  │ • Schemas    │  │ • JSON format│         │ │
│  │  │ • Headers    │  │ • Types      │  │ • Error track│         │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                   │                                 │
│  ┌─────────────────────────────────┼─────────────────────────────────┐ │
│  │                   SERVICE LAYER                                 │ │
│  │                                                                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ │
│  │  │  AI CLIENT   │  │  DB SERVICE  │  │   METRICS    │         │ │
│  │  │              │  │              │  │              │         │ │
│  │  │ • GPToss API │  │ • Supabase   │  │ • Calculator │         │ │
│  │  │ • Prompts    │  │ • CRUD ops   │  │ • OVN/Churn  │         │ │
│  │  │ • Fallback   │  │ • Relations  │  │ • Fun-Drive  │         │ │
│  │  │ • Cache      │  │ • Migrations │  │ • Purchase   │         │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                   │                                 │
│  ┌─────────────────────────────────┼─────────────────────────────────┐ │
│  │                    MODELS LAYER                                 │ │
│  │                                                                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ │
│  │  │   SCHEMAS    │  │   ENTITIES   │  │     DTOS     │         │ │
│  │  │              │  │              │  │              │         │ │
│  │  │ • Request    │  │ • Session    │  │ • Analysis   │         │ │
│  │  │ • Response   │  │ • Profile    │  │ • Strategy   │         │ │
│  │  │ • Validation │  │ • Archetype  │  │ • Feedback   │         │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Dependencies
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Controllers   │ ──→│    Services     │ ──→│   Repositories  │
│                 │    │                 │    │                 │
│ • Route handlers│    │ • Business logic│    │ • Data access   │
│ • Input/Output  │    │ • AI integration│    │ • DB operations │
│ • Error handling│    │ • Calculations  │    │ • External APIs │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ↓                       ↓                       ↓
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Models      │    │   Utilities     │    │   Config        │
│                 │    │                 │    │                 │
│ • Pydantic      │    │ • Helpers       │    │ • Environment   │
│ • Validation    │    │ • Formatters    │    │ • Constants     │
│ • Serialization │    │ • Converters    │    │ • Settings      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## C4: CODE DIAGRAM - AI SERVICE

### ExpertOllamaClient Class Structure
```python
┌─────────────────────────────────────────────────────────────────────┐
│                      ExpertOllamaClient                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ATTRIBUTES:                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │ • base_url: str                                                 │ │
│  │ • api_key: str                                                  │ │
│  │ • model: str = "gptoss120b"                                     │ │
│  │ • db_service: ExtendedDatabaseService                           │ │
│  │ • expert_data: Dict[str, Any]                                   │ │
│  │ • system_prompts: Dict[str, str]                                │ │
│  │ • fallback_responses: List[Dict]                                │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  METHODS:                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │ + __init__(base_url, api_key, model, db_service)               │ │
│  │ + initialize_expert_knowledge() -> None                        │ │
│  │ + analyze_customer_expert(input, context) -> Dict              │ │
│  │ + generate_strategy(profile, context) -> Dict                  │ │
│  │ + handle_objection(objection, context) -> Dict                 │ │
│  │ + get_playbook(archetype, situation) -> Dict                   │ │
│  │ + _make_ai_request(prompt, options) -> Dict                    │ │
│  │ + _fallback_analysis(input, context) -> Dict                   │ │
│  │ + _build_expert_prompt(input, context) -> str                  │ │
│  │ + _parse_ai_response(response) -> Dict                         │ │
│  │ + close() -> None                                              │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  DEPENDENCIES:                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │ → ExtendedDatabaseService (data access)                        │ │
│  │ → MetricsCalculator (performance metrics)                      │ │
│  │ → ollama (AI model client)                                     │ │
│  │ → asyncio (async operations)                                   │ │
│  │ → logging (error handling)                                     │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow Sequence
```
Client Request → FastAPI → AIService → Database → AI API → Response

1. POST /analyze
   ├── Validate input (Pydantic)
   ├── Get session context (DB)
   ├── Build expert prompt (AI Service)
   ├── Call GPToss API (External)
   ├── Parse AI response (AI Service)  
   ├── Calculate metrics (Metrics Service)
   ├── Store results (DB)
   └── Return analysis (JSON)

2. Error Handling Flow
   ├── AI API failure → Fallback analysis
   ├── DB connection error → Cached response
   ├── Validation error → Error response
   └── Timeout → Partial response
```

---

## DEPLOYMENT ARCHITECTURE

### Current State (Local Development)
```
┌─────────────────────────────────────────────────────────────────────┐
│                        LOCAL MACHINE                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐              ┌─────────────────┐               │
│  │    TERMINAL 1   │              │    TERMINAL 2   │               │
│  │                 │              │                 │               │
│  │ Backend Server  │              │ Frontend Server │               │
│  │ Port: 8000      │              │ Port: 3000      │               │
│  │                 │              │                 │               │
│  │ python3         │              │ python3 -m      │               │
│  │ main_refactored │              │ http.server     │               │
│  │ .py             │              │ 3000            │               │
│  └─────────────────┘              └─────────────────┘               │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                        BROWSER                                  │ │
│  │                                                                │ │
│  │  http://localhost:3000/ultra-bigdecoder.html                   │ │
│  │                                                                │ │
│  │  ├── Fetch API calls to http://localhost:8000                  │ │
│  │  ├── WebSocket connection for real-time                        │ │
│  │  └── Static assets (CSS, JS) embedded                          │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

External Dependencies:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Supabase      │    │   GPToss AI     │    │   CDN Assets    │
│                 │    │                 │    │                 │
│ PostgreSQL DB   │    │ ollama.com      │    │ Tailwind CSS    │
│ REST API        │    │ API calls       │    │ Chart.js        │
│ Real-time       │    │ 120b model      │    │ Google Fonts    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Proposed Production Architecture
```
┌─────────────────────────────────────────────────────────────────────┐
│                           CLOUD PROVIDER                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                      LOAD BALANCER                             │ │
│  │                                                                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ │
│  │  │   NGINX      │  │     SSL      │  │   FIREWALL   │         │ │
│  │  │              │  │              │  │              │         │ │
│  │  │ • Routing    │  │ • TLS 1.3    │  │ • Rate limit │         │ │
│  │  │ • Caching    │  │ • Cert mgmt  │  │ • DDoS prot  │         │ │
│  │  │ • Compression│  │ • HSTS       │  │ • IP filter  │         │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                   │                                 │
│  ┌─────────────────────────────────┼─────────────────────────────────┐ │
│  │                   CONTAINER ORCHESTRATION                       │ │
│  │                                                                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ │
│  │  │   FRONTEND   │  │   BACKEND    │  │   WORKER     │         │ │
│  │  │   PODS       │  │   PODS       │  │   PODS       │         │ │
│  │  │              │  │              │  │              │         │ │
│  │  │ • React App  │  │ • FastAPI    │  │ • Scheduler  │         │ │
│  │  │ • 3 replicas │  │ • 2 replicas │  │ • AI batch   │         │ │
│  │  │ • Auto-scale │  │ • Auto-scale │  │ • Reports    │         │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                   │                                 │
│  ┌─────────────────────────────────┼─────────────────────────────────┐ │
│  │                     DATA LAYER                                  │ │
│  │                                                                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ │
│  │  │  SUPABASE    │  │   REDIS      │  │   S3 BUCKET  │         │ │
│  │  │              │  │              │  │              │         │ │
│  │  │ • PostgreSQL │  │ • Cache      │  │ • Static     │         │ │
│  │  │ • Multi-AZ   │  │ • Sessions   │  │ • Logs       │         │ │
│  │  │ • Backup     │  │ • Cluster    │  │ • Exports    │         │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                       MONITORING & OBSERVABILITY                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   LOGGING    │  │   METRICS    │  │   TRACING    │              │
│  │              │  │              │  │              │              │
│  │ • ELK Stack  │  │ • Prometheus │  │ • Jaeger     │              │
│  │ • Structured │  │ • Grafana    │  │ • OpenTel    │              │
│  │ • Centralized│  │ • Alerts     │  │ • APM        │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## DATA ARCHITECTURE

### Current Database Schema (Partial)
```
┌─────────────────────────────────────────────────────────────────────┐
│                        SUPABASE POSTGRESQL                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ✅ EXISTING TABLES (4/11)                                         │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                                                                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ │
│  │  │  archetypes  │  │  promotions  │  │  objections  │         │ │
│  │  │              │  │              │  │              │         │ │
│  │  │ • id (PK)    │  │ • id (PK)    │  │ • id (PK)    │         │ │
│  │  │ • name       │  │ • title      │  │ • category   │         │ │
│  │  │ • traits     │  │ • amount     │  │ • content    │         │ │
│  │  │ • strategies │  │ • valid_until│  │ • response   │         │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │ │
│  │                                                                │ │
│  │  ┌──────────────┐                                              │ │
│  │  │  playbooks   │                                              │ │
│  │  │              │                                              │ │
│  │  │ • id (PK)    │                                              │ │
│  │  │ • title      │                                              │ │
│  │  │ • content    │                                              │ │
│  │  │ • archetype  │                                              │ │
│  │  └──────────────┘                                              │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ❌ MISSING TABLES (7/11) - CRITICAL                               │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                                                                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ │
│  │  │   sessions   │  │client_profiles│ │ conversations│         │ │
│  │  │              │  │              │  │              │         │ │
│  │  │ • session_id │  │ • profile_id │  │ • message_id │         │ │
│  │  │ • user_id    │  │ • session_id │  │ • session_id │         │ │
│  │  │ • metadata   │  │ • archetype  │  │ • content    │         │ │
│  │  │ • created_at │  │ • confidence │  │ • timestamp  │         │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │ │
│  │                                                                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ │
│  │  │  strategies  │  │   feedback   │  │tesla_models  │         │ │
│  │  │              │  │              │  │              │         │ │
│  │  │ • strategy_id│  │ • feedback_id│  │ • model_id   │         │ │
│  │  │ • session_id │  │ • session_id │  │ • name       │         │ │
│  │  │ • content    │  │ • rating     │  │ • price      │         │ │
│  │  │ • confidence │  │ • comments   │  │ • specs      │         │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │ │
│  │                                                                │ │
│  │  ┌──────────────┐                                              │ │
│  │  │ competitors  │                                              │ │
│  │  │              │                                              │ │
│  │  │ • brand      │                                              │ │
│  │  │ • model      │                                              │ │
│  │  │ • comparison │                                              │ │
│  │  └──────────────┘                                              │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Proposed Complete Schema
```sql
-- Core session management
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR UNIQUE NOT NULL,
    user_id VARCHAR,
    metadata JSONB DEFAULT '{}',
    client_context JSONB DEFAULT '{}',
    archetype_evolution JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR DEFAULT 'active'
);

-- Client profiling and analysis
CREATE TABLE client_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR REFERENCES sessions(session_id),
    archetyp VARCHAR,
    confidence FLOAT,
    main_needs JSONB,
    objections JSONB,
    preferences JSONB,
    psychometric_data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Conversation history
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR REFERENCES sessions(session_id),
    message_type VARCHAR, -- 'client', 'salesperson', 'ai_suggestion'
    content TEXT,
    timestamp TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

-- Generated strategies
CREATE TABLE strategies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR REFERENCES sessions(session_id),
    strategy_type VARCHAR,
    content JSONB,
    confidence FLOAT,
    effectiveness_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Performance feedback
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR REFERENCES sessions(session_id),
    strategy_id UUID REFERENCES strategies(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    effectiveness VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Product data
CREATE TABLE tesla_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name VARCHAR NOT NULL,
    variant VARCHAR,
    price_pln INTEGER,
    range_km INTEGER,
    acceleration FLOAT,
    features JSONB,
    availability VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Competitive intelligence
CREATE TABLE competitors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand VARCHAR NOT NULL,
    model VARCHAR NOT NULL,
    price_pln INTEGER,
    range_km INTEGER,
    strengths JSONB,
    weaknesses JSONB,
    tesla_advantages JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## SECURITY ARCHITECTURE

### Current Security Posture
```
┌─────────────────────────────────────────────────────────────────────┐
│                        SECURITY LAYERS                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🔴 TRANSPORT LAYER                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │ • HTTP (not HTTPS) for local development                       │ │
│  │ • HTTPS for external APIs (Supabase, GPToss)                   │ │
│  │ • WebSocket without WSS                                         │ │
│  │ • CORS: wildcard (*) - too permissive                          │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  🔴 APPLICATION LAYER                                               │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │ • No authentication/authorization                               │ │
│  │ • API keys hardcoded in source                                  │ │
│  │ • No input sanitization beyond Pydantic                        │ │
│  │ • No rate limiting                                              │ │
│  │ • No request signing                                            │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ⚠️ DATA LAYER                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │ • Supabase service role key (powerful)                         │ │
│  │ • Row Level Security status unknown                             │ │
│  │ • No data encryption at rest (Supabase default)                │ │
│  │ • No PII/GDPR considerations                                    │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ✅ EXTERNAL SERVICES                                               │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │ • HTTPS for Supabase API                                        │ │
│  │ • HTTPS for GPToss API                                          │ │
│  │ • API key authentication                                        │ │
│  │ • Managed service security (Supabase)                          │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Proposed Security Architecture
```
┌─────────────────────────────────────────────────────────────────────┐
│                      ENHANCED SECURITY                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ✅ TRANSPORT LAYER                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │ • TLS 1.3 for all connections                                   │ │
│  │ • WSS for WebSocket connections                                 │ │
│  │ • HSTS headers                                                  │ │
│  │ • Certificate pinning                                           │ │
│  │ • CORS: specific origins only                                   │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ✅ APPLICATION LAYER                                               │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │ • JWT-based authentication                                      │ │
│  │ • Role-based authorization (RBAC)                               │ │
│  │ • Environment variables for secrets                             │ │
│  │ • Input validation & sanitization                               │ │
│  │ • Rate limiting (100 req/min)                                   │ │
│  │ • Request signing for AI API                                    │ │
│  │ • Security headers (CSP, XSS protection)                       │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ✅ DATA LAYER                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │ • Row Level Security (RLS) enabled                              │ │
│  │ • Least privilege access                                        │ │
│  │ • Data encryption at rest                                       │ │
│  │ • PII anonymization                                             │ │
│  │ • Audit logging                                                 │ │
│  │ • Regular security scans                                        │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ✅ MONITORING & COMPLIANCE                                         │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │ • Security event logging                                        │ │
│  │ • Intrusion detection                                           │ │
│  │ • GDPR compliance                                               │ │
│  │ • Vulnerability scanning                                        │ │
│  │ • Penetration testing                                           │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## PROPOSED IMPROVEMENTS

### Phase 1: Stabilization (P0) - 48h
1. **Fix Critical Dependencies**
   - Set up virtual environment
   - Install all Python packages
   - Create missing database tables
   - Fix AI integration

2. **Basic Security**
   - Move secrets to environment variables
   - Restrict CORS origins
   - Enable basic RLS policies

### Phase 2: Architecture Refactor (P1) - 2 weeks
1. **Frontend Modernization**
   ```
   Current: Monolithic HTML (2169 lines)
   ↓
   Proposed: React + TypeScript Components
   
   ┌─────────────────┐    ┌─────────────────┐
   │   App.tsx       │    │  Components/    │
   │                 │    │                 │
   │ • Router        │    │ • ChatInterface │
   │ • State mgmt    │    │ • AnalysisPanel │
   │ • Auth          │    │ • MetricsChart  │
   │ • Error bounds  │    │ • StrategyCard  │
   └─────────────────┘    └─────────────────┘
   ```

2. **Backend Microservices**
   ```
   Current: Monolithic FastAPI
   ↓
   Proposed: Microservices Architecture
   
   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
   │   API Gateway   │    │   AI Service    │    │  Data Service   │
   │                 │    │                 │    │                 │
   │ • Routing       │    │ • NLP analysis  │    │ • CRUD ops      │
   │ • Auth          │    │ • Model mgmt    │    │ • Caching       │
   │ • Rate limiting │    │ • Fallbacks     │    │ • Migrations    │
   └─────────────────┘    └─────────────────┘    └─────────────────┘
   ```

### Phase 3: Advanced Features (P2) - 1 month
1. **AI/ML Enhancements**
   - Multi-model support (GPT-4, Claude, Llama)
   - A/B testing for strategies
   - Continuous learning pipeline
   - Custom fine-tuning

2. **Analytics & Reporting**
   - Real-time dashboards
   - Sales performance metrics
   - AI effectiveness tracking
   - Customer journey analysis

### Phase 4: Scale & Performance (P3) - 2 months
1. **Infrastructure**
   - Container orchestration (Kubernetes)
   - Auto-scaling policies
   - CDN for static assets
   - Multi-region deployment

2. **Advanced Security**
   - Zero-trust architecture
   - End-to-end encryption
   - Compliance frameworks (SOC2, ISO27001)
   - Threat modeling

---

## ARCHITECTURAL DECISION RECORDS (ADRs)

### ADR-001: Database Choice
- **Decision:** Supabase PostgreSQL
- **Status:** Accepted
- **Rationale:** 
  - Managed PostgreSQL with real-time features
  - Built-in auth and row-level security
  - RESTful API auto-generation
  - Cost-effective for MVP

### ADR-002: AI Provider
- **Decision:** GPToss 120b via Ollama API
- **Status:** Under Review (model unavailable)
- **Alternatives:** OpenAI GPT-4, Anthropic Claude, Local Llama
- **Recommendation:** Implement multi-provider fallback

### ADR-003: Frontend Architecture
- **Decision:** Vanilla HTML/JS (current)
- **Status:** Deprecated
- **Proposed:** React + TypeScript
- **Rationale:** Better maintainability, type safety, component reuse

### ADR-004: Authentication Strategy
- **Decision:** No auth (current)
- **Status:** Temporary
- **Proposed:** JWT + Supabase Auth
- **Timeline:** Phase 2

---

**Dokument przygotowany przez:** Senior Principal Software Architect & Auditor  
**Ostatnia aktualizacja:** 14 stycznia 2025  
**Następny przegląd:** Po implementacji Phase 1 (16 stycznia 2025)  
**Status architektury:** 🔴 Requires Immediate Attention