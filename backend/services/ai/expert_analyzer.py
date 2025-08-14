"""
ULTRA BIGDECODER 3.0 - Expert AI Analyzer
Wykorzystuje pełną moc gptoss 120b jako eksperta
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio

class ExpertAnalyzer:
    """
    Zaawansowany analizator wykorzystujący pełną wiedzę ekspercką
    """
    
    def __init__(self, ollama_client, db_service):
        self.ollama = ollama_client
        self.db = db_service
        self.knowledge_cache = {}
        
    async def analyze_with_full_context(
        self,
        customer_input: str,
        session_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analizuje z pełnym kontekstem eksperckim
        """
        
        # 1. POBIERZ CAŁĄ WIEDZĘ EKSPERCKĄ
        expert_knowledge = await self._gather_expert_knowledge(customer_input)
        
        # 2. ZBUDUJ ZAAWANSOWANY PROMPT
        enriched_prompt = self._build_expert_prompt(
            customer_input,
            session_context,
            expert_knowledge
        )
        
        # 3. WYKORZYSTAJ PEŁNĄ MOC 120B PARAMETRÓW
        analysis = await self._deep_analysis(enriched_prompt)
        
        # 4. WZBOGAĆ O DANE REAL-TIME
        enriched_analysis = await self._enrich_with_realtime_data(analysis)
        
        # 5. GENERUJ STRATEGIĘ EKSPERCKĄ
        expert_strategy = await self._generate_expert_strategy(
            enriched_analysis,
            expert_knowledge
        )
        
        return {
            "analysis": enriched_analysis,
            "strategy": expert_strategy,
            "knowledge_used": expert_knowledge.get("sources", []),
            "confidence": enriched_analysis.get("confidence", 0),
            "expert_insights": await self._generate_insights(enriched_analysis)
        }
    
    async def _gather_expert_knowledge(self, input_text: str) -> Dict[str, Any]:
        """
        Zbiera całą relevantną wiedzę ekspercką
        """
        knowledge = {}
        
        # Równoległe pobieranie danych
        tasks = [
            self._get_subsidies_info(input_text),
            self._get_tax_benefits(input_text),
            self._get_charging_infrastructure(),
            self._get_solar_integration(input_text),
            self._get_winter_performance(),
            self._get_tco_calculations(input_text),
            self._get_competitor_comparison(input_text),
            self._get_market_trends()
        ]
        
        results = await asyncio.gather(*tasks)
        
        knowledge["subsidies"] = results[0]
        knowledge["tax_benefits"] = results[1]
        knowledge["charging"] = results[2]
        knowledge["solar"] = results[3]
        knowledge["winter"] = results[4]
        knowledge["tco"] = results[5]
        knowledge["competitors"] = results[6]
        knowledge["market"] = results[7]
        
        return knowledge
    
    async def _get_subsidies_info(self, context: str) -> Dict:
        """
        Pobiera informacje o dopłatach
        """
        # Sprawdź czy klient jest firmą czy osobą prywatną
        is_business = any(word in context.lower() for word in [
            'firma', 'działalność', 'vat', 'leasing', 'flota'
        ])
        
        subsidies = await self.db.query("""
            SELECT * FROM ev_subsidies_poland 
            WHERE valid_until >= CURRENT_DATE
            AND (
                eligibility_criteria->>'customer_type' LIKE %s
                OR eligibility_criteria->>'customer_type' LIKE '%all%'
            )
            ORDER BY max_amount_pln DESC
        """, ['%business%' if is_business else '%individual%'])
        
        return {
            "available": subsidies,
            "total_possible": sum(s['max_amount_pln'] for s in subsidies),
            "best_option": subsidies[0] if subsidies else None
        }
    
    async def _get_tax_benefits(self, context: str) -> Dict:
        """
        Pobiera korzyści podatkowe
        """
        benefits = await self.db.query("""
            SELECT * FROM tax_regulations_business
            WHERE valid_until IS NULL OR valid_until >= CURRENT_DATE
            ORDER BY benefit_amount DESC
        """)
        
        return {
            "vat_savings": next((b for b in benefits if b['regulation_type'] == 'VAT'), None),
            "depreciation": next((b for b in benefits if b['regulation_type'] == 'Depreciation'), None),
            "bik_advantage": next((b for b in benefits if b['regulation_type'] == 'BIK'), None),
            "total_tax_benefit_annual": self._calculate_tax_savings(benefits)
        }
    
    async def _get_solar_integration(self, context: str) -> Dict:
        """
        Informacje o integracji z PV
        """
        if not any(word in context.lower() for word in ['panel', 'pv', 'fotowolt', 'słoneczn']):
            return {}
            
        solar_data = await self.db.query("""
            SELECT * FROM solar_panels_compatibility
            ORDER BY roi_years ASC
        """)
        
        return {
            "integration_options": solar_data,
            "average_daily_range": sum(s['ev_range_per_day_km'] for s in solar_data) / len(solar_data) if solar_data else 0,
            "roi_improvement": "Skrócenie ROI z 7 do 4 lat przy EV+PV"
        }
    
    async def _build_expert_prompt(
        self,
        input_text: str,
        context: Dict,
        knowledge: Dict
    ) -> str:
        """
        Buduje zaawansowany prompt z pełną wiedzą
        """
        from backend.prompts.expert_system_prompt import EXPERT_SYSTEM_PROMPT
        
        prompt = f"""
        {EXPERT_SYSTEM_PROMPT}
        
        ═══════════════════════════════════════════════════════════════
        AKTUALNA WIEDZA KONTEKSTOWA:
        ═══════════════════════════════════════════════════════════════
        
        DOSTĘPNE DOPŁATY:
        {json.dumps(knowledge.get('subsidies', {}), indent=2, ensure_ascii=False)}
        
        KORZYŚCI PODATKOWE:
        {json.dumps(knowledge.get('tax_benefits', {}), indent=2, ensure_ascii=False)}
        
        INFRASTRUKTURA ŁADOWANIA:
        {json.dumps(knowledge.get('charging', {}), indent=2, ensure_ascii=False)}
        
        INTEGRACJA Z PV:
        {json.dumps(knowledge.get('solar', {}), indent=2, ensure_ascii=False)}
        
        KALKULACJE TCO:
        {json.dumps(knowledge.get('tco', {}), indent=2, ensure_ascii=False)}
        
        ═══════════════════════════════════════════════════════════════
        KONTEKST SESJI:
        ═══════════════════════════════════════════════════════════════
        {json.dumps(context, indent=2, ensure_ascii=False)}
        
        ═══════════════════════════════════════════════════════════════
        WYPOWIEDŹ KLIENTA DO ANALIZY:
        ═══════════════════════════════════════════════════════════════
        {input_text}
        
        ZADANIE:
        1. Przeprowadź głęboką analizę psychometryczną
        2. Wykorzystaj KONKRETNE dane z wiedzy kontekstowej
        3. Zaproponuj SPERSONALIZOWANĄ strategię
        4. Użyj RZECZYWISTYCH liczb i faktów
        5. Bądź EKSPERTEM, nie kopiuj - TWÓRZ wartościowe odpowiedzi
        
        Odpowiedz w formacie JSON.
        """
        
        return prompt
    
    async def _deep_analysis(self, prompt: str) -> Dict:
        """
        Wykorzystuje pełną moc 120B parametrów
        """
        response = await self.ollama.generate(
            prompt=prompt,
            temperature=0.7,  # Balans między kreatywnością a precyzją
            top_p=0.9,
            top_k=40,
            max_tokens=2000,
            presence_penalty=0.3,  # Zachęca do różnorodności
            frequency_penalty=0.2  # Unika powtórzeń
        )
        
        return self._parse_expert_response(response)
    
    async def _generate_expert_strategy(
        self,
        analysis: Dict,
        knowledge: Dict
    ) -> Dict:
        """
        Generuje zaawansowaną strategię sprzedażową
        """
        strategy = {
            "immediate_action": self._get_immediate_action(analysis),
            "talking_points": self._generate_talking_points(analysis, knowledge),
            "objection_handlers": self._prepare_objection_handlers(analysis, knowledge),
            "value_proposition": self._create_value_proposition(analysis, knowledge),
            "closing_techniques": self._select_closing_techniques(analysis),
            "follow_up_plan": self._create_follow_up_plan(analysis)
        }
        
        # Dodaj konkretne liczby i kalkulacje
        if knowledge.get('tco'):
            strategy["financial_argument"] = self._build_financial_case(
                analysis,
                knowledge['tco'],
                knowledge.get('subsidies', {})
            )
        
        # Dodaj personalizację
        strategy["personalized_benefits"] = self._personalize_benefits(
            analysis.get('archetype'),
            knowledge
        )
        
        return strategy
    
    def _build_financial_case(
        self,
        analysis: Dict,
        tco_data: Dict,
        subsidies: Dict
    ) -> Dict:
        """
        Buduje konkretny argument finansowy
        """
        # Przykładowa kalkulacja
        annual_km = analysis.get('estimated_annual_km', 20000)
        ownership_years = 5
        
        # Koszty paliwa vs elektryczność
        fuel_cost_annual = (annual_km / 100) * 45  # 45 PLN/100km benzyna
        electricity_cost_annual = (annual_km / 100) * 12  # 12 PLN/100km EV
        
        # Oszczędności
        fuel_savings_annual = fuel_cost_annual - electricity_cost_annual
        service_savings_annual = 3000 - 1000  # Różnica w serwisie
        
        # Dopłaty
        subsidy_amount = subsidies.get('total_possible', 0)
        
        total_savings = (fuel_savings_annual + service_savings_annual) * ownership_years + subsidy_amount
        
        return {
            "annual_fuel_savings": fuel_savings_annual,
            "annual_service_savings": service_savings_annual,
            "subsidy_benefit": subsidy_amount,
            "total_5_year_savings": total_savings,
            "monthly_equivalent": total_savings / (ownership_years * 12),
            "break_even_months": self._calculate_break_even(total_savings, annual_km)
        }
    
    async def _generate_insights(self, analysis: Dict) -> List[str]:
        """
        Generuje eksperckie wnioski
        """
        insights = []
        
        # Analiza psychologiczna
        if analysis.get('confidence', 0) > 0.7:
            insights.append(
                f"Klient to {analysis.get('archetype')} - kluczowe jest podkreślenie {self._get_key_motivator(analysis.get('archetype'))}"
            )
        
        # Sygnały kupna
        if analysis.get('buying_signals'):
            insights.append(
                f"Silne sygnały kupna: {', '.join(analysis.get('buying_signals'))}. Czas na konkretną ofertę."
            )
        
        # Obawy do adresowania
        if analysis.get('objections'):
            insights.append(
                f"Główna obawa: {analysis.get('objections')[0]}. Użyj techniki FEEL-FELT-FOUND."
            )
        
        # Rekomendacja następnego kroku
        insights.append(
            f"Rekomendowany następny krok: {self._recommend_next_step(analysis)}"
        )
        
        return insights
    
    def _get_key_motivator(self, archetype: str) -> str:
        """
        Zwraca kluczowy motywator dla archetypu
        """
        motivators = {
            "Security Seeker": "bezpieczeństwo rodziny i gwarancje",
            "Value Optimizer": "oszczędności i ROI",
            "Tech Enthusiast": "innowacje i technologia",
            "Status Achiever": "prestiż i wyróżnienie",
            "Eco Warrior": "wpływ na środowisko",
            "Family Guardian": "komfort i bezpieczeństwo rodziny",
            "Performance Driver": "osiągi i emocje z jazdy",
            "Pragmatic Buyer": "praktyczność i niezawodność",
            "Innovation Seeker": "bycie pionierem",
            "Lifestyle Minimalist": "prostota i funkcjonalność"
        }
        return motivators.get(archetype, "wartość i jakość")
    
    def _recommend_next_step(self, analysis: Dict) -> str:
        """
        Rekomenduje następny krok na podstawie analizy
        """
        confidence = analysis.get('confidence', 0)
        phase = analysis.get('buying_phase', 'awareness')
        
        if confidence < 0.4:
            return "Zadaj pytania odkrywcze o potrzebach i oczekiwaniach"
        elif confidence < 0.7:
            return "Zaproponuj kalkulację TCO dopasowaną do potrzeb"
        elif phase == 'consideration':
            return "Umów jazdę próbną w dogodnym terminie"
        elif phase == 'decision':
            return "Przedstaw konkretną ofertę z wszystkimi benefitami"
        else:
            return "Edukuj o korzyściach i buduj zaufanie"
    
    def _calculate_tax_savings(self, benefits: List[Dict]) -> float:
        """
        Kalkuluje roczne oszczędności podatkowe
        """
        annual_savings = 0
        
        for benefit in benefits:
            if benefit['regulation_type'] == 'VAT':
                # Zakładamy średnią cenę 250k
                annual_savings += 250000 * 0.23  # 23% VAT savings
            elif benefit['regulation_type'] == 'BIK':
                # Różnica 1% vs 2% miesięcznie od 250k
                annual_savings += 250000 * 0.01 * 12
        
        return annual_savings
    
    def _calculate_break_even(self, total_savings: float, annual_km: int) -> int:
        """
        Kalkuluje okres zwrotu inwestycji
        """
        # Uproszczona kalkulacja
        price_difference = 50000  # Średnia różnica ceny EV vs ICE
        monthly_savings = total_savings / 60  # 5 lat = 60 miesięcy
        
        if monthly_savings > 0:
            return int(price_difference / monthly_savings)
        return 999
    
    def _parse_expert_response(self, response: str) -> Dict:
        """
        Parsuje odpowiedź ekspercką z AI
        """
        try:
            return json.loads(response)
        except:
            # Fallback parsing
            return {
                "archetype": "Unknown",
                "confidence": 0.5,
                "analysis": response,
                "objections": [],
                "buying_signals": []
            }
