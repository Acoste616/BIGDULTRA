"""
ULTRA BIGDECODER 3.0 - Kalkulator Metryk
Pełne logiki dla OVN, Churn Risk, Fun-Drive, Purchase Likelihood
"""
from typing import Dict, Any, List, Optional, Tuple
import math
from datetime import datetime

class MetricsCalculator:
    """Kalkulator wszystkich kluczowych metryk systemu Ultra BIGDecoder 3.0"""
    
    def __init__(self):
        """Inicjalizacja z wagami i progami"""
        
        # Wagi dla Purchase Likelihood (suma = 1.2 dla amplifikacji)
        self.purchase_weights = {
            'tone': 0.15,           # Ton wypowiedzi
            'latency': 0.10,        # Szybkość odpowiedzi
            'length_trend': 0.05,   # Trend długości wiadomości
            'intent': 0.20,         # Sygnały intencji
            'objection_intensity': -0.20,  # Obiekcje (negatywne)
            'fit': 0.20,            # Dopasowanie potrzeb
            'slots': 0.10,          # Kompletność informacji
            'momentum': 0.20,       # Momentum sesji
            'context': 0.15,        # Kontekst (PV, firma, rodzina)
            'competitor': -0.10     # Porównania z konkurencją
        }
        
        # Progi decyzyjne
        self.thresholds = {
            'high_confidence': 0.8,
            'medium_confidence': 0.5,
            'purchase_ready': 0.75,
            'churn_danger': 0.7,
            'fun_drive_threshold': 6  # Powyżej = tylko pojeździć
        }
        
        # Archetypy z potencjałem OVN (1-10)
        self.archetype_ovn = {
            'Status Achiever': 8,
            'Pragmatic Analyst': 4,
            'Eco-Transcender': 6,
            'Security Seeker': 3,
            'Młody Profesjonalista z Dużego Miasta': 9,
            'Performance Enthusiast': 10,
            'Tech Executive': 8,
            'Early Adopter': 7,
            'Budget Conscious Family': 2,
            'Cautious Adopter': 5
        }
    
    def calculate_all_metrics(self, 
                            session_data: Dict[str, Any],
                            analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Oblicza wszystkie metryki na podstawie danych sesji i analizy
        
        Returns:
            Dict z wszystkimi metrykami i ich składowymi
        """
        # Ekstraktuj features
        features = self._extract_features(session_data, analysis_result)
        
        # Oblicz główne metryki
        purchase_likelihood = self._calculate_purchase_likelihood(features)
        churn_risk = self._calculate_churn_risk(features, purchase_likelihood)
        fun_drive_score = self._calculate_fun_drive(features, analysis_result)
        ovn_potential = self._calculate_ovn_potential(analysis_result)
        cta_readiness = self._determine_cta_readiness(
            purchase_likelihood, 
            features.get('confidence', 0),
            features.get('slots', 0)
        )
        
        # Określ następne kroki
        next_actions = self._generate_next_actions(
            purchase_likelihood,
            churn_risk,
            features,
            analysis_result
        )
        
        # Sygnały de-eskalacji
        deescalation_signals = self._detect_deescalation_signals(
            churn_risk,
            features
        )
        
        return {
            'purchase_likelihood': round(purchase_likelihood, 1),
            'churn_risk': round(churn_risk, 1),
            'fun_drive_score': round(fun_drive_score, 1),
            'ovn_potential': ovn_potential,
            'cta_readiness': cta_readiness,
            'next_actions': next_actions,
            'deescalation_signals': deescalation_signals,
            'confidence_level': self._get_confidence_level(features.get('confidence', 0)),
            'features': features,  # Dla debugowania
            'timestamp': datetime.now().isoformat()
        }
    
    def _extract_features(self, 
                         session_data: Dict[str, Any],
                         analysis_result: Dict[str, Any]) -> Dict[str, float]:
        """Ekstraktuje features z danych sesji i analizy"""
        
        features = {}
        
        # 1. TON WYPOWIEDZI (0-1)
        # Mapowanie: bardzo negatywny=0, neutralny=0.5, pozytywny=1.0
        tone_map = {
            'very_negative': 0.0,
            'negative': 0.25,
            'skeptical': 0.35,
            'neutral': 0.5,
            'interested': 0.65,
            'positive': 0.75,
            'enthusiastic': 1.0
        }
        detected_tone = analysis_result.get('tone', 'neutral')
        features['tone'] = tone_map.get(detected_tone, 0.5)
        
        # 2. LATENCY - szybkość odpowiedzi (0-1)
        # Zakładamy że szybka odpowiedź = zainteresowanie
        response_time = session_data.get('avg_response_time', 30)  # sekundy
        features['latency'] = max(0, min(1, 1 - (response_time / 60)))
        
        # 3. TREND DŁUGOŚCI WIADOMOŚCI (0-1)
        # Rosnący = zainteresowanie (0.7-1), spadający = znudzenie (0-0.4)
        messages = session_data.get('messages', [])
        if len(messages) >= 2:
            recent_lengths = [len(m.get('text', '')) for m in messages[-3:]]
            older_lengths = [len(m.get('text', '')) for m in messages[:-3]]
            if older_lengths:
                trend = sum(recent_lengths) / sum(older_lengths) if sum(older_lengths) > 0 else 1
                features['length_trend'] = max(0, min(1, trend))
            else:
                features['length_trend'] = 0.5
        else:
            features['length_trend'] = 0.5
        
        # 4. SYGNAŁY INTENCJI (0-1)
        intent_signals = {
            'financing_interest': 0.25,
            'test_drive_request': 0.35,
            'configuration_interest': 0.30,
            'delivery_timeline': 0.40,
            'trade_in_mentioned': 0.20,
            'family_consultation': 0.15,
            'comparison_active': -0.10  # Negatywne gdy porównuje
        }
        
        intent_score = 0
        for signal, weight in intent_signals.items():
            if session_data.get(signal, False):
                intent_score += weight
        features['intent'] = max(0, min(1, intent_score))
        
        # 5. INTENSYWNOŚĆ OBIEKCJI (0-1)
        objections = analysis_result.get('objections', [])
        objection_count = len(objections)
        objection_severity = sum(obj.get('severity', 5) for obj in objections) / 10 if objections else 0
        features['objection_intensity'] = min(1, (objection_count * 0.2 + objection_severity * 0.8))
        
        # 6. DOPASOWANIE POTRZEB (0-1)
        fit_factors = {
            'has_pv': 0.3,           # Ma panele PV
            'family_fit': 0.25,      # Pasuje do rodziny
            'budget_match': 0.25,    # Budżet się zgadza
            'use_case_match': 0.20   # Przypadek użycia pasuje
        }
        
        fit_score = 0
        if session_data.get('has_solar_panels'):
            fit_score += fit_factors['has_pv']
        if session_data.get('family_size', 0) > 2 and 'Model Y' in analysis_result.get('recommended_model', ''):
            fit_score += fit_factors['family_fit']
        if session_data.get('budget_ok', True):
            fit_score += fit_factors['budget_match']
        if session_data.get('daily_commute', 0) < 100:  # km
            fit_score += fit_factors['use_case_match']
        
        features['fit'] = fit_score
        
        # 7. KOMPLETNOŚĆ SLOTÓW (0-1)
        required_slots = [
            'current_car', 'annual_mileage', 'charging_possibility',
            'budget_range', 'purchase_timeline', 'key_priorities'
        ]
        filled_slots = sum(1 for slot in required_slots if session_data.get(slot))
        features['slots'] = filled_slots / len(required_slots)
        
        # 8. MOMENTUM SESJI (0-1)
        # Ostatnie 3 interakcje - czy poprawia się scoring/ton/konkretność
        recent_scores = session_data.get('interaction_scores', [0.5, 0.5, 0.5])[-3:]
        if len(recent_scores) >= 2:
            momentum = (recent_scores[-1] - recent_scores[0]) / 2 + 0.5
            features['momentum'] = max(0, min(1, momentum))
        else:
            features['momentum'] = 0.5
        
        # 9. KONTEKST BIZNESOWY/RODZINNY (0-1)
        context_score = 0
        if session_data.get('is_business_context'):
            context_score += 0.3
        if session_data.get('has_family'):
            context_score += 0.2
        if session_data.get('eco_conscious'):
            context_score += 0.2
        if session_data.get('tech_savvy'):
            context_score += 0.3
        features['context'] = min(1, context_score)
        
        # 10. PORÓWNANIA Z KONKURENCJĄ (0-1)
        # Więcej porównań = mniej pewności
        competitor_mentions = session_data.get('competitor_mentions', 0)
        features['competitor'] = min(1, competitor_mentions * 0.2)
        
        # 11. CONFIDENCE z analizy AI
        features['confidence'] = analysis_result.get('confidence_score', 0)
        
        return features
    
    def _calculate_purchase_likelihood(self, features: Dict[str, float]) -> float:
        """
        Oblicza prawdopodobieństwo zakupu na podstawie features
        Używa ważonej sumy z sigmoidą dla normalizacji
        """
        score_raw = 0
        
        for feature, weight in self.purchase_weights.items():
            if feature in features:
                score_raw += weight * features[feature]
        
        # Sigmoid dla gładkiego mapowania na 0-100
        def sigmoid(x, steepness=5):
            return 1 / (1 + math.exp(-steepness * (x - 0.5)))
        
        # Normalizacja do 0-100
        purchase_likelihood = sigmoid(score_raw) * 100
        
        # EMA (Exponential Moving Average) dla wygładzenia
        # Tu uproszczone - w prawdziwej implementacji byłoby z historii
        return max(0, min(100, purchase_likelihood))
    
    def _calculate_churn_risk(self, 
                             features: Dict[str, float],
                             purchase_likelihood: float) -> float:
        """
        Oblicza ryzyko utraty klienta
        NIE jest to 100 - purchase_likelihood!
        """
        # Bazowe ryzyko
        churn_base = 100 - purchase_likelihood
        
        # Dodatkowe kary za negatywne sygnały
        penalty = 0
        
        # Kara za negatywny ton
        penalty += 20 * (1 - features.get('tone', 0.5))
        
        # Kara za obiekcje
        penalty += 15 * features.get('objection_intensity', 0)
        
        # Kara za brak momentum
        penalty += 10 * (1 - features.get('momentum', 0.5))
        
        # Kara za konkurencję
        penalty += 10 * features.get('competitor', 0)
        
        # Bonus za dobre dopasowanie (zmniejsza churn)
        penalty -= 15 * features.get('fit', 0)
        
        churn_risk = churn_base + penalty
        
        return max(0, min(100, churn_risk))
    
    def _calculate_fun_drive(self, 
                            features: Dict[str, float],
                            analysis_result: Dict[str, Any]) -> float:
        """
        Oblicza Fun-Drive Score (0-10)
        Wysoki = chce tylko pojeździć, nie kupić
        Niski = poważnie zainteresowany zakupem
        """
        fun_drive = 5  # Bazowa wartość
        
        # Czynniki zwiększające fun-drive (chce tylko pojeździć)
        if 'test_drive' in str(analysis_result.get('input_text', '')).lower():
            fun_drive += 2
        
        if features.get('intent', 0) < 0.3:
            fun_drive += 1.5
        
        if features.get('slots', 0) < 0.3:
            fun_drive += 1
        
        # Wykrywanie fraz wskazujących na "tylko pojeździć"
        fun_phrases = ['ciekawy jak jeździ', 'chcę spróbować', 'zobaczyć przyspieszenie',
                      'porównać z', 'test', 'wypróbować']
        input_text = str(analysis_result.get('input_text', '')).lower()
        if any(phrase in input_text for phrase in fun_phrases):
            fun_drive += 2
        
        # Czynniki zmniejszające fun-drive (poważne zainteresowanie)
        if features.get('intent', 0) > 0.6:
            fun_drive -= 2
        
        if features.get('slots', 0) > 0.6:
            fun_drive -= 1.5
        
        if 'financing' in input_text or 'leasing' in input_text:
            fun_drive -= 3
        
        if 'delivery' in input_text or 'termin' in input_text:
            fun_drive -= 2
        
        # Archetyp ma wpływ
        archetype = analysis_result.get('archetype', {}).get('name', '')
        if archetype in ['Performance Enthusiast', 'Early Adopter']:
            fun_drive += 1
        elif archetype in ['Pragmatic Analyst', 'Budget Conscious Family']:
            fun_drive -= 1
        
        return max(0, min(10, fun_drive))
    
    def _calculate_ovn_potential(self, analysis_result: Dict[str, Any]) -> int:
        """
        Oblicza Overnight Value Potential (0-10)
        Potencjał jazdy weekendowej/przedłużonej
        """
        archetype = analysis_result.get('archetype', {}).get('name', 'Unknown')
        
        # Pobierz wartość z mapy archetypów
        base_ovn = self.archetype_ovn.get(archetype, 5)
        
        # Modyfikatory na podstawie kontekstu
        modifiers = 0
        
        input_text = str(analysis_result.get('input_text', '')).lower()
        
        # Pozytywne modyfikatory
        if any(word in input_text for word in ['weekend', 'wakacje', 'podróż', 'rodzina']):
            modifiers += 1
        
        if 'tesla' in input_text and 'marzenie' in input_text:
            modifiers += 1
        
        # Negatywne modyfikatory  
        if any(word in input_text for word in ['drogo', 'za dużo', 'nie stać']):
            modifiers -= 2
        
        if 'tylko miasto' in input_text or 'krótkie trasy' in input_text:
            modifiers -= 1
        
        ovn_potential = base_ovn + modifiers
        
        return max(0, min(10, ovn_potential))
    
    def _determine_cta_readiness(self, 
                                purchase_likelihood: float,
                                confidence: float,
                                slots_filled: float) -> str:
        """
        Określa gotowość do Call-To-Action
        """
        if purchase_likelihood >= 85 and confidence >= 0.8:
            return 'immediate_purchase'
        elif purchase_likelihood >= 70 and slots_filled >= 0.7:
            return 'configuration'
        elif purchase_likelihood >= 60 and confidence >= 0.6:
            return 'book_test_drive'
        elif purchase_likelihood >= 40:
            return 'schedule_callback'
        elif slots_filled < 0.4:
            return 'gather_information'
        else:
            return 'build_trust'
    
    def _generate_next_actions(self,
                              purchase_likelihood: float,
                              churn_risk: float,
                              features: Dict[str, float],
                              analysis_result: Dict[str, Any]) -> List[str]:
        """
        Generuje listę następnych kroków dla sprzedawcy
        """
        actions = []
        
        # WYSOKA SZANSA ZAKUPU
        if purchase_likelihood >= 75:
            actions.append("🔥 Przejdź do finalizacji - klient gotowy!")
            actions.append("📋 Zaproponuj konfigurację online")
            actions.append("💰 Przedstaw opcje finansowania")
            
        # ŚREDNIA SZANSA - BUDUJ WARTOŚĆ
        elif purchase_likelihood >= 50:
            if features.get('slots', 0) < 0.5:
                actions.append("❓ Zadaj pytania uzupełniające o potrzeby")
            
            if features.get('objection_intensity', 0) > 0.3:
                actions.append("🛡️ Zbij główne obiekcje faktami")
            
            actions.append("🚗 Zaproponuj jazdę testową")
            actions.append("📊 Pokaż kalkulację TCO")
            
        # NISKA SZANSA - BUDUJ ZAUFANIE
        else:
            actions.append("🤝 Buduj relację, nie sprzedawaj")
            actions.append("📚 Edukuj o technologii i korzyściach")
            actions.append("👂 Słuchaj i zbieraj informacje")
        
        # WYSOKIE RYZYKO UTRATY
        if churn_risk >= 70:
            actions.insert(0, "⚠️ DE-ESKALACJA: Zmień ton na bardziej empatyczny")
            actions.insert(1, "🎯 Skup się na JEDNEJ głównej korzyści")
        
        # SPECYFICZNE DLA KONTEKSTU
        if analysis_result.get('has_solar_panels'):
            actions.append("☀️ Pokaż synergię z panelami PV")
        
        if analysis_result.get('competitor_mentioned'):
            actions.append("🆚 Porównaj TCO z konkurencją")
        
        if features.get('intent', 0) > 0.7:
            actions.append("⏰ Podkreśl ograniczoną dostępność")
        
        return actions[:5]  # Maksymalnie 5 akcji
    
    def _detect_deescalation_signals(self,
                                    churn_risk: float,
                                    features: Dict[str, float]) -> List[str]:
        """
        Wykrywa sygnały wymagające de-eskalacji
        """
        signals = []
        
        if churn_risk >= 70:
            signals.append("🔴 Wysokie ryzyko utraty - zmień podejście!")
        
        if features.get('tone', 0.5) < 0.3:
            signals.append("😤 Klient jest sfrustrowany - okaż empatię")
        
        if features.get('objection_intensity', 0) > 0.7:
            signals.append("🛑 Za dużo obiekcji - cofnij się i słuchaj")
        
        if features.get('momentum', 0.5) < 0.2:
            signals.append("📉 Tracisz zainteresowanie - zmień taktykę")
        
        if features.get('competitor', 0) > 0.5:
            signals.append("🆚 Klient mocno porównuje - pokaż unikalne wartości")
        
        return signals
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Określa poziom pewności"""
        if confidence >= self.thresholds['high_confidence']:
            return 'high'
        elif confidence >= self.thresholds['medium_confidence']:
            return 'medium'
        else:
            return 'low'
    
    def calculate_evolution_metrics(self,
                                   session_history: List[Dict],
                                   current_analysis: Dict) -> Dict[str, Any]:
        """
        Oblicza metryki ewolucji archetypu w czasie
        """
        if len(session_history) < 2:
            return {
                'evolution_stage': 'initial',
                'stability': 0,
                'direction': 'unknown'
            }
        
        # Analiza stabilności archetypu
        archetype_changes = []
        for i in range(1, len(session_history)):
            prev = session_history[i-1].get('archetype', {}).get('name')
            curr = session_history[i].get('archetype', {}).get('name')
            if prev != curr:
                archetype_changes.append({
                    'from': prev,
                    'to': curr,
                    'step': i
                })
        
        stability = 1 - (len(archetype_changes) / len(session_history))
        
        # Kierunek ewolucji
        if len(archetype_changes) > 0:
            last_change = archetype_changes[-1]
            # Mapowanie kierunku (uproszczone)
            positive_evolution = ['Cautious Adopter', 'Pragmatic Analyst', 'Status Achiever']
            if last_change['to'] in positive_evolution:
                direction = 'positive'
            else:
                direction = 'exploratory'
        else:
            direction = 'stable'
        
        # Etap ewolucji
        total_interactions = len(session_history)
        if total_interactions < 3:
            evolution_stage = 'initial'
        elif total_interactions < 7:
            evolution_stage = 'exploration'
        elif stability > 0.7:
            evolution_stage = 'stabilized'
        else:
            evolution_stage = 'dynamic'
        
        return {
            'evolution_stage': evolution_stage,
            'stability': round(stability, 2),
            'direction': direction,
            'archetype_changes': archetype_changes,
            'total_interactions': total_interactions
        }
