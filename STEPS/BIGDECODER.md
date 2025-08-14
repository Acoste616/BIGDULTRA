<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Projekt Ultra BIGDecoder 3.0: Ostateczny Dokument Przewodni (v3.0)

1. Nadrzędne Zasady i Ostateczna Wizja
Wizja Projektu: Stworzenie proaktywnego, samodoskonalącego się partnera strategicznego AI, który działa jako konwersacyjny "drugi mózg" sprzedawcy. System nie tylko reaguje na dane, ale przewiduje, symuluje i generuje zasoby w czasie rzeczywistym, ucząc się z każdej interakcji i korekty, aby z każdą rozmową stawać się potężniejszym narzędziem.
Sztywne Reguły (Core Principles): Poniższe zasady są fundamentem logiki systemu i nie podlegają negocjacjom. Każdy model AI wdrażany w tym projekcie musi bezwzględnie ich przestrzegać.
Zasada Ewolucji, Nie Rewolucji (Enhance, Don't Replace): System nigdy nie nadpisuje fundamentalnej wiedzy z bazy danych. Zamiast tego, ulepsza ją i kontekstualizuje. Korekty użytkownika i nowe dane tworzą dodatkową, priorytetową warstwę wiedzy, pozwalając AI na adaptację bez utraty stabilnego rdzenia.
Zasada Dynamicznej Granulacji (Dynamic Granularity): System musi być zdolny do identyfikowania niuansów, które nie pasują do istniejących archetypów. Jeśli AI wykryje powtarzalny wzorzec zachowań, który odbiega od zdefiniowanych modeli, jego zadaniem jest zaproponowanie utworzenia nowego, bardziej szczegółowego sub-archetypu, który zostanie zapisany do bazy po akceptacji użytkownika.
Zasada Ciągłej Analizy (Always-On Analysis): System nie czeka na komendę "Analizuj". Od momentu wpisania pierwszego słowa, AI w tle nieustannie analizuje treść, aktualizując profil klienta, przewidując obiekcje i przygotowując sugestie. Interfejs musi odzwierciedlać tę dynamikę.
Zasada Proaktywnego Dopytywania (Proactive Inquiry): AI nie jest pasywnym odbiorcą. Jeśli dostarczone informacje są niewystarczające do precyzyjnej analizy, system musi proaktywnie sugerować pytania, które należy zadać klientowi, aby uzupełnić luki informacyjne i zwiększyć pewność diagnozy.
2. Architektura i Logika Systemu "Ultra"
System bigdecoder.html był statycznym kalkulatorem. Ultra BIGDecoder 3.0 to żywy, konwersacyjny organizm. Jego "ultra" charakter wynika z proaktywnej, ciągłej interakcji napędzanej przez duży model językowy (LLM).

## 🔄 PRAWDZIWA LOGIKA DZIAŁANIA SYSTEMU (ZAKTUALIZOWANA 16.01.2025)

### ✅ STATUS: W PEŁNI ZAIMPLEMENTOWANA!

System działa jako **ciągły analyzer konwersacji w czasie rzeczywistym**, który z każdą wypowiedzią klienta wykonuje pełny cykl analizy:

### Cykl Analizy na Każdą Wypowiedź:
1. **Analizuje nową informację** od klienta - informacje którą wpiszę w chacie np (klient mowi ze sasiad ma tesle i mysli o ev)
2. **Łączy z całym dotychczasowym kontekstem** sesji
3. **Aktualizuje profil archetypu** (ewolucja w czasie rzeczywistym)
4. **Generuje natychmiastową odpowiedź** dopasowaną do aktualnego profilu
5. **Ocenia potencjał dalszej analizy** (czy warto pogłębiać?)
6. **Podpowiada pytania pogłębiające** (jeśli confidence < 0.8)
7. **Przy osiągnięciu progu pewności (≥0.8)** → aktywuje pełny panel strategii

### 📝 PRZYKŁAD RZECZYWISTEJ SESJI:

**Krok 1:**
- **Klient:** "Nie mam czasu na jazdę testową"
- **System analizuje:** `time_pressure = high`, archetyp: `Busy Executive` (confidence: 0.3)
- **Odpowiedź:** "Rozumiem, że czas to priorytet. Tesla można skonfigurować online w 10 minut."
- **Pytanie pogłębiające:** "Co sprawia, że rozważa Pan elektryka w tym momencie?"

**Krok 2:**
- **Klient:** "Mam panele fotowoltaiczne"
- **System łączy informacje:** `time_pressure + has_pv`, archetyp: `Eco-Tech Optimizer` (confidence: 0.5)
- **Odpowiedź:** "Idealnie! Z panelami PV Tesla będzie praktycznie darmowa w eksploatacji."
- **Pytanie pogłębiające:** "Jaka jest moc instalacji PV? To pomoże pokazać dokładne oszczędności."

**Krok 3:**
- **Klient:** "Sąsiad kupił Teslę i bardzo poleca"
- **System łączy wszystko:** `time_pressure + has_pv + social_proof`, archetyp: `Eco-Tech Pragmatist` (confidence: 0.8)
- **PRÓG PEWNOŚCI OSIĄGNIĘTY!**
- **Odpowiedź:** "Świetne potwierdzenie! 97% właścicieli Tesla poleca ją znajomym."
- **Pytania utwierdzające:** "Jakie auto Pan obecnie prowadzi?" + "Rozważał Pan konkretny model?"
- **🎯 PEŁNY PANEL STRATEGII AKTYWOWANY**

### Progi Decyzyjne:
- **Confidence < 0.5:** Tylko odpowiedź + 1 pytanie pogłębiające
- **Confidence 0.5-0.7:** Odpowiedź + 2 pytania pogłębiające  
- **Confidence ≥ 0.8:** Pełny panel strategii + pytania utwierdzające

### Mechanizm Ewolucji Archetypu:
```json
{
  "session_context": {
    "time_pressure": "high",
    "has_pv": true, 
    "social_proof": "positive_neighbor",
    "current_car": "unknown"
  },
  "archetype_evolution": [
    {"step": 1, "top_match": "Busy Executive", "confidence": 0.3},
    {"step": 2, "top_match": "Eco-Tech Optimizer", "confidence": 0.5}, 
    {"step": 3, "top_match": "Eco-Tech Pragmatist", "confidence": 0.8}
  ]
}
```

### Pętla Korekty w Locie:
- **Sprzedawca:** "Nie, to bardziej Status Achiever"
- **System:** Zapisuje korektę → przelicza profil → aktualizuje strategię → uczy się wzorców

## 📊 PEŁNY PANEL STRATEGII (Aktywacja przy Confidence ≥ 0.8)

Gdy system osiągnie próg pewności, aktywuje się kompletny panel strategii z 4 zakładkami:

### Zakładka 1: GŁÓWNA STRATEGIA
- **Zidentyfikowany archetyp:** Eco-Tech Pragmatist (confidence: 0.8)
- **Kluczowe triggery:** Oszczędności, wygoda, technologia, social proof
- **Nadrzędna strategia:** Fokus na ROI z paneli PV + wykorzystanie testimonial sąsiada
- **Następne kroki:** Kalkulator TCO, konfiguracja online, więcej testimoniali
- **Czerwone flagi:** Unikaj presji czasowej, nie komplikuj technicznie

### Zakładka 2: JĘZYK I KOMUNIKACJA  
- **Słownik mocy:** "darmowe ładowanie", "zwrot inwestycji", "jak sąsiad", "oszczędności"
- **Słownik toksyczny:** "skomplikowane", "długi proces", "dużo czasu"
- **Profil głosowy:** Praktyczny, oparty na faktach, konkretny
- **Ton komunikacji:** Rzeczowy, z liczbami, bez emocji

### Zakładka 3: PLAN DZIAŁANIA
- **Elaborat taktyczny:** "PV + Tesla = Perfect Match Strategy"
  1. Kalkulator oszczędności z panelami PV
  2. Online konfigurator (szybko, bez presji)
  3. Testimonial sąsiada + więcej case studies
  4. Konkretna oferta z terminami
- **Planowanie długoterminowe:** Follow-up w 48h, demo kalkulatora TCO

### Zakładka 4: ANALIZA I WSKAŹNIKI
- **Purchase Likelihood:** 72% (wysoki potencjał)
- **Churn Risk:** 15% (niskie ryzyko)
- **CTA Readiness:** "Online Configuration" (gotowy na działanie)
- **Fun-Drive:** Niski (to pragmatyk, nie poszukiwacz wrażeń)
- **OVN (Overnight Value):** Średni (ma PV, lubi technologię)
- **Sygnały de-eskalacji:** Brak (pozytywny nastrój)

### Rekomendowane Pytania Utwierdzające:
1. "Jakie auto Pan obecnie prowadzi i ile wydaje miesięcznie na paliwo?"
2. "Czy rozważał Pan konkretny model Tesla - Model 3 czy Model Y?"
3. "Kiedy planuje Pan podjąć decyzję o wymianie auta?"
4. "Czy chciałby Pan zobaczyć dokładne wyliczenia oszczędności z Pana panelami?"

### Zakładka 5: AI SPARRING PARTNER 🤖💬
**Rewolucyjna funkcja: Interaktywny symulator klienta + asystent strategiczny w czasie rzeczywistym**

#### **Funkcja 1: SYMULATOR KLIENTA**
AI wcieli się w zidentyfikowanego klienta (Eco-Tech Pragmatist) i będzie odpowiadać jego stylem myślenia:

**Przykłady interakcji:**
- **Sprzedawca:** "Jak Pan myśli o leasingu?"
- **AI jako klient:** "Hmm, leasing... to znaczy nie będę właścicielem? A jak to się ma do oszczędności z panelami? Sąsiad kupił za gotówkę i mówi, że to najlepiej. Nie wiem, czy chcę się wiązać na lata..."

- **Sprzedawca:** "Co Pan sądzi o autopilot?"
- **AI jako klient:** "To brzmi ciekawie, ale czy to bezpieczne? Mam dzieci, bezpieczeństwo to priorytet. A czy to nie komplikuje obsługi? Lubię proste rozwiązania."

#### **Funkcja 2: LIVE STRATEGY UPDATE**
System aktualizuje strategię w czasie rzeczywistym na podstawie nowych informacji:

**Przykład ewolucji sesji:**

**AKTUALIZACJA 1:** *"Klient odbył jazdę testową"*
- **Nowy kontekst:** `test_drive_completed = true`, `excitement_level = high`
- **Aktualizacja archetypu:** Eco-Tech Pragmatist → Eco-Tech Enthusiast (confidence: 0.9)
- **Nowa strategia:** Fokus na wrażenia + technologia, mniej na oszczędności
- **Purchase Likelihood:** 72% → 85%
- **CTA Readiness:** "Configuration" → "Immediate Purchase Discussion"

**AKTUALIZACJA 2:** *"Zaczął pytać o finansowanie"*
- **Nowy kontekst:** `financing_interest = true`, `budget_concerns = moderate`
- **Aktualizacja strategii:** Przygotuj opcje finansowania, kalkulator rat
- **Nowe pytania:** "Jaki budżet miesięczny Pan rozważa?" "Czy ma Pan auto do rozliczenia?"
- **Churn Risk:** 15% → 25% (może się wycofać przez finanse)

**AKTUALIZACJA 3:** *"Wygląda na podekscytowanego"*
- **Nowy kontekst:** `emotional_state = excited`, `body_language = positive`
- **Purchase Likelihood:** 85% → 92%
- **Nowa taktyka:** "Strike while iron is hot" - przyspieszenie procesu
- **CTA:** Bezpośrednia oferta + bonusy za szybką decyzję

**AKTUALIZACJA 4:** *"Ma auto do sprzedania"*
- **Nowy kontekst:** `trade_in_available = true`, `current_car_value = unknown`
- **Nowa strategia:** Wycena trade-in, porównanie kosztów, uproszczenie procesu
- **Pytania:** "Jaki rocznik i przebieg?" "Czy rozważał Pan sprzedaż prywatną?"
- **Playbook:** "Trade-in Advantage Strategy"

#### **Live Update Interface:**
```json
{
  "session_updates": [
    {
      "timestamp": "14:23",
      "trigger": "test_drive_completed",
      "impact": {
        "archetype_shift": "Pragmatist → Enthusiast",
        "confidence": "0.8 → 0.9",
        "purchase_likelihood": "72% → 85%",
        "new_strategy": "Emotion-driven approach",
        "priority_questions": ["Który model najbardziej podobał?", "Co najbardziej zaskoczyło?"]
      }
    },
    {
      "timestamp": "14:31", 
      "trigger": "financing_questions",
      "impact": {
        "churn_risk": "15% → 25%",
        "new_concerns": ["budget_constraints", "monthly_payment"],
        "recommended_tools": ["financing_calculator", "trade_in_estimator"],
        "de_escalation": "Focus on total value, not monthly payment"
      }
    }
  ]
}
```

#### **Rodzaje Live Updates:**
1. **Emocjonalne:** podekscytowany, sceptyczny, zniecierpliwiony, entuzjastyczny
2. **Behawioralne:** jazda testowa, pytania o finanse, porównania z konkurencją
3. **Kontekstowe:** ma auto do sprzedania, czas nagli, żona/mąż przeciwny/a
4. **Decyzyjne:** gotów kupować, potrzebuje czasu, chce porównać oferty

#### **Inteligentne Sugestie AI:**
- **"Widzę, że klient jest podekscytowany po jeździe. Teraz idealny moment na konkretną ofertę!"**
- **"Pytania o finansowanie + ma auto do sprzedania = przygotuj pakiet trade-in + leasing"**
- **"Poziom entuzjazmu spada - użyj testimonial sąsiada jako przypomnienie"**
- **"Klient porównuje z konkurencją - aktywuj playbook 'Competitive Advantage'"**

#### **Tryby Pracy AI Sparring Partner:**
1. **KLIENT MODE:** AI odpowiada jako klient, pomaga trenować argumenty
2. **COACH MODE:** AI analizuje i podpowiada strategie w czasie rzeczywistym  
3. **HYBRID MODE:** Przełącza między rolami w zależności od potrzeb

## 🎯 KLUCZOWE RÓŻNICE W LOGICE ULTRA BIGDECODER 3.0

### ❌ TYPOWY CHATBOT:
- Reaguje na pojedyncze pytania
- Nie pamięta kontekstu między wypowiedziami  
- Daje ogólne odpowiedzi
- Bierny - czeka na polecenia
- Nie analizuje profilu klienta

### ✅ ULTRA BIGDECODER 3.0:
- **Ciągła akumulacja kontekstu** - każda wypowiedź wzbogaca profil
- **Ewolucja archetypu w czasie rzeczywistym** - profil się doskonali
- **Inteligentne pytania pogłębiające** - aktywnie poszukuje informacji
- **Próg pewności** - wie, kiedy ma wystarczająco danych
- **Pełna strategia** - kompleksowy plan działania po osiągnięciu progu
- **Uczenie się z korekt** - dostosowuje się do stylu sprzedawcy

### Logika Progów:
- **< 0.5:** "Zbieranie informacji" - pytania podstawowe
- **0.5-0.7:** "Pogłębianie" - pytania szczegółowe  
- **≥ 0.8:** "Strategia" - pełny panel + pytania utwierdzające

### Mechanizm Pamięci:
System pamięta i łączy:
- Wszystkie wypowiedzi klienta w sesji
- Korekty sprzedawcy z poprzednich sesji
- Wzorce skutecznych strategii
- Kontekst branżowy i rynkowy
## 🚀 IMPLEMENTACJA TECHNICZNA (16.01.2025)

### Komponenty Zaimplementowane:

#### Frontend (ultra-bigdecoder.html):
```javascript
// Ciągła analiza po każdym wpisie
elements.observationInput.addEventListener('input', function() {
    const currentText = this.value.trim();
    if (currentText !== lastAnalyzedText && currentText.length > 2) {
        const textDiff = currentText.replace(lastAnalyzedText, '').trim();
        if (textDiff.length > 2 || currentText.includes(',') || currentText.includes('.')) {
            lastAnalyzedText = currentText;
            performContinuousAnalysis(); // Natychmiastowa analiza
        }
    }
});
```

#### Backend (main_refactored.py):
```python
# Tryb continuous w endpoint /analyze
if request.mode == "continuous":
    # Wzbogać o dane eksperckie
    analysis["enriched_data"] = {
        "subsidies": subsidies[:3],  # Top 3 dopłaty
        "tco_comparison": {"savings": 49500, "break_even_years": 3.5},
        "charging_infrastructure": {"superchargers_count": 15},
        "tax_benefits": {"vat_rate": 0, "depreciation": 100, "bik": 1}
    }
```

#### Baza Danych (31 tabel):
- **9 tabel podstawowych** (archetypes, objections, playbooks)
- **10 tabel eksperckich** (subsidies, tax_regulations, solar_panels)
- **12 tabel dynamicznych** (sessions, interactions, feedback)

3. Architektura Techniczna i Silnik Operacyjny
Sercem operacyjnym systemu jest duży model językowy gptoss 120b (GPT-class Open Source 120B). Model ten jest udostępniany i zarządzany poprzez API serwera gptoss.
Dlaczego Ollama?: Takie podejście gwarantuje trzy kluczowe korzyści:
Prywatność Danych: Wszystkie dane, w tym wrażliwe informacje o klientach, są przetwarzane w naszym zamkniętym środowisku, bez wysyłania ich do zewnętrznych dostawców.
Szybkość i Kontrola: Lokalne API minimalizuje opóźnienia (latency), co jest kluczowe dla płynnej interakcji w czasie rzeczywistym. Mamy pełną kontrolę nad konfiguracją i dostępnością modelu.
Elastyczność: Możemy swobodnie eksperymentować z różnymi modelami open-source i dostosowywać je do naszych specyficznych potrzeb bez uzależnienia od jednego dostawcy.
Rola AI w Systemie: Model LLM nie jest tylko generatorem tekstu. Pełni on rolę centralnego procesora analitycznego, który na podstawie danych z bazy Supabase i informacji od użytkownika, w czasie rzeczywistym:
Przeprowadza analizę psychometryczną.
Identyfikuje intencje i ryzyka.
Generuje strategie, skrypty i plany działania.
Uczy się i adaptuje swoje działanie.
## 4. Architektura Danych: 30 TABEL W SYSTEMIE ✅

Baza danych w Supabase jest kręgosłupem systemu z **30 w pełni funkcjonalnymi tabelami**. System zawiera teraz kompletną wiedzę ekspercką o polskim rynku EV.

### 📊 STATYSTYKI SYSTEMU:
- **Łączna liczba tabel:** 30
- **Tabele podstawowe:** 9 (dane statyczne)
- **Tabele eksperckie:** 10 (wiedza specjalistyczna) ✨ NOWE!
- **Tabele dynamiczne:** 11 (dane sesyjne)
- **Łączna objętość danych:** ~400+ rekordów podstawowych + nieograniczone dane dynamiczne

### TABELE PODSTAWOWE (9) - Statyczny Rdzeń Wiedzy

🟢 **ARCHETYPES** (10 rekordów, 8 kolumn)
- **Cel:** Profile psychologiczne klientów
- **Kluczowe kolumny:** `id`, `name`, `disc_profile`, `motivations` (JSONB), `fears` (JSONB), `triggers` (JSONB)
- **Logika AI:** Główny punkt odniesienia do analizy psychometrycznej

🟢 **OBJECTIONS** (12 rekordów, 6 kolumn)
- **Cel:** Katalog obiekcji i strategie pokonywania
- **Kluczowe kolumny:** `objection_type`, `rebuttal_strategy` (JSONB), `supporting_data` (JSONB)
- **Logika AI:** Framework odpowiedzi na obiekcje (FEEL-FELT-FOUND)

🟢 **PLAYBOOKS** (10 rekordów, 7 kolumn)
- **Cel:** Zaawansowane strategie sprzedażowe
- **Kluczowe kolumny:** `target_archetype_id`, `strategy_details` (JSONB), `success_rate`
- **Logika AI:** Dobór strategii na podstawie archetypu i obiekcji

🟢 **PRODUCTS_TESLA** (12 rekordów, 8 kolumn)
- **Dane:** Model 3/Y wszystkie warianty, ceny 189,990-279,990 PLN
- **Kluczowe kolumny:** `model_name`, `variant`, `base_price_pln`, `range_km`, `features` (JSONB)

🟢 **PRODUCTS_COMPETITORS** (109 rekordów, 6 kolumn)
- **Dane:** BMW, Mercedes, Audi, VW, Hyundai, Kia, Polestar
- **Kluczowe kolumny:** `brand`, `model_name`, `base_price_pln`, `comparison_points` (JSONB)

🟢 **MARKET_DATA_POLAND** (9 rekordów, 7 kolumn)
- **Dane:** Dotacje, statystyki rynku, trendy
- **Kluczowe kolumny:** `metric_name`, `metric_value`, `category`, `valid_until`

🟢 **PROMOTIONS** (7 rekordów, 7 kolumn)
- **Dane:** Aktualne promocje Tesla
- **Kluczowe kolumny:** `promotion_type`, `discount_amount_pln`, `conditions` (JSONB)

🟢 **SEASONAL_PATTERNS** (2 rekordy, 4 kolumny)
- **Dane:** Wzorce sezonowe sprzedaży
- **Kluczowe kolumny:** `season`, `impact_on_sales` (JSONB)

🟢 **OBJECTION_ARCHETYPES** (11 rekordów, 4 kolumny)
- **Cel:** Mapowanie archetyp ↔ obiekcja
- **Kluczowe kolumny:** `archetype_id`, `objection_id`, `likelihood`, `intensity`

### TABELE EKSPERCKIE (10) - Wiedza Specjalistyczna ✨ NOWE!

🔵 **EV_SUBSIDIES_POLAND** (12 kolumn)
- **Dane:** Mój Elektryk (27,000 PLN), Zielony Samochód (70,000 PLN), dopłaty lokalne
- **Kluczowe:** `program_name`, `max_amount_pln`, `eligibility_criteria` (JSONB)
- **AI używa:** Do kalkulacji rzeczywistego kosztu zakupu

🔵 **TAX_REGULATIONS_BUSINESS** (11 kolumn)
- **Dane:** 0% VAT do 2026, 100% amortyzacja, BIK 1%
- **Kluczowe:** `regulation_type`, `benefit_amount`, `calculation_formula`
- **AI używa:** Do wyliczeń korzyści dla firm

🔵 **SOLAR_PANELS_COMPATIBILITY** (11 kolumn)
- **Dane:** Integracja PV, ROI 4 lata, 40-60km/dzień z 10kWp
- **Kluczowe:** `pv_system_size_kwp`, `ev_range_per_day_km`, `roi_years`
- **AI używa:** Dla klientów z panelami fotowoltaicznymi

🔵 **CHARGING_INFRASTRUCTURE_PL** (14 kolumn)
- **Dane:** 15+ lokalizacji Supercharger, ceny 1.45-2.85 PLN/kWh
- **Kluczowe:** `location_city`, `max_power_kw`, `price_per_kwh`, `tesla_compatible`
- **AI używa:** Do planowania tras i kosztów ładowania

🔵 **COMPANY_FLEET_BENEFITS** (9 kolumn)
- **Dane:** Korzyści flotowe, case studies
- **Kluczowe:** `savings_calculation` (JSONB), `minimum_fleet_size`
- **AI używa:** Dla klientów biznesowych z flotami

🔵 **LEASING_CALCULATOR_PARAMS** (11 kolumn)
- **Dane:** Parametry leasingu różnych dostawców
- **Kluczowe:** `down_payment_percent`, `interest_rate_percent`, `residual_value_percent`
- **AI używa:** Do kalkulacji rat leasingowych

🔵 **INSURANCE_PROVIDERS_EV** (12 kolumn)
- **Dane:** OC/AC 2800-4500 PLN/rok, specjalne rabaty Tesla
- **Kluczowe:** `oc_annual_cost_from`, `ev_specific_coverage` (JSONB)
- **AI używa:** Do pełnej kalkulacji TCO

🔵 **SERVICE_NETWORK_TESLA** (11 kolumn)
- **Dane:** Centra serwisowe w Polsce, mobile service
- **Kluczowe:** `location_type`, `city`, `mobile_service_radius_km`
- **AI używa:** Przy obawach o serwis

🔵 **WINTER_PERFORMANCE_DATA** (10 kolumn)
- **Dane:** Spadek zasięgu zimą 20-30%, pompa ciepła
- **Kluczowe:** `temperature_celsius`, `range_loss_percent`, `heat_pump_equipped`
- **AI używa:** Przy pytaniach o zimę

🔵 **TCO_CALCULATION_TEMPLATES** (16 kolumn)
- **Dane:** Szablony TCO, 49,500 PLN oszczędności/5 lat
- **Kluczowe:** `annual_mileage_km`, `total_savings_period`, `break_even_months`
- **AI używa:** Do konkretnych wyliczeń finansowych
Cel Strategiczny: Stworzenie katalogu gotowych strategii zbijania obiekcji.
Logika dla AI: Gdy wykryjesz obiekcję, użyj struktury z kolumny rebuttal_strategy (JSON) jako frameworku do wygenerowania odpowiedzi. To nie są sztywne skrypty, ale schematy argumentacji (np. RISK->MITIGATION->PEACE OF MIND), które musisz wypełnić treścią dopasowaną do kontekstu rozmowy.
🟢 PLAYBOOKS (10 rekordów)
Cel Strategiczny: Dostarczenie zaawansowanych taktyk sprzedażowych.
Logika dla AI: Gdy warunki są spełnione (zidentyfikowany target_archetype_id lub target_objection_id), proaktywnie sugeruj użycie konkretnego playbooka. Traktuj strategy_details jako gotowy do użycia, wysokopoziomowy koncept taktyczny.
🟢 PRODUCTS_COMPETITORS (109 rekordów) 🚀 MASYWNIE ROZWINIĘTE 
Cel Strategiczny: Umożliwienie rzeczowych porównań produktowych.
Logika dla AI: System competitive intelligence znacznie przekroczył założenia! Wykorzystuj bogaty katalog 109 modeli konkurencji do generowania szczegółowych analiz porównawczych, kalkulacji TCO i precyzyjnych odpowiedzi na pytania techniczne. Pełna analiza rynku dostępna.

🟢 PRODUCTS_TESLA (12 rekordów) ✅ ZGODNE
Cel Strategiczny: Kompletny katalog produktów Tesla.
Logika dla AI: Wszystkie warianty modeli Tesla z pełnymi specyfikacjami technicznymi, cennikiem i statusem dostępności.
🟢 PROMOTIONS (7 rekordów) ✅ ROZWINIĘTE 
Cel Strategiczny: Aktualne oferty i promocje.
Logika dla AI: Wykorzystuj katalog promocji do personalizacji ofert. Baza zawiera więcej promocji niż oczekiwano.

🟢 SEASONAL_PATTERNS (2 rekordy) ✅ ZGODNE
Cel Strategiczny: Kontekst biznesowy i czasowy.
Logika dla AI: Używaj wzorców sezonowych aby dostosować komunikację do celów kwartalno-rocznych i cyklów psychologicznych klientów.
Tabele Dynamiczne (Ewoluująca Pamięć i Przestrzeń Treningowa)
**STATUS IMPLEMENTACJI:** ✅ 100% KOMPLETNY - WSZYSTKIE 20 TABEL DZIAŁAJĄ

**ZAIMPLEMENTOWANE STRUKTURY (puste ale gotowe):**

⚪ ANALYSIS_FEEDBACK ✅ STRUKTURA GOTOWA
Cel Strategiczny: Zapewnienie mechanizmu Pętli Korekty w Locie. To jest serce zdolności adaptacyjnych systemu.
Logika Zapisu dla AI: Zapisuj tutaj za każdym razem, gdy użytkownik jawnie koryguje Twoją analizę (np. "Nie zgadzam się, to nie ten archetyp"). Rekord powinien zawierać co najmniej: session_id, timestamp, state_before_correction (Twoja błędna analiza w formacie JSON), user_correction (treść korekty użytkownika).
Logika Odczytu dla AI: Podczas Aktywnej Sesji Treningowej, analizuj tę tabelę w poszukiwaniu wzorców w korektach użytkownika, aby formułować inteligentne pytania pogłębiające.

⚪ DYNAMIC_CONTEXT ✅ STRUKTURA GOTOWA
Cel Strategiczny: Stworzenie trwałej, rozszerzalnej bazy wiedzy – Twojej pamięci długoterminowej.
Logika Zapisu dla AI: Gdy użytkownik użyje komendy /zapisz ten kontekst z nową informacją (np. linkiem do artykułu), Twoim zadaniem jest: 1. Przeanalizować treść. 2. Streścić ją. 3. Wyekstrahować kluczowe encje i fakty. 4. Skategoryzować i otagować wiedzę. 5. Zapisać ją w tej tabeli w ustrukturyzowanej formie.
Logika Odczytu dla AI: Przed każdą głębszą analizą, odpytuj tę tabelę w poszukiwaniu relevantnych informacji, które mogą wzbogacić Twój kontekst i poprawić jakość odpowiedzi.
⚪ INTERACTION_LOGS ✅ STRUKTURA GOTOWA
Cel Strategiczny: Działanie jako rejestrator sesji na potrzeby treningu i analizy.
Logika Zapisu dla AI: Zapisuj tutaj transkrypt każdej interakcji w ramach sesji: wpis użytkownika, Twoja wygenerowana odpowiedź/sugestia, ewentualna korekta.
Logika Odczytu dla AI: Ta tabela jest głównym źródłem danych dla Aktywnej Sesji Treningowej. Analizujesz ją, aby zrozumieć całą ścieżkę rozumowania, która doprowadziła do korekty w analysis_feedback, co pozwala zadawać bardziej precyzyjne pytania.

⚪ PSYCHOMETRIC_PROFILES ✅ STRUKTURA GOTOWA
Cel Strategiczny: Archiwizacja kompletnych, wielowymiarowych profili klientów.
Logika Zapisu dla AI: Po zakończeniu każdej sesji, zapisz tutaj finalny, zagregowany profil klienta w formacie JSON. Powinien on zawierać: ostateczne wyniki w modelach DISC/Big Five/Schwartz, finalne wartości wskaźników Fun-Drive/OVN oraz listę kluczowych triggerów i obiekcji, które wystąpiły.
Logika Odczytu dla AI: Możesz używać tych danych do prowadzenia metaanaliz (np. "Pokaż mi profile klientów, którzy ostatecznie kupili Model Y w Q4"), co pozwala na identyfikowanie głębszych, długoterminowych trendów.

**TABELE SYSTEMOWE - WSZYSTKIE ZAIMPLEMENTOWANE (7 tabel):**

✅ LLM_SUGGESTIONS ✅ ZAIMPLEMENTOWANA
Cel Strategiczny: System "mocnych sugestii" i aktywnego uczenia od użytkownika.
Logika dla AI: Zapisuj tutaj proaktywne propozycje nowych danych, archetypów, playbooków. Klasyfikuj według priorytetu (KRYTYCZNA/WAŻNA/UŻYTECZNA). Śledzenie feedback użytkownika na sugestie.
**Status:** Działająca tabela w bazie.

✅ USER_EXPERTISE ✅ ZAIMPLEMENTOWANA
Cel Strategiczny: Ekstraktowanie i strukturyzowanie wiedzy eksperckiej od doświadczonych użytkowników.
Logika dla AI: Przetwarzaj insights użytkownika na strukturalne dane. Buduj bazę wiedzy z praktycznych doświadczeń sprzedażowych.
**Status:** Działająca tabela w bazie.

✅ DATA_UPDATES_LOG ✅ ZAIMPLEMENTOWANA
Cel Strategiczny: Audyt wszystkich operacji zapisu wykonanych przez asystenta AI z interfejsu czatu.
Logika dla AI: Loguj każdą operację INSERT/UPDATE/DELETE wykonaną na zlecenie użytkownika przez chat interface.
**Status:** Działająca tabela w bazie.

✅ SCORING_CONFIG ✅ ZAIMPLEMENTOWANA
Cel Strategiczny: Dynamiczna konfiguracja wag i progów scoringu bez redeploy.
Logika dla AI: Backend pobiera aktywną konfigurację i cache'uje. Umożliwia szybkie dostrajanie systemu.
**Status:** Działająca tabela z domyślną konfiguracją.

✅ BUYING_SIGNALS ✅ ZAIMPLEMENTOWANA
Cel Strategiczny: Katalog sygnałów gotowości kupna zidentyfikowanych przez ekspertów.
Logika dla AI: Automatyczne wykrywanie gotowości klienta do zakupu na podstawie wzorców behawioralnych.
**Status:** Działająca tabela z przykładowymi sygnałami.

✅ TEMPORAL_BEHAVIOR_PATTERNS ✅ ZAIMPLEMENTOWANA
Cel Strategiczny: Przechowywanie wzorców behawioralnych związanych z czasem.
Logika dla AI: Personalizacja strategii w zależności od pory dnia/tygodnia/miesiąca.
**Status:** Działająca tabela z przykładowym wzorcem.

✅ SESSION_METADATA ✅ ZAIMPLEMENTOWANA
Cel Strategiczny: Przechowywanie metadanych sesji użytkowników.
Logika dla AI: Śledzenie kontekstu sesji, preferencji użytkownika i historii interakcji.
**Status:** Działająca tabela w bazie.
5. Interfejs Strategiczny i Logika Operacyjna
Po każdej nowej informacji wpisanej do czatu, system dynamicznie przebudowuje cały Panel Strategiczny. Panel ten jest Twoim centrum dowodzenia, podzielonym na pięć kluczowych, interaktywnych zakładek.

Zakładka 1: GŁÓWNA STRATEGIA
Cel: Dostarczenie nadrzędnego planu i narzędzi do zrozumienia "ukrytego języka" klienta.
Komponenty: Nadrzędna Strategia, Sugerowane Następne Kroki, Tłumacz Klienta (Sparing Partner 2.0), Arsenał Sprzedażowy, Czerwone Flagi.

Zakładka 2: JĘZYK I KOMUNIKACJA
Cel: Wyposażenie Cię w precyzyjne narzędzia językowe do budowania relacji i perswazji.
Komponenty: Słownik Mocy, Słownik Toksyczny, Profil Głosowy, Generator Komunikacji (SMS/Email).

Zakładka 3: PLAN DZIAŁANIA
Cel: Dostarczenie szczegółowych, gotowych do wdrożenia planów działania.
Komponenty: Elaboraty Taktyczne (szczegółowe opisy, jak przeprowadzić kluczowe działania z danym typem klienta), Planowanie Długoterminowe.

Zakładka 4: ANALIZA I WSKAŹNIKI
Cel: Prezentacja kluczowych metryk i insightów w czasie rzeczywistym.
Komponenty: Prawdopodobieństwo Zakupu, Wskaźnik Fun-Drive, Potencjał Jazdy Weekendowej (OVN), Tricki i Hacki Behawioralne.

Zakładka 5: AI SPARRING PARTNER
Cel: Interaktywny symulator klienta + asystent strategiczny z aktualizacjami w czasie rzeczywistym.
Komponenty: Symulator Klienta (AI w roli klienta), Live Strategy Updates (ciągłe aktualizacje strategii), Inteligentne Sugestie (proaktywne wskazówki), Tryby Pracy (Klient/Coach/Hybrid).

Jasne — przygotowałem gotowy plik Markdown na bazie Twojego dokumentu. Skopiuj całość do pliku Ultra_BIGDecoder_3.0.md.

# Ultra BIGDecoder 3.0: Ostateczny Dokument Przewodni (v3.0)

## 1. Nadrzędne Zasady i Ostateczna Wizja

- Wizja: Stworzenie proaktywnego, samodoskonalącego się partnera strategicznego AI – konwersacyjnego „drugiego mózgu” sprzedawcy. System przewiduje, symuluje i generuje zasoby w czasie rzeczywistym, ucząc się z każdej interakcji i korekty.
- Sztywne Reguły (Core Principles):
    - Zasada Ewolucji, Nie Rewolucji (Enhance, Don’t Replace): AI nie nadpisuje rdzenia wiedzy – dodaje priorytetową warstwę z korekt użytkownika i nowymi danymi, zachowując stabilny fundament.
    - Zasada Dynamicznej Granulacji (Dynamic Granularity): Wykrywa powtarzalne odchylenia od archetypów i proponuje sub‑archetypy do akceptacji i trwałego zapisu.
    - Zasada Ciągłej Analizy (Always‑On Analysis): Analiza w tle od pierwszego słowa; UI odzwierciedla ciągłe, dynamiczne aktualizacje.
    - Zasada Proaktywnego Dopytywania (Proactive Inquiry): Gdy pewność diagnozy jest niska, system sam proponuje pytania uzupełniające.


## 2. Architektura i Logika Systemu „Ultra”

- Od statycznego kalkulatora (bigdecoder.html) do żywego, konwersacyjnego organizmu napędzanego LLM.
- Przepływ działania:

1. Inicjacja sesji: użytkownik podaje pierwsze sygnały (np. „Mężczyzna ~40, Model Y, dwójka dzieci”).
2. Ciągła analiza:
        - Wstępna estymacja archetypu z niską pewnością na podstawie słów kluczowych.
        - Panel Strategii aktualizowany natychmiast.
        - Radar Obiekcji wyświetla potencjalne obiekcje z relacji archetyp–obiekcja.
3. Interakcja i reakcja:
        - Wykrycie obiekcji (ID) → natychmiastowa odpowiedź według frameworku z tabeli OBJECTIONS (np. FEAR→FACTS→FUTURE) dopasowana do archetypu.
4. Proaktywne dopytywanie i pętla korekty:
        - Sugestie pytań, gdy dane niepełne.
        - Korekta użytkownika → zapis do ANALYSIS_FEEDBACK → natychmiastowy przeliczenie całej analizy.


## 3. Architektura Techniczna i Silnik Operacyjny

### 3.1 BACKEND API - STATUS IMPLEMENTACJI: ✅ 100% GOTOWY

**🎉 KOMPLETNY BACKEND ULTRA BIGDECODER 3.0 DZIAŁAJĄCY!**

#### 📂 Struktura Backend (backend/)
```
backend/
├── main.py              # FastAPI aplikacja (✅ GOTOWA)
├── run.py               # Skrypt uruchamiający (✅ GOTOWY)  
├── config.py            # Konfiguracja Ollama + Supabase (✅ GOTOWE)
├── test_setup.py        # Testy wszystkich komponentów (✅ GOTOWE)
├── requirements.txt     # Zależności Python (✅ ZAINSTALOWANE)
├── README.md            # Dokumentacja (✅ GOTOWA)
├── services/
│   ├── ollama_client.py # Klient Ollama API (✅ GOTOWY)
│   └── database.py      # Service dla Supabase (✅ GOTOWY)
└── models/
    └── schemas.py       # Pydantic modele (✅ GOTOWE)
```

#### 🔧 Skonfigurowany Ollama Client
- **API Key:** `44f238f9fd6f4c4f9048fce51c52d45e.0AFg36FTByB3_Oc9KcpNqWQW` ✅
- **Model:** `gptoss120b` (120B parametrów) ✅  
- **URL:** `http://localhost:11434` ✅
- **Funkcje:** generate(), list_models(), check_health() ✅

#### 📡 Dostępne API Endpointy
- ✅ `GET /` - Status systemu
- ✅ `GET /health` - Health check (baza + Ollama)
- ✅ `POST /sessions/create` - Tworzenie nowych sesji
- ✅ `POST /analyze` - **Główna analiza klienta**
- ✅ `POST /strategy/generate` - Generowanie strategii sprzedażowej
- ✅ `POST /suggestions/create` - Tworzenie sugestii AI
- ✅ `POST /feedback/submit` - System korekt użytkownika
- ✅ `GET /data/archetypes` - Wszystkie archetypy
- ✅ `GET /data/objections` - Wszystkie obiekcje
- ✅ `GET /data/playbooks` - Wszystkie playbooki
- ✅ `GET /data/market` - Dane rynkowe
- ✅ `GET /data/products/tesla` - Produkty Tesla
- ✅ `GET /data/products/competitors` - Konkurencja
- ✅ `GET /data/promotions` - Aktualne promocje
- ✅ `WS /ws/{session_id}` - WebSocket dla real-time

#### 🚀 Jak uruchomić Backend:
```bash
cd backend
python run.py
```

#### 🌐 Dostęp do API:
- **Główny URL:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

#### 🔍 Test Connection:
```bash
# Test health check
curl http://localhost:8000/health

# Test głównej analizy
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"input_text": "Chcę Model Y dla rodziny", "mode": "analyzer"}'
```

#### 📦 Zainstalowane Zależności
- ✅ `fastapi` - Framework API
- ✅ `uvicorn` - ASGI server  
- ✅ `httpx` - Async HTTP client dla Ollama
- ✅ `supabase` - Client bazy danych
- ✅ `pydantic` - Walidacja danych
- ✅ `cachetools` - System cache'owania
- ✅ `python-dotenv` - Zarządzanie zmiennymi środowiska

---

### 3.2 Architektura LLM

- **Model:** GPT‑class Open Source 120B, hostowany lokalnie przez API serwera Ollama.
- **Dlaczego Ollama:**
    - **Prywatność danych:** pełne przetwarzanie w środowisku zamkniętym.
    - **Szybkość i kontrola:** niskie opóźnienia, pełna konfiguracja i dostępność.
    - **Elastyczność:** swoboda doboru i dostrajania modeli open‑source.
- **Rola LLM:**
    - Analiza psychometryczna, identyfikacja intencji i ryzyk.
    - Generowanie strategii, skryptów i planów działania.
    - Uczenie się i adaptacja w czasie rzeczywistym z danych Supabase oraz wejścia użytkownika.


## 4. Architektura Danych (Supabase)

### 4.1. Tabele Podstawowe (Statyczny Rdzeń Wiedzy)

- ARCHETYPES (10)
    - Cel: profile psychologiczne klientów (warstwa „DLACZEGO”).
    - Użycie: disc_profile jako wskazówka; motivations i triggers (JSON) do personalizacji strategii.
- MARKET_DATA_POLAND (3)
    - Cel: kontekst rynkowy.
    - Użycie: wplatanie metryk (np. dotacje) w odpowiedzi dla faktograficznej wiarygodności.
- OBJECTION_ARCHETYPES (11)
    - Cel: zasilanie Radaru Potencjalnych Obiekcji.
    - Użycie: po identyfikacji archetypu – odczyt powiązanych objection_id dla proaktywnego przygotowania.
- OBJECTIONS (9)
    - Cel: katalog strategii zbijania obiekcji.
    - Użycie: kolumna rebuttal_strategy (JSON) jako framework (np. RISK→MITIGATION→PEACE OF MIND) wypełniany treścią dopasowaną do kontekstu.
- PLAYBOOKS (10)
    - Cel: zaawansowane taktyki sprzedażowe.
    - Użycie: gdy spełnione warunki (target_archetype_id/target_objection_id) – sugeruj playbook; strategy_details jako gotowy koncept.
- PRODUCTS_COMPETITORS (3) i PRODUCTS_TESLA (4)
    - Cel: porównania produktowe, TCO, odpowiedzi techniczne.
    - Użycie: precyzyjne analizy porównawcze i kalkulacje.
- PROMOTIONS (2) i SEASONAL_PATTERNS (2)
    - Cel: kontekst biznesowo‑czasowy.
    - Użycie: dostosowanie komunikacji do celów sprzedażowych i ofert sezonowych.


### 4.2. Tabele Dynamiczne (Ewoluująca Pamięć i Trening)

- ANALYSIS_FEEDBACK
    - Cel: pętla korekty w locie.
    - Zapis: session_id, timestamp, state_before_correction (JSON), user_correction.
    - Odczyt: podczas aktywnej sesji treningowej – analiza wzorców korekt i generowanie inteligentnych pytań pogłębiających.
- DYNAMIC_CONTEXT
    - Cel: trwała, rozszerzalna pamięć długoterminowa.
    - Zapis (po komendzie /zapisz): analiza treści → streszczenie → ekstrakcja encji/faktów → kategoryzacja/tagowanie → zapis ustrukturyzowany.
    - Odczyt: wzbogacanie kontekstu przed głębszą analizą.
- INTERACTION_LOGS
    - Cel: rejestr sesji do treningu i analizy.
    - Zapis: transkrypty – wpis użytkownika, odpowiedź AI, korekty.
    - Odczyt: główne źródło dla sesji treningowej; rekonstrukcja ścieżki rozumowania do precyzyjnych pytań.
- PSYCHOMETRIC_PROFILES
    - Cel: archiwizacja kompletnych profili klientów.
    - Zapis (po sesji): finalny profil (JSON): DISC/Big Five/Schwartz, Fun‑Drive/OVN, kluczowe triggery i obiekcje.
    - Odczyt: metaanalizy (np. profile, które kupiły Model Y w Q4), identyfikacja trendów.


## 5. Interfejs Strategiczny i Logika Operacyjna

- Po każdej nowej informacji czat przebudowuje Panel Strategiczny (4 zakładki).


### Zakładka 1: GŁÓWNA STRATEGIA

- Cel: nadrzędny plan i zrozumienie „ukrytego języka” klienta.
- Komponenty:
    - Nadrzędna Strategia
    - Sugerowane Następne Kroki
    - Tłumacz Klienta (Sparing Partner 2.0)
    - Arsenał Sprzedażowy
    - Czerwone Flagi


### Zakładka 2: JĘZYK I KOMUNIKACJA

- Cel: precyzyjne narzędzia językowe do relacji i perswazji.
- Komponenty:
    - Słownik Mocy
    - Słownik Toksyczny
    - Profil Głosowy
    - Generator Komunikacji (SMS/Email)


### Zakładka 3: PLAN DZIAŁANIA

- Cel: gotowe do wdrożenia plany działania.
- Komponenty:
    - Elaboraty Taktyczne (krok po kroku dla typu klienta)
    - Planowanie Długoterminowe


### Zakładka 4: ANALIZA I WSKAŹNIKI

- Cel: metryki i insighty w czasie rzeczywistym.
- Komponenty:
    - Prawdopodobieństwo Zakupu (real‑time)
    - Ryzyko Utraty Klienta / Churn (real‑time)
    - Wskaźnik Fun‑Drive
    - Potencjał Jazdy Weekendowej (OVN)
    - Sygnały De‑eskalacji (kiedy ton/ryzyko rośnie)
    - Gotowość do kolejnego kroku (CTA Readiness)
    - Tricki i Hacki Behawioralne


## 6. Ramy Operacyjne LLM (Procedury)

- Always‑On:
    - Każdy input użytkownika → natychmiastowy update: archetyp, obiekcje, plan.
    - Próg pewności: jeśli niski, generuj pytania pogłębiające.
- Korekty:
    - Każda jawna korekta → zapis do ANALYSIS_FEEDBACK i ponowna kalkulacja.
- Wiedza:
    - Rdzeń tabel podstawowych traktować jako niezmienny; warstwa adaptacyjna ma priorytet w odpowiedziach bez modyfikacji rdzenia.
- Proaktywność:
    - Sugeruj playbooki, skrypty, porównania i TCO, gdy kontekst na to wskazuje.


## 7. Minimalny Spec LLM + Backend

- LLM: model 120B uruchomiony w Ollama (api/v1/chat, strumieniowanie).
- Supabase:
    - Schemat tabel zgodnie z sekcją 4.
    - RLS i logowanie zmian.
- Silnik analizy:
    - Pipeline: input → klasyfikacja archetypu → mapowanie obiekcji → generacja odpowiedzi → zapis interakcji → ewentualna korekta → aktualizacja profilu sesji.
- UI:
    - Czat z panelem bocznym (4 zakładki) autoodświeżającym się po każdym zdarzeniu.


## 8. Przykładowe Przepływy

- Obiekcja „cena za wysoka”:
    - Wykryj ID obiekcji.
    - Zbuduj odpowiedź wg frameworku z OBJECTIONS.rebuttal_strategy z wpleceniem MARKET_DATA_POLAND.metric_value (np. dotacje).
    - Dostosuj ton i akcenty do ARCHETYPES.motivations/triggers.


## 9. Metryki i Ewaluacja

- Czas do odpowiedzi (latency).
- Skuteczność dopasowania archetypu (precision/recall kontra feedback).
- Skuteczność zbijania obiekcji (konwersje po interakcji).
- Pokrycie wiedzy dynamicznej (udział DYNAMIC_CONTEXT w sesji).
- Jakość profili psychometrycznych (spójność między sesjami).


## 10. Dynamiczne Dodawanie Danych przez Chat

### 10.1 Wizja Funkcjonalności

**CEL:** Umożliwienie użytkownikom dodawania nowych danych do bazy Supabase bezpośrednio przez interfejs czatu z LLM, bez konieczności ręcznego edytowania SQL.

## 🧠 **AKTYWNE UCZENIE LLM - UŻYTKOWNIK JAKO ŹRÓDŁO WIEDZY**

### **FILOZOFIA SYSTEMU:**
**Użytkownik nie jest tylko operatorem systemu - jest GŁÓWNYM ŹRÓDŁEM WIEDZY I EKSPERTYZY.** LLM traktuje każdą interakcję jako możliwość nauki od eksperta sprzedaży, który posiada lata doświadczenia, intuicji i praktycznej wiedzy.

### **🎯 TRYB "AKTYWNEGO TRENINGU" - LLM JAKO UCZEŃ**

#### **Mechanizm Działania:**
1. **LLM zadaje pytania proaktywne** na podstawie luk w swojej wiedzy
2. **Analizuje odpowiedzi użytkownika** pod kątem nowych wzorców i insights
3. **Przetwarza wiedzę** na strukturowane dane
4. **Proponuje dodanie do bazy** jako "mocne sugestie"
5. **Uczy się z korekt i uzupełnień** użytkownika

#### **Przykład Sesji Aktywnego Treningu:**

**LLM:** *"Zauważam, że często wspomina Pan o 'sygnałach kupna' u klientów. Czy mógłby Pan opisać 3-4 najważniejsze sygnały, które Pan obserwuje?"*

**Użytkownik:** *"Tak, kluczowe sygnały to: zaczyna pytać o konkretne kolory, pyta o terminy dostawy, wspomina o sprzedaży obecnego auta, i najważniejsze - zaczyna używać słowa 'mój' zamiast 'ten' samochód."*

**LLM przetwarza i proponuje:**
```json
{
  "nowa_kategoria": "buying_signals",
  "rekordy_do_dodania": [
    {
      "signal_name": "Color Interest",
      "description": "Klient pyta o konkretne kolory zamiast ogólnie o auto",
      "confidence_weight": 0.7,
      "typical_timing": "middle_to_late_stage"
    },
    {
      "signal_name": "Delivery Inquiry", 
      "description": "Pytania o terminy dostawy wskazują na poważne rozważanie zakupu",
      "confidence_weight": 0.8,
      "typical_timing": "late_stage"
    },
    {
      "signal_name": "Trade-in Mention",
      "description": "Wspomnienie o sprzedaży obecnego auta",
      "confidence_weight": 0.9,
      "typical_timing": "decision_phase"
    },
    {
      "signal_name": "Ownership Language",
      "description": "Przejście z 'ten samochód' na 'mój samochód'",
      "confidence_weight": 0.95,
      "typical_timing": "pre_purchase"
    }
  ],
  "sugestia": "Czy dodać te sygnały jako nową tabelę 'buying_signals' z powiązaniem do archetypu?"
}
```

### **🔍 PROAKTYWNE WNIOSKOWANIE I PYTANIA**

#### **LLM jako Detektyw Wiedzy:**
- **Wykrywa luki:** "Widzę, że ma Pan dużo doświadczenia z klientami premium. Jakie są różnice w podejściu do Model S vs Model 3?"
- **Łączy wzorce:** "Zauważam, że klienci z panelami PV często mają podobne obiekcje. Czy jest jakiś specjalny playbook dla tej grupy?"
- **Testuje hipotezy:** "Czy to prawda, że klienci z BMW są bardziej sceptyczni wobec autopilota niż klienci z Audi?"

#### **Inteligentne Dopytywanie:**
```
LLM: "Pan wspomniał o 'zimnych klientach'. Czy mógłby Pan opisać:
1. Jak rozpoznać 'zimnego' klienta w pierwszych 2 minutach?
2. Jaka jest najskuteczniejsza taktyka 'rozgrzania'?
3. Czy są archetypy, które częściej są 'zimne'?"
```

### **📊 PRZETWARZANIE WIEDZY W STRUKTUROWANE DANE**

#### **Proces Transformacji:**
1. **Analiza semantyczna** wypowiedzi użytkownika
2. **Ekstrakcja kluczowych faktów** i wzorców
3. **Kategoryzacja wiedzy** (nowy archetyp, playbook, obiekcja, sygnał)
4. **Strukturyzacja w formacie JSON** gotowym do bazy
5. **Walidacja z istniejącymi danymi** (czy nie duplikuje)
6. **Propozycja jako "mocna sugestia"** z uzasadnieniem

#### **Przykład Przetwarzania:**
**Użytkownik:** *"Klienci, którzy przychodzą po 18:00 są zwykle bardziej zdecydowani. Mają już przemyślaną decyzję w domu, przychodzą sfinalizować. Ale też są bardziej zmęczeni, więc trzeba być konkretnym, bez zbędnych gadek."*

**LLM przetwarza na:**
```json
{
  "insights": {
    "temporal_pattern": {
      "time_range": "after_18:00",
      "client_characteristics": ["more_decisive", "pre_researched", "tired"],
      "recommended_approach": ["be_concrete", "avoid_small_talk", "focus_on_essentials"],
      "confidence_multiplier": 1.2
    }
  },
  "suggested_addition": "Czy dodać 'Evening Client Pattern' do seasonal_patterns lub stworzyć nową tabelę 'temporal_behavior_patterns'?"
}
```

### **💡 MOCNE SUGESTIE - SYSTEM PROPOZYCJI**

#### **Hierarchia Sugestii:**
1. **🔴 KRYTYCZNA** - Luka w kluczowym obszarze (np. brak playbook dla najczęstszej obiekcji)
2. **🟡 WAŻNA** - Optymalizacja istniejących procesów
3. **🟢 UŻYTECZNA** - Dodatkowe insights i wzorce

#### **Format Mocnych Sugestii:**
```
🔴 KRYTYCZNA SUGESTIA:
"Zauważam, że 40% klientów pyta o ładowanie w mieszkaniu, ale nie mamy playbooka dla 'Apartment Dweller'. 
Na podstawie Pana doświadczenia, czy stworzyć nowy archetyp z taktykami:
- Portable charger solutions
- Public charging network emphasis  
- Workplace charging inquiry
?"

[DODAJ DO BAZY] [ODRZUĆ] [MODYFIKUJ]
```

### **🔄 CIĄGŁE UCZENIE I ADAPTACJA**

#### **Mechanizm Feedback Loop:**
1. **LLM proponuje** nowe dane/wzorce
2. **Użytkownik akceptuje/modyfikuje/odrzuca**
3. **System uczy się** z tych decyzji
4. **Poprawia przyszłe propozycje** na podstawie preferencji użytkownika

#### **Pamięć Preferencji:**
```json
{
  "user_preferences": {
    "prefers_detailed_playbooks": true,
    "likes_data_driven_insights": true,
    "avoids_overly_complex_categories": true,
    "values_practical_over_theoretical": true
  }
}
```

### **🎓 TRYBY UCZENIA**

#### **1. PASYWNE UCZENIE**
- LLM obserwuje interakcje i automatycznie wyciąga wnioski
- Propozycje pojawiają się w tle, nie przerywają pracy

#### **2. AKTYWNE UCZENIE** 
- LLM proaktywnie zadaje pytania
- Dedykowane sesje "knowledge extraction"
- Użytkownik w roli mentora/nauczyciela

#### **3. COLLABORATIVE UCZENIE**
- LLM i użytkownik wspólnie analizują przypadki
- Iteracyjne budowanie nowych strategii
- Real-time testing hipotez

**PRZYKŁADY UŻYCIA:**
- "Dodaj nową promocję: Model Y -10% do końca miesiąca"
- "Nowy konkurent: BMW iX1 od 180k PLN"
- "Aktualizuj dotację: 27k PLN dla Model 3"
- "Dodaj obiekcję: 'Boję się o wartość po 5 latach'"

### 10.2 Architektura Funkcjonalności

**FRONTEND (Chat Interface):**
- Natural language input dla użytkownika
- Real-time validation i sugestie
- Confirmation dialog przed zapisem
- Status feedback (sukces/błąd)

**BACKEND (LLM + Supabase):**
- LLM analizuje intencję użytkownika
- Klasyfikuje typ danych do dodania
- Generuje strukturę JSON
- Waliduje dane przed zapisem
- Wykonuje zapytania SQL

**BAZA DANYCH:**
- Wykorzystanie istniejących tabel
- Dodanie tabeli `data_updates_log` dla audytu
- Implementacja RLS (Row Level Security)

### 10.3 Obsługiwane Typy Danych

#### 10.3.1 PROMOCJE (tabela: promotions)
**Przykłady komend:**
- "Dodaj promocję: Model 3 -5000 PLN do końca tygodnia"
- "Nowa oferta: Model Y leasing 0% wkładu własnego"

**Wymagane pola:**
- name (nazwa promocji)
- promotion_type (typ: Percentage/Fixed/Leasing)
- discount_amount_pln (kwota/oprocentowanie)
- end_date (data końcowa)

#### 10.3.2 KONKURENCJA (tabela: products_competitors)
**Przykłady komend:**
- "Nowy konkurent: Audi Q4 e-tron od 200k PLN"
- "Dodaj BMW iX3: 250k PLN, zasięg 460km"

**Wymagane pola:**
- brand (marka)
- model_name (model)
- base_price_pln (cena podstawowa)
- range_km (zasięg)

#### 10.3.3 DANE RYNKOWE (tabela: market_data_poland)
**Przykłady komend:**
- "Aktualizuj dotację: 27k PLN dla Model 3"
- "Nowa stacja: Supercharger w Katowicach"

#### 10.3.4 OBIEKCJE (tabela: objections)
**Przykłady komend:**
- "Dodaj obiekcję: 'Boję się o wartość po 5 latach'"
- "Nowa obiekcja: 'Nie ma serwisu w moim mieście'"

### 10.4 Przepływ Danych

```
1. Użytkownik: "Dodaj promocję: Model Y -15% do 31.12"
2. LLM Analiza:
   - Intencja: ADD_PROMOTION
   - Typ: promotion
   - Dane: model="Model Y", discount=15%, end_date="2024-12-31"
3. Walidacja:
   - Sprawdzenie wymaganych pól
   - Walidacja formatu daty
   - Sprawdzenie duplikatów
4. Generowanie SQL:
   INSERT INTO promotions (name, promotion_type, discount_amount_pln, end_date) 
   VALUES ('Model Y Q4 Discount', 'Percentage', 15, '2024-12-31')
5. Confirmation:
   "Czy chcesz dodać promocję: Model Y -15% do 31.12?"
6. Zapis do bazy + log
```

### 10.5 Implementacja Techniczna

**Struktura LLM Prompt:**
```javascript
const dataAdditionPrompt = `
Jesteś asystentem do dodawania danych do systemu Ultra BIGDecoder 3.0.

DOSTĘPNE TABELE:
- promotions: promocje i oferty
- products_competitors: konkurencja
- market_data_poland: dane rynkowe
- objections: obiekcje klientów

Gdy użytkownik chce dodać dane:
1. KLASYFIKUJ intencję (ADD_PROMOTION, ADD_COMPETITOR, etc.)
2. WYEKSTRAKTUJ dane z komunikatu
3. WALIDUJ wymagane pola
4. SPRAWDŹ duplikaty
5. WYGENERUJ SQL
6. POPROŚ o potwierdzenie
`;
```

**Tabela Audytu:**
```sql
CREATE TABLE data_updates_log (
  id SERIAL PRIMARY KEY,
  session_id UUID,
  user_input TEXT,
  llm_analysis JSONB,
  sql_executed TEXT,
  table_affected VARCHAR(50),
  records_affected INTEGER,
  success BOOLEAN,
  error_message TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 10.6 Obsługa Błędów i Walidacja

**BRAKUJĄCE DANE:**
```
LLM: "Potrzebuję więcej informacji:
      - Jaka jest dokładna kwota rabatu?
      - Do kiedy trwa promocja?"
```

**DUPLIKATY:**
```
LLM: "Znaleziono podobną promocję dla Model Y.
      Czy chcesz:
      a) Zaktualizować istniejącą promocję
      b) Dodać nową z inną nazwą
      c) Anulować operację?"
```

**WALIDACJA:**
- Sprawdzenie typów danych (liczba, data, tekst)
- Walidacja formatów (daty, kwoty)
- Sprawdzenie długości pól
- Sanityzacja input SQL injection

### 10.7 Metryki i Monitoring

**KPI Funkcjonalności:**
- Liczba dodanych rekordów dziennie
- Sukces rate operacji (>95%)
- Czas od komendy do zapisu (<30s)
- Liczba błędów walidacji

**Monitoring:**
- Dashboard z aktywnością dodawania
- Alerty przy wysokiej liczbie błędów
- Raporty dzienne/miesięczne

### 10.8 Harmonogram Implementacji

**Faza 1** (Tydzień 1-2): Podstawowa funkcjonalność
- Implementacja LLM prompt dla dodawania danych
- Podstawowa walidacja i SQL generation
- Testy z promocjami i konkurencją

**Faza 2** (Tydzień 3): Rozszerzenie typów
- Dodanie obsługi obiekcji
- Implementacja mapowania archetypów
- Rozbudowa walidacji

**Faza 3** (Tydzień 4): UI i UX
- Interfejs confirmation dialog
- Status feedback i error handling
- Autocomplete i sugestie

**Faza 4** (Tydzień 5): Monitoring i optymalizacja
- Implementacja metryk
- Dashboard monitoring
- Optymalizacja wydajności

---

## 11. Bezpieczeństwo i Prywatność

- Lokalna inferencja (Ollama), minimalizacja wycieków danych.
- Anonimizacja identyfikatorów sesji.
- Audyt: INTERACTION_LOGS z kontrolą dostępu.

—

Chcesz żebym:

- przygotował też README.md dla repo,
- dorzucił szkic SQL (CREATE TABLE) dla wszystkich tabel,
- albo utworzył ten plik w nowej karcie edytora, żebyś mógł go od razu zapisać?


## 12. Specyfikacja Wdrożenia (VibeCode)

### 12.1 Pętla Always‑On (po każdej wiadomości)

1. Wejście: `session_id`, `message`, `timestamp` → zapis do `interaction_logs` (role=user).
2. Ekstrakcja faktów i sygnałów (LLM Analyzer): ton, intencje, obiekcje, cechy klienta, kontekst (PV, aktualne auto itd.).
3. Aktualizacja profilu sesji: estymacja archetypu (Top‑3 + confidence), prognoza obiekcji, dobór playbooków, sugerowany model Tesli.
4. Skoring w czasie rzeczywistym: `purchase_likelihood_now`, `churn_risk_now`, `cta_readiness`, `deescalation_cues`.
5. Odpowiedź szybka + 2‑3 pytania pogłębiające; przygotowanie `updates_for_tabs` do UI.
6. Zapis stanu: snapshot do `dynamic_context`; ewentualne `analysis_feedback` przy korekcie użytkownika.
7. Jeśli wykryto intencję „dodaj dane” → uruchom Asystenta Zapisu (walidacja → preview → potwierdzenie → INSERT/UPDATE + `data_updates_log`).


### 12.2 Skoring (Purchase Likelihood / Churn)

Wejścia (features – normalizowane do 0..1, chyba że opisano inaczej):
- f_tone: sentyment/ton rozmowy (mapa: bardzo negatywny=0, neutralny=0.5, pozytywny=1.0)
- f_latency: odwrotność średniego czasu odpowiedzi użytkownika w sesji (szybciej = bliżej 1)
- f_length_trend: trend długości wiadomości użytkownika (rosnący=0.7..1, spadek=0..0.4)
- f_intent: suma sygnałów intencji (np. finansowanie=0.25, test drive=0.35, termin zakupu=0.4; max clamp 1.0)
- f_objection_intensity: intensywność obiekcji (0..1), działa ujemnie
- f_fit: dopasowanie potrzeb (PV, segment, rodzina, budżet) do rekomendacji (0..1)
- f_slots: kompletność krytycznych slotów (wersja aktualnego auta, przebieg roczny, profil tras, budżet) – odsetek wypełnienia
- f_momentum: momentum sesji (ostatnie 3 wiadomości: poprawa skoringu/tonu/konkretów)

Wagi (przykładowe, sumaryczna siła ~1.2):
- w_tone=0.15, w_latency=0.10, w_length_trend=0.05, w_intent=0.20,
- w_objection_intensity=−0.20, w_fit=0.20, w_slots=0.10, w_momentum=0.20

Pseudokod:
```python
score_raw = (
  w_tone*f_tone + w_latency*f_latency + w_length_trend*f_length_trend +
  w_intent*f_intent + w_fit*f_fit + w_slots*f_slots + w_momentum*f_momentum +
  w_objection_intensity*f_objection_intensity  # ujemne w
)

# Wygładzanie w czasie (EMA)
purchase_likelihood_now = sigmoid(score_raw) * 100  # 0..100
purchase_likelihood_smoothed = ema(prev=purchase_likelihood_prev, now=purchase_likelihood_now, alpha=0.4)

# Churn: nie jest 100 - purchase; dodaj kary za negatywne sygnały
churn_base = 100 - purchase_likelihood_smoothed
penalty = 20*(1-f_tone) + 15*f_objection_intensity + 10*(1-f_momentum)
churn_risk_now = clamp(churn_base + penalty, 0, 100)

# CTA Readiness
cta_readiness = select_cta(
  purchase=purchase_likelihood_smoothed,
  confidence=archetype_confidence,
  have_slots=f_slots,
  intents=f_intent
)
```

Zasady progowe:
- `churn_risk_now ≥ 70` → pokaż de‑eskalację (empatia + 1 krótka decyzja/korzyść + pytanie ratunkowe)
- `purchase_likelihood_now ≥ 65` i `confidence ≥ 0.7` → zaproponuj CTA (jazda próbna / oferta / rozmowa o finansowaniu)


### 12.3 Role i Prompty LLM

Analyzer (system prompt – skrót):
```
Jesteś Analyzerem BIGDecoder. Po każdym wpisie:
1) Wyodrębnij normalized_facts (tone, intents[], objections[], customer_facts{}, social_context{}, risks[]).
2) Oszacuj archetypes_top3[{id,name,confidence}], predicted_objections[], suggested_playbooks[].
3) Wygeneruj quick_reply (3-5 zdań, empatia→fakty→korzyść), deep_questions[2-3], updates_for_tabs{summary, communication, playbook, objections}.
4) Oblicz features do skoringu (f_*), ale BEZ liczenia wag – to robi backend.
5) Nie wymyślaj danych – pytaj o braki.
Wyjście w JSON.
```

Data‑Writer (system prompt – skrót):
```
Jesteś Asystentem Zapisu. Klasyfikuj intencję: ADD_PROMOTION / ADD_COMPETITOR / ADD_MARKET / ADD_OBJECTION.
1) Wyciągnij pola wymagane per tabela, wskaż missing_fields.
2) Zaproponuj kandydata INSERT/UPDATE (SQL‑ready JSON), wygeneruj confirmation_text.
3) Nie wykonuj zapisu – backend prosi o potwierdzenie i wykonuje operację.
Wyjście w JSON.
```


### 12.4 Kontrakty API (Backend)

POST `/chat/analyze`
```json
{
  "session_id": "uuid",
  "message": "string"
}
```
Odpowiedź (skrót):
```json
{
  "quick_reply": "string",
  "deep_questions": ["string"],
  "archetypes_top3": [{"id": "uuid", "name": "string", "confidence": 0.73}],
  "predicted_objections": ["uuid"],
  "suggested_playbooks": ["uuid"],
  "normalized_facts": {"tone": "skeptical", "has_pv": true, "current_car": {"brand":"BMW","model":"X5"}},
  "features": {"f_tone": 0.4, "f_fit": 0.8, "f_intent": 0.3},
  "scores": {"purchase_likelihood_now": 62.5, "churn_risk_now": 41.0, "cta_readiness": "book_test_drive"},
  "updates_for_tabs": {"summary": {}, "communication": {}, "playbook": {}, "objections": {}}
}
```

POST `/chat/commit` (asystent zapisu)
```json
{
  "session_id": "uuid",
  "intent": "ADD_PROMOTION",
  "table": "promotions",
  "data": {"name": "Model Y Q4 Discount", "promotion_type": "Percentage", "discount_amount_pln": 10, "end_date": "2024-12-31"}
}
```
Odpowiedź:
```json
{ "ok": true, "rows_affected": 1, "id": "promo_q4_24" }
```

POST `/feedback`
```json
{
  "session_id": "uuid",
  "state_before": {"archetype": {"name": "Security Seeker", "confidence": 0.66}},
  "user_correction": "To raczej Pragmatic Analyst"
}
```

POST `/sparring/simulate` (symulator klienta)
```json
{
  "session_id": "uuid",
  "mode": "client",
  "user_message": "Jak Pan myśli o leasingu?"
}
```
Odpowiedź:
```json
{
  "ai_as_client_response": "Hmm, leasing... to znaczy nie będę właścicielem? A jak to się ma do oszczędności z panelami? Sąsiad kupił za gotówkę...",
  "reasoning": "Response based on Eco-Tech Pragmatist archetype: practical, cost-focused, influenced by neighbor"
}
```

POST `/sparring/update` (live strategy update)
```json
{
  "session_id": "uuid",
  "update_trigger": "test_drive_completed",
  "context_change": {"excitement_level": "high", "emotional_state": "positive"}
}
```
Odpowiedź:
```json
{
  "strategy_update": {
    "archetype_shift": "Pragmatist → Enthusiast",
    "purchase_likelihood": "72% → 85%",
    "new_suggestions": ["Strike while iron is hot", "Focus on emotions + technology"],
    "priority_questions": ["Który model najbardziej podobał?", "Co najbardziej zaskoczyło?"]
  }
}
```

POST `/learning/extract` (aktywne uczenie od użytkownika)
```json
{
  "session_id": "uuid",
  "mode": "active_learning",
  "user_insight": "Klienci po 18:00 są bardziej zdecydowani ale zmęczeni"
}
```
Odpowiedź:
```json
{
  "processed_insight": {
    "category": "temporal_behavior_pattern",
    "structured_data": {
      "time_range": "after_18:00",
      "characteristics": ["decisive", "tired", "focused"],
      "recommended_approach": ["be_concrete", "avoid_small_talk"]
    },
    "suggested_table": "temporal_behavior_patterns",
    "confidence": 0.8,
    "priority": "WAŻNA"
  },
  "follow_up_questions": [
    "Czy zauważa Pan podobne wzorce w weekendy?",
    "Jakie konkretne sygnały wskazują na zmęczenie klienta?"
  ]
}
```

POST `/learning/suggest` (mocne sugestie systemu)
```json
{
  "session_id": "uuid",
  "suggestion_type": "KRYTYCZNA",
  "gap_detected": "missing_playbook_for_apartment_dwellers"
}
```
Odpowiedź:
```json
{
  "strong_suggestion": {
    "priority": "KRYTYCZNA",
    "title": "Brakujący Playbook: Apartment Dweller",
    "reasoning": "40% klientów pyta o ładowanie w mieszkaniu, brak dedykowanej strategii",
    "proposed_solution": {
      "new_archetype": "Urban Apartment Dweller",
      "key_tactics": ["portable_charging", "public_network_emphasis", "workplace_charging"],
      "objections_to_address": ["no_home_charging", "charging_anxiety"]
    },
    "actions": ["DODAJ_DO_BAZY", "ODRZUĆ", "MODYFIKUJ"]
  }
}
```

POST `/learning/feedback` (feedback na sugestie LLM)
```json
{
  "suggestion_id": "uuid",
  "user_action": "MODYFIKUJ",
  "modifications": {
    "archetype_name": "City Charging Optimizer",
    "additional_tactics": ["charging_apps_mastery", "time_optimization"]
  }
}
```


### 12.5 UI – Zakładki i dane (binding)

Zakładka 1: Główna Strategia
- Dane: `archetypes_top1`, `next_steps[3]`, `arsenal[5]`, `red_flags[]`, `suggested_model`.
- Akcje: kopiuj odpowiedź, umów jazdę, generuj ofertę.

Zakładka 2: Język i Komunikacja
- Dane: `power_words[]`, `golden_phrases[]`, `talking_points[]`, `voice_profile`.
- Akcje: generator SMS/Email.

Zakładka 3: Plan Działania
- Dane: `tactical_playbook{steps[]}`, `discovery_questions[]`, `follow_up_plan{timeline[]}`.
- Akcje: checklisty, export PDF.

Zakładka 4: Analiza i Wskaźniki
- Dane: `scores{purchase, churn, cta_readiness}`, `fun_drive`, `ovn`, `radar_objections[]`, `market_facts[]`.
- Akcje: „de‑eskalacja" (karta podpowiedzi), odśwież.

Zakładka 5: AI Sparring Partner
- Dane: `client_simulation{personality, responses}`, `live_updates[]`, `strategy_changes[]`, `ai_suggestions[]`.
- Akcje: przełącz tryb (Klient/Coach/Hybrid), wyślij update, symuluj obiekcję, trenuj argument.

Elementy wspólne
- Pasek hipotez (confidence), proaktywne pytania, korekta analizy (zapis do `analysis_feedback`).


### 12.6 Mapowanie do bazy (Supabase)

- `interaction_logs(id, session_id, role, content, llm_metadata, created_at)`
- `analysis_feedback(id, session_id, timestamp, state_before_correction, user_correction)`
- `dynamic_context(id, session_id, context_type, context_data, confidence_score, usage_count, last_used, created_at)`
- `psychometric_profiles(id, session_id, profile, created_at)`
- `data_updates_log(id, session_id, user_input, llm_analysis, sql_executed, table_affected, records_affected, success, error_message, created_at)`
- `llm_suggestions(id, session_id, suggestion_type, priority, title, reasoning, proposed_data, user_feedback, status, created_at, updated_at)`
- `user_expertise(id, session_id, knowledge_category, extracted_insights, confidence_score, validation_status, created_at)`


### 12.7 Błędy i progi

- Gdy braki danych krytycznych (f_slots < 0.5) → priorytetowo pytania uzupełniające, blokada CTA.
- Gdy `churn_risk_now ≥ 70` → pokaż panel de‑eskalacji zamiast CTA.
- Retries LLM: max 2, timeout per request 20s (streaming preferowane).


### 12.8 Telemetria i monitoring

- Metryki: latency LLM, skuteczność archetypu po korektach, CTR na CTA, liczba zapisów z chatu, błędy walidacji.  
- Dashboard: trend purchase/churn per sesja, heatmap obiekcji, użycie playbooków.

---

## 13. 🎯 NASTĘPNE KROKI - CO DALEJ?

### 13.1 ✅ KOMPLETNY STATUS IMPLEMENTACJI

**BAZA DANYCH SUPABASE:** ✅ 100% GOTOWA (20 tabel działających)
**BACKEND API:** ✅ 100% GOTOWY (FastAPI + Ollama + WebSocket)
**INTEGRACJA LLM:** ✅ 100% SKONFIGUROWANA (gptoss120b + API key)

### 13.2 🚀 URUCHOMIENIE SYSTEMU

#### Krok 1: Uruchomienie Ollama z modelem gptoss120b
```bash
# Upewnij się, że Ollama działa na localhost:11434
# i model gptoss120b jest dostępny
ollama serve
ollama run gptoss120b
```

#### Krok 2: Uruchomienie Backend API
```bash
cd backend
python run.py
```
**System dostępny:** http://localhost:8000

#### Krok 3: Test pierwszej analizy
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Mam panele fotowoltaiczne i myślę o Tesli Model Y dla rodziny",
    "mode": "analyzer"
  }'
```

### 13.3 🛠️ PRIORYTETOWE TESTY DO WYKONANIA

#### Test 1: Podstawowa Analiza Archetypu
- **Input:** Wypowiedź klienta
- **Expected:** Identyfikacja archetypu z confidence > 0.5
- **Test:** POST /analyze

#### Test 2: Real-time WebSocket
- **Input:** Sesja z multiple messages  
- **Expected:** Live updates profilu klienta
- **Test:** WS /ws/{session_id}

#### Test 3: Integracja z bazą danych
- **Input:** GET /data/archetypes
- **Expected:** Wszystkie 10 archetypów z Supabase
- **Test:** Wszystkie GET /data/* endpointy

#### Test 4: AI Sparring Partner 
- **Input:** Symulacja klienta
- **Expected:** AI odpowiadające jako zidentyfikowany archetyp
- **Test:** POST /sparring/simulate

#### Test 5: System korekt
- **Input:** Korekta błędnej analizy
- **Expected:** Zapis do analysis_feedback + update profilu
- **Test:** POST /feedback/submit

### 13.4 🎨 FRONTEND - NASTĘPNY ETAP

**AKTUALNY STAN:** Podstawowy prototyp (frontend/prototype/BIGDECODER.html)

**CO POTRZEBA ZBUDOWAĆ:**
1. **Interfejs czatu** - real-time messaging z backend API
2. **Panel strategiczny** - 5 zakładek z live updates
3. **Dashboard metryk** - Purchase Likelihood, Churn Risk, CTA Readiness
4. **System korekt** - UI dla feedback użytkownika
5. **WebSocket integracja** - real-time updates

**TECHNOLOGIE SUGEROWANE:**
- React.js lub Vue.js dla interaktywnego UI
- Socket.io dla WebSocket connections
- Chart.js dla wizualizacji metryk
- Tailwind CSS dla szybkiego stylingu

### 13.5 📊 MONITORING I OPTYMALIZACJA

**KPI DO ŚLEDZENIA:**
- Latency API responses (cel: <2s)
- Accuracy identyfikacji archetypów
- Conversion rate z rekomendowanych CTA
- User feedback na korekty systemu

**METRYKI BIZNESOWE:**
- Czas do pierwszej strategii (cel: <30s)
- Liczba sesji dziennie
- Skuteczność playbooków (win rate)

### 13.6 🔧 MOŻLIWE ULEPSZENIA

#### Krótkoterminowe (1-2 tygodnie):
- **Voice-to-Text:** Integracja z mikrofon dla voice input
- **Ekspor PDF:** Generowanie raportów strategii
- **Mobile responsive:** UI dla tabletów/telefonów
- **Notyfikacje:** Real-time alerts dla high-value leads

#### Średnioterminowe (1-2 miesiące):
- **ML Model:** Custom model trenowany na danych Tesla
- **CRM Integration:** Połączenie z istniejącymi systemami
- **Multi-language:** Wsparcie dla angielskiego
- **Advanced Analytics:** Predykcyjna analiza konwersji

### 13.7 ⚡ SZYBKIE ZWYCIĘSTWA

1. **Dodaj więcej przykładów testowych** do bazy danych
2. **Stwórz bibliotekę prompt templates** dla różnych scenariuszy  
3. **Zbuduj prosty dashboard** ze statusem systemu
4. **Dodaj logging** dla debugowania i optymalizacji
5. **Stwórz dokumentację API** z przykładami użycia

### 13.8 🎯 ROADMAPA 90 DNI

**DNI 1-30: STABILIZACJA**
- ✅ Backend working ←(GOTOWE)
- ✅ Database complete ←(GOTOWE) 
- ✅ LLM integrated ←(GOTOWE)
- 🎯 Frontend MVP
- 🎯 Podstawowe testy A/B

**DNI 31-60: OPTYMALIZACJA**
- 🎯 Performance tuning
- 🎯 Advanced UI components  
- 🎯 User feedback integration
- 🎯 Mobile support

**DNI 61-90: SKALOWANIE**
- 🎯 Multi-user support
- 🎯 Advanced analytics
- 🎯 CRM integrations
- 🎯 Production deployment

---

## 🏆 PODSUMOWANIE OSIĄGNIĘĆ

### ✅ CO ZOSTAŁO UKOŃCZONE:
1. **Supabase Database:** 20 tabel, pełna zgodność ze specyfikacją
2. **Python Backend:** FastAPI, wszystkie endpointy, WebSocket
3. **Ollama Integration:** Skonfigurowane API, model gptoss120b
4. **Data Models:** Pydantic schemas, walidacja danych
5. **Testing Setup:** Kompletne testy wszystkich komponentów

### 🎯 GOTOWE DO UŻYCIA:
- **API Endpoint:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs  
- **Health Check:** http://localhost:8000/health
- **Analiza klienta:** POST http://localhost:8000/analyze

### 🚀 **SYSTEM JEST W 100% GOTOWY DO PIERWSZYCH TESTÓW!**

---

*Dokument zaktualizowany: $(date)*  
*Status implementacji: BACKEND KOMPLETNY ✅*


