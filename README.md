# 🚀 ULTRA BIGDECODER 3.0

**Inteligentny Asystent Sprzedaży Tesla** - System AI wspomagający proces sprzedaży poprzez analizę psychometryczną klientów i generowanie spersonalizowanych strategii w czasie rzeczywistym.

## 🎯 STATUS: SYSTEM W PEŁNI OPERACYJNY! (16.01.2025)

### ✨ Główne Funkcje

- 🧠 **Analiza Psychometryczna** - 10 archetypów klientów z AI
- 🎯 **Strategie Sprzedażowe** - Personalizowane playbooki
- 💬 **Real-time Chat** - WebSocket komunikacja
- 📊 **Metryki i Analityka** - Dashboard z kluczowymi wskaźnikami
- 🤖 **gptoss 120b AI** - 120 miliardów parametrów
- 🔄 **NOWE: Ciągła Analiza** - Po każdym wpisie (przecinek, kropka, 3+ znaki)
- 💡 **NOWE: Dane Eksperckie** - 31 tabel, dopłaty 27k PLN, 0% VAT, TCO 49.5k
- ⚡ **NOWE: Zbijanie Obiekcji** - Natychmiastowe odpowiedzi dopasowane do kontekstu

## 🏗️ Architektura

```
Frontend (HTML/JS) ↔ Backend (FastAPI) ↔ gptoss AI + Supabase DB
```

## 📁 Struktura Projektu

```
UltraBIGDecoder/
├── backend/                 # Python/FastAPI backend
│   ├── api/                # API endpoints
│   ├── core/               # Core configuration
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   │   ├── ai/            # AI services
│   │   ├── business/      # Business services
│   │   └── data/          # Data services
│   ├── utils/              # Utilities
│   └── tests/              # Tests
├── frontend/               # Frontend application
│   └── ultra-bigdecoder.html  # Single Page Application
├── database/               # Database scripts
├── docs/                   # Documentation
│   ├── Blueprint.md       # Architecture blueprint
│   ├── AUDIT_REPORT.md    # Security audit
│   └── PLAN.md           # Development plan
└── scripts/               # Utility scripts
```

## 🚀 Quick Start - JAK URUCHOMIĆ SYSTEM

### Wymagania
- Python 3.10+
- Konto Supabase (z 31 tabelami)
- Klucz API gptoss
- Windows/Linux/Mac

### ⚡ SZYBKIE URUCHOMIENIE (3 kroki)

#### 1️⃣ Backend (terminal 1):
```bash
cd backend
python main_refactored.py
# Czekaj na: "✅ System ULTRA BIGDECODER 3.0 gotowy!"
```

#### 2️⃣ Frontend (terminal 2):
```bash
cd frontend
python -m http.server 3000
# Serwer HTTP działa na porcie 3000
```

#### 3️⃣ Otwórz w przeglądarce:
```
http://localhost:3000/ultra-bigdecoder.html
```

### Instalacja (pierwsze uruchomienie)

1. **Klonuj repozytorium**
```bash
git clone https://github.com/user/UltraBIGDecoder.git
cd UltraBIGDecoder
```

2. **Utwórz środowisko Python**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Zainstaluj zależności**
```bash
pip install -r backend/requirements.txt
```

4. **Skonfiguruj zmienne środowiskowe**
```bash
cp .env.example .env
# Edytuj .env i dodaj swoje klucze
```

5. **Uruchom backend**
```bash
cd backend
python run.py
```

6. **Otwórz frontend**
```
Otwórz frontend/ultra-bigdecoder.html w przeglądarce
```

## ⚙️ Konfiguracja

Utwórz plik `.env` w głównym katalogu:

```env
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_service_role_key

# AI - gptoss 120b
GPTOSS_API_URL=https://api.gptoss.com
GPTOSS_API_KEY=your_gptoss_api_key
GPTOSS_MODEL=gptoss120b

# Security
SECRET_KEY=generate_secure_random_key
ENVIRONMENT=development
```

## 🔄 JAK DZIAŁA SYSTEM - CIĄGŁA ANALIZA W CZASIE RZECZYWISTYM

### Logika Działania:
1. **Wpisujesz:** "Mam panele fotowoltaiczne"
   - **System:** Natychmiast analizuje → pokazuje oszczędności z PV + ROI 4 lata

2. **Dodajesz:** ", myślę o Tesli"
   - **System:** Aktualizuje profil → pokazuje dopłaty 27k PLN + modele Tesla

3. **Dodajesz:** ", ale martwię się o zimę"
   - **System:** Wykrywa obiekcję → pokazuje zbicie (spadek zasięgu 20-30%, pompa ciepła)

4. **Dodajesz:** ", sąsiad ma i poleca"
   - **System:** Confidence >= 0.8 → PEŁNA STRATEGIA AKTYWOWANA!

### Progi Decyzyjne:
- **Confidence < 0.5:** 1 pytanie pogłębiające
- **Confidence 0.5-0.7:** 2 pytania pogłębiające
- **Confidence >= 0.8:** Pełna strategia + playbook + dane eksperckie

### Wykorzystywane Dane (31 tabel):
- **Dopłaty:** Mój Elektryk 27,000 PLN, dla firm do 70,000 PLN
- **Podatki:** 0% VAT do 2026, 100% amortyzacja, BIK 1%
- **TCO:** 49,500 PLN oszczędności na 5 lat
- **Infrastruktura:** 15+ Superchargerów w Polsce
- **Zimowa wydajność:** Spadek zasięgu 20-30%, pompa ciepła standard
- **Integracja PV:** 40-60km dziennie z 10kWp, ROI 4 lata

## 📊 Status Implementacji

| Komponent | Status | Opis |
|-----------|--------|------|
| Backend API | ✅ 100% | Wszystkie endpointy działają z ciągłą analizą |
| Frontend | ✅ 80% | HTML5+JS z real-time updates, planowana migracja do React |
| Baza danych | ✅ 100% | **31 tabel** w Supabase (9 podstawowych + 10 eksperckich + 12 dynamicznych) |
| Integracja AI | ✅ 100% | gptoss 120b z expert system prompt (2000+ linii) |
| Ciągła Analiza | ✅ 100% | Tryb "continuous" po każdym wpisie |
| Wiedza ekspercka | ✅ 100% | Polski rynek EV, dopłaty, przepisy, PV, infrastruktura |
| Testy | ⚠️ 30% | E2E testy działają, unit testy w trakcie |
| Dokumentacja | ✅ 95% | Zaktualizowana 16.01.2025 |

## 🔌 API Endpoints

### Główne endpointy:
- `POST /analyze` - Analiza klienta
- `POST /sessions/create` - Nowa sesja
- `POST /strategy/generate` - Generowanie strategii
- `POST /feedback/submit` - Feedback użytkownika
- `GET /data/archetypes` - Lista archetypów
- `WS /ws/{session_id}` - WebSocket real-time

### Przykład wywołania:
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Szukam bezpiecznego auta dla rodziny",
    "mode": "analyzer"
  }'
```

## 📈 Archetypy Klientów

1. **Security Seeker** - bezpieczeństwo
2. **Eco-Tech Pragmatist** - ekologia
3. **Busy Executive** - efektywność
4. **Status Achiever** - prestiż
5. **Family Guardian** - rodzina
6. **Performance Driver** - prędkość
7. **Rational Analyst** - analiza
8. **Value Optimizer** - wartość
9. **Innovation Seeker** - technologia
10. **Lifestyle Minimalist** - prostota

## 🛠️ Rozwój

### Roadmapa
- [ ] Sprint 1: Zabezpieczenie kluczy API
- [ ] Sprint 2-3: Optymalizacja wydajności
- [ ] Sprint 4-5: Nowe funkcjonalności
- [ ] Sprint 6+: Migracja do React/TypeScript

### Testowanie
```bash
# Uruchom testy
python -m pytest backend/tests/

# Test połączenia z AI
python test_ai.py
```

## 📄 Dokumentacja

- [Blueprint.md](docs/Blueprint.md) - Architektura systemu
- [AUDIT_REPORT.md](docs/AUDIT_REPORT.md) - Raport audytu
- [PLAN.md](docs/PLAN.md) - Plan rozwoju
- [BIGDECODER.md](docs/BIGDECODER.md) - Specyfikacja biznesowa

## 🔒 Bezpieczeństwo

- Klucze API w zmiennych środowiskowych
- Walidacja danych wejściowych
- System lokalny (jednoosobowy)

## 💰 Koszty (miesięczne)

- gptoss API: ~500-1000 PLN
- Supabase: Free tier
- **Razem:** ~1000-1500 PLN/miesiąc

## 🎯 CO DALEJ? - MOŻLIWE ULEPSZENIA

### Krótkoterminowe (1-2 tygodnie):
- **Migracja do React** - Komponentowa architektura frontendu
- **Voice Input** - Integracja z Web Speech API
- **Export PDF** - Generowanie raportów strategii
- **Mobile UI** - Responsywny design dla tabletów
- **Dark/Light Mode** - Przełącznik motywu

### Średnioterminowe (1-2 miesiące):
- **Multi-user** - System logowania i ról
- **CRM Integration** - Połączenie z Salesforce/HubSpot
- **Custom AI Training** - Fine-tuning na danych Tesla
- **Advanced Analytics** - Dashboardy i predykcje
- **API Marketplace** - Integracje zewnętrzne

## 🐛 ZNANE PROBLEMY I ROZWIĄZANIA

### Problem: CORS błędy
**Rozwiązanie:** Używaj Python http.server dla frontendu:
```bash
cd frontend
python -m http.server 3000
```

### Problem: Session creation error
**Rozwiązanie:** Upewnij się że backend używa `main_refactored.py` (nie main.py)

### Problem: Błąd 500 przy analizie
**Rozwiązanie:** Sprawdź czy wszystkie metody aliasowe są w ExtendedDatabaseService

## 📞 Wsparcie

W przypadku problemów:
1. Sprawdź dokumentację w `/docs`
2. Sprawdź logi w konsoli
3. Zweryfikuj konfigurację `.env`
4. Zobacz sekcję "Znane problemy" powyżej

## 📝 Licencja

Projekt prywatny - wszystkie prawa zastrzeżone.

---

**Wersja:** 3.0.1  
**Status:** ✅ W produkcji (lokalnie) - CIĄGŁA ANALIZA AKTYWNA  
**Ostatnia aktualizacja:** 16 stycznia 2025  
**Główne osiągnięcie:** System analizuje w czasie rzeczywistym po każdym wpisie!
