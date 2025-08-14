"""
ULTRA BIGDECODER 3.0 - Ollama API Client
Integracja z modelem gptoss120b przez API
"""
import httpx
import json
import hashlib
import asyncio
from typing import Dict, Any, Optional, AsyncGenerator
from datetime import datetime
from cachetools import TTLCache

class OllamaClient:
    """Klient do komunikacji z Ollama API"""
    
    def __init__(self, base_url: str, api_key: str, model: str = "gptoss120b"):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.available = None  # Cache availability status
        
        # HTTP client z connection pooling - zawsze z Authorization dla chmury
        base_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5
            ),
            headers=base_headers
        )
        
        # Cache dla odpowiedzi
        self.cache = TTLCache(maxsize=100, ttl=300)  # 5 min cache
        
    async def check_availability(self) -> bool:
        """Sprawdź czy Ollama API jest dostępne"""
        if self.available is not None:
            return self.available
            
        try:
            # Try both /api/tags and /tags endpoints
            test_endpoints = [f"{self.base_url}/tags", f"{self.base_url}/api/tags"]
            
            for endpoint in test_endpoints:
                try:
                    response = await self.client.get(endpoint, timeout=5)
                    if response.status_code == 200:
                        self.available = True
                        return True
                except:
                    continue
                    
            self.available = False
            return False
        except:
            self.available = False
            return False
        
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generuje odpowiedź używając modelu gptoss120b
        
        Args:
            prompt: Główny prompt
            system: System prompt (kontekst)
            temperature: Kreatywność modelu (0-1)
            max_tokens: Maksymalna długość odpowiedzi
            stream: Czy streamować odpowiedź
            **kwargs: Dodatkowe parametry
            
        Returns:
            Dict z odpowiedzią modelu
        """
        
        # Sprawdź cache
        cache_key = self._get_cache_key(prompt, system, temperature)
        if not stream and cache_key in self.cache:
            return self.cache[cache_key]
        
        # Przygotuj payload
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "top_p": kwargs.get("top_p", 0.9),
                "top_k": kwargs.get("top_k", 40),
                "num_predict": max_tokens,
                "stop": kwargs.get("stop", []),
                "seed": kwargs.get("seed", None)
            }
        }
        
        if system:
            payload["system"] = system
            
        # Wywołaj API z retry logic
        response = await self._call_with_retry(payload, stream)
        
        # Cache jeśli nie stream
        if not stream:
            self.cache[cache_key] = response
            
        return response
    
    async def analyze_customer(
        self,
        customer_input: str,
        session_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Główna metoda analizy klienta - serce systemu BIGDECODER
        
        Args:
            customer_input: Wypowiedź klienta  
            session_context: Kontekst sesji (historia, profil)
            
        Returns:
            Dict z pełną analizą archetypu, obiekcji i strategii
        """
        if not await self.check_availability():
            # Intelligent fallback gdy Ollama nie działa
            return await self._fallback_analysis(customer_input, session_context)
        
        # Przygotuj prompt zgodnie z BIGDECODER.md
        system_prompt = """Jesteś Ultra BIGDecoder 3.0 - ekspertem analizy klientów Tesla w Polsce.

TWOJE ZADANIE: Analizuj wypowiedź klienta i zwróć JSON z:
1. ARCHETYPE - zidentyfikowany typ klienta
2. CONFIDENCE - pewność analizy (0-1)
3. RESPONSE - natychmiastowa odpowiedź do klienta
4. QUESTIONS - pytania pogłębiające (jeśli confidence < 0.8)
5. OBJECTIONS - wykryte obawy
6. PURCHASE_PROBABILITY - szansa na zakup (0-1)

ARCHETYPY (wybierz najlepszy):
- Security Seeker: bezpieczeństwo, gwarancje, niezawodność
- Eco-Tech Pragmatist: oszczędności, ekologia, praktyczność  
- Busy Executive: czas, efektywność, automatyka
- Status Achiever: prestiż, innowacje, wyróżnianie się
- Family Guardian: rodzina, bezpieczeństwo dzieci
- Performance Driver: prędkość, emocje, sportowość
- Rational Analyst: dane, analiza, logika
- Value Optimizer: cena, wartość, oszczędności

ODPOWIADAJ ZAWSZE PO POLSKU w formacie JSON."""

        # Kontekst z historii
        context_text = ""
        if session_context and session_context.get("history"):
            context_text = f"\\nKontekst z poprzednich wypowiedzi: {session_context['history'][-3:]}"

        prompt = f"""ANALIZA KLIENTA TESLA:
Wypowiedź: "{customer_input}"{context_text}

Zwróć JSON:"""

        try:
            result = await self.generate(
                prompt=prompt,
                system=system_prompt,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse JSON response
            response_text = result.get("response", "{}")
            try:
                analysis = json.loads(response_text)
                return self._format_analysis(analysis, customer_input)
            except:
                # Jeśli JSON parsing fails, użyj fallback
                return await self._fallback_analysis(customer_input, session_context)
                
        except Exception as e:
            print(f"Ollama analysis error: {e}")
            return await self._fallback_analysis(customer_input, session_context)

    async def generate_response(
        self,
        customer_profile: Dict[str, Any],
        objection: str = None,
        mode: str = "coach"
    ) -> Dict[str, Any]:
        """Generuj strategię/coaching dla sprzedawcy"""
        
        if not await self.check_availability():
            return self._fallback_strategy(customer_profile, objection, mode)
            
        system_prompt = f"""Jesteś Ultra BIGDecoder 3.0 - ekspertem strategii sprzedaży Tesla.

TRYB: {mode}
- coach: Podpowiedzi dla sprzedawcy
- analyzer: Analiza sytuacji  
- client_simulator: Symulacja klienta

Generuj strategię w formacie JSON z polami:
- response: Główna rada/strategia
- key_points: Kluczowe punkty (array)
- confidence: Pewność strategii (0-1)
- next_actions: Następne kroki (array)"""

        profile_text = json.dumps(customer_profile, ensure_ascii=False)
        objection_text = f" Obiekcja: {objection}" if objection else ""
        
        prompt = f"""PROFIL KLIENTA: {profile_text}{objection_text}

Wygeneruj strategię sprzedażową (JSON):"""

        try:
            result = await self.generate(
                prompt=prompt,
                system=system_prompt,
                temperature=0.8,
                max_tokens=800
            )
            
            response_text = result.get("response", "{}")
            try:
                strategy = json.loads(response_text)
                return strategy
            except:
                return self._fallback_strategy(customer_profile, objection, mode)
                
        except Exception as e:
            print(f"Strategy generation error: {e}")
            return self._fallback_strategy(customer_profile, objection, mode)

    async def _fallback_analysis(self, customer_input: str, session_context: Dict = None) -> Dict[str, Any]:
        """Inteligentny fallback gdy Ollama nie działa"""
        
        # Prosta analiza oparta na słowach kluczowych
        text_lower = customer_input.lower()
        
        # Określ archetyp
        archetype = "Security Seeker"  # default
        confidence = 0.4
        
        if any(word in text_lower for word in ["drogi", "cena", "koszt", "tani"]):
            archetype = "Value Optimizer"
            confidence = 0.6
        elif any(word in text_lower for word in ["rodzina", "dzieci", "bezpieczny"]):
            archetype = "Family Guardian"  
            confidence = 0.7
        elif any(word in text_lower for word in ["czas", "szybko", "autopilot"]):
            archetype = "Busy Executive"
            confidence = 0.6
        elif any(word in text_lower for word in ["ekologia", "oszczędność", "środowisko"]):
            archetype = "Eco-Tech Pragmatist"
            confidence = 0.7
            
        # Generuj odpowiedź
        responses = {
            "Security Seeker": "Tesla to jedna z najbezpieczniejszych marek. Czy bezpieczeństwo jest Pana priorytetem?",
            "Value Optimizer": "Tesla oferuje doskonałą wartość w długoterminowej perspektywie. Interesuje Pana analiza kosztów?",
            "Family Guardian": "Tesla Model Y to idealny wybór dla rodziny. Czy planuje Pan podróże z dziećmi?",
            "Busy Executive": "Tesla oszczędza czas dzięki automatyce. Czy efektywność jest dla Pana ważna?",
            "Eco-Tech Pragmatist": "Tesla łączy ekologię z oszczędnościami. Czy ma Pan panele fotowoltaiczne?"
        }
        
        return {
            "archetype": {
                "name": archetype,
                "confidence": confidence
            },
            "response": responses.get(archetype, "Dziękuję za informację. Opowie Pan więcej o swoich potrzebach?"),
            "questions": [
                "Co jest dla Pana najważniejsze w nowym samochodzie?",
                "Czy rozważał Pan wcześniej samochody elektryczne?"
            ],
            "objections": [],
            "purchase_probability": confidence * 0.5,
            "confidence": confidence
        }

    def _fallback_strategy(self, profile: Dict, objection: str, mode: str) -> Dict[str, Any]:
        """Fallback strategia"""
        return {
            "response": f"Strategia dla {mode}: Skup się na budowaniu zaufania i pokazaniu korzyści.",
            "key_points": ["Zbuduj zaufanie", "Pokaż korzyści", "Zadaj pytania"],
            "confidence": 0.6,
            "next_actions": ["Kontynuuj rozmowę", "Zbierz więcej informacji"]
        }

    def _format_analysis(self, analysis: Dict, customer_input: str) -> Dict[str, Any]:
        """Formatuj analizę do standardu systemu"""
        return {
            "archetype": {
                "name": analysis.get("archetype", "Security Seeker"),
                "confidence": analysis.get("confidence", 0.5)
            },
            "response": analysis.get("response", "Dziękuję za informację."),
            "questions": analysis.get("questions", []),
            "objections": analysis.get("objections", []),
            "purchase_probability": analysis.get("purchase_probability", 0.5),
            "confidence": analysis.get("confidence", 0.5)
        }
    
    async def _call_with_retry(
        self, 
        payload: Dict, 
        stream: bool,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """Wywołanie API z automatycznym retry"""
        
        for attempt in range(max_retries):
            try:
                if stream:
                    return await self._stream_response(payload)
                else:
                    return await self._single_response(payload)
                    
            except httpx.TimeoutException as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Timeout po {max_retries} próbach: {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Błąd API po {max_retries} próbach: {e}")
                await asyncio.sleep(2 ** attempt)
    
    async def _single_response(self, payload: Dict) -> Dict[str, Any]:
        """Pojedyncza odpowiedź (bez streamingu)"""
        
        response = await self.client.post(
            f"{self.base_url}/api/generate",
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code} - {response.text}")
            
        result = response.json()
        
        return {
            "response": result.get("response", ""),
            "model": result.get("model", self.model),
            "created_at": result.get("created_at", datetime.now().isoformat()),
            "done": result.get("done", True),
            "context": result.get("context", []),
            "total_duration": result.get("total_duration", 0),
            "prompt_eval_count": result.get("prompt_eval_count", 0),
            "eval_count": result.get("eval_count", 0)
        }
    
    async def _stream_response(self, payload: Dict) -> AsyncGenerator:
        """Streamowana odpowiedź"""
        
        async with self.client.stream(
            "POST",
            f"{self.base_url}/api/generate",
            json=payload
        ) as response:
            
            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code}")
                
            async for line in response.aiter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        yield chunk
                    except json.JSONDecodeError:
                        continue
    
    def _get_cache_key(self, prompt: str, system: str, temperature: float) -> str:
        """Generuje klucz cache dla danego zestawu parametrów"""
        
        key_string = f"{self.model}:{prompt}:{system}:{temperature}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    async def analyze_customer_v2(
        self, 
        customer_input: str,
        session_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Specjalizowana funkcja do analizy klienta
        
        Args:
            customer_input: Wypowiedź klienta
            session_context: Kontekst sesji (profil, historia)
            
        Returns:
            Analiza z archetypem, obiekcjami, strategią
        """
        
        db_data = session_context.get('db_data', {})
        archetypes_list = json.dumps(db_data.get('archetypes', []), ensure_ascii=False, indent=2)
        objections_list = json.dumps(db_data.get('objections', []), ensure_ascii=False, indent=2)
        playbooks_list = json.dumps(db_data.get('playbooks', []), ensure_ascii=False, indent=2)

        newest_input_text = session_context.get('newest_input', customer_input)

        prompt = f"""
ANALIZA KLIENTA TESLA:

DOSTĘPNE DANE Z BAZY:
---
Archetypy:
{archetypes_list}
---
Obiekcje:
{objections_list}
---
Playbooki:
{playbooks_list}
---

AKTUALNA SYTUACJA:
Całość rozmowy: "{customer_input}"
NAJNOWSZA WYPOWIEDŹ (skup się na tym): "{newest_input_text}"

Kontekst sesji:
- Profil: {json.dumps(session_context.get('profile', {}), ensure_ascii=False)}
- Historia: {json.dumps(session_context.get('history', [])[-5:], ensure_ascii=False)}

ZADANIA:
Twoim nadrzędnym zadaniem jest zareagować na NAJNOWSZĄ WYPOWIEDŹ klienta, biorąc pod uwagę CAŁOŚĆ ROZMOWY i dostępne dane.

1. Przeanalizuj NAJNOWSZĄ WYPOWIEDŹ w kontekście historii i dostępnych danych.
2. Zaktualizuj lub potwierdź archetyp klienta z listy Archetypy. Zwróć jego DOKŁADNE id i name.
3. **Dynamiczna Granulacja**: Jeśli pewność ('confidence') jest niska (< 0.6) i widzisz unikalny wzorzec, który nie pasuje do żadnego archetypu, zaproponuj nowy sub-archetyp w polu `new_archetype_suggestion`. W przeciwnym razie zostaw to pole jako `null`.
4. Zidentyfikuj NOWE obiekcje z listy Obiekcje, które pojawiły się w najnowszej wypowiedzi.
5. Wygeneruj 'quick_reply': krótką, trafną odpowiedź, która BEZPOŚREDNIO odnosi się do najnowszej wypowiedzi.
6. Wygeneruj pytania pogłębiające ('questions'), które wynikają z najnowszej wypowiedzi.
7. Zaktualizuj prawdopodobieństwo zakupu ('purchase_probability', 0.0-1.0).
8. Zaproponuj następne kroki ('next_actions') w oparciu o NOWĄ sytuację.
9. Dopasuj najlepszy playbook z listy Playbooki. Zwróć DOKŁADNE playbook_id.

Odpowiedz w formacie JSON, używając DOKŁADNYCH wartości 'id' i 'playbook_id' z dostarczonych list. ID dla archetypu i obiekcji jest kluczem 'id', a dla playbooka kluczem 'id' (mapowane na playbook_id w strategii).

Struktura odpowiedzi JSON:
{{
    "archetype": {{
        "id": "uuid",
        "name": "string",
        "confidence": float
    }},
    "new_archetype_suggestion": {{
        "based_on": ["archetype_name_1", "archetype_name_2"],
        "new_name": "string",
        "reasoning": "string"
    }},
    "objections": [
        {{
            "id": "uuid",
            "text": "string",
            "hidden": boolean
        }}
    ],
    "strategy": {{
        "playbook_id": "uuid",
        "approach": "string",
        "key_points": ["string"]
    }},
    "quick_reply": "string",
    "questions": ["string"],
    "purchase_probability": float,
    "next_actions": ["string"]
}}
"""
        
        response = await self.generate(
            prompt=prompt,
            system=self._get_analysis_system_prompt(),
            temperature=0.3,  # Niska dla konsystentnych analiz
            max_tokens=2000
        )
        
        try:
            return json.loads(response["response"])
        except:
            return response
    
    def _get_analysis_system_prompt(self) -> str:
        """System prompt dla analizy klienta"""
        
        return """
Jesteś ekspertem analizy behawioralnej klientów Tesla.

TWOJA WIEDZA:
- 10 archetypów: Tech Enthusiast, Status Achiever, Eco Warrior, Pragmatic Family, 
  Innovation Seeker, Performance Driver, Economic Optimizer, Security Seeker, 
  Lifestyle Minimalist, Future Visionary
- 12 obiekcji: Cena, Zasięg, Ładowanie, Serwis, Spadek wartości, Technologia,
  Bezpieczeństwo, Praktyczność, Dostępność, Jakość, Zima, Autopilot
- 10 playbooków sprzedażowych dopasowanych do archetypów
- Psychologia sprzedaży i techniki perswazji

ZASADY ANALIZY:
1. Szukaj subtelnych sygnałów w języku klienta
2. Identyfikuj ukryte obawy za pytaniami
3. Oceń fazę procesu zakupowego
4. Dostosuj strategię do profilu psychometrycznego
5. Zawsze proponuj konkretne następne kroki

Odpowiadaj TYLKO w formacie JSON.
"""
    
    async def generate_response_v2(
        self,
        customer_profile: Dict[str, Any],
        objection: Optional[Dict[str, Any]] = None,
        mode: str = "coach"
    ) -> str:
        """
        Generuje odpowiedź dla sprzedawcy lub symulację klienta
        
        Args:
            customer_profile: Profil klienta
            objection: Aktualna obiekcja do adresowania
            mode: Tryb pracy (coach/client_simulator/hybrid)
            
        Returns:
            Wygenerowana odpowiedź
        """
        
        if mode == "coach":
            return await self._generate_coach_response(customer_profile, objection)
        elif mode == "client_simulator":
            return await self._generate_client_simulation(customer_profile)
        else:  # hybrid
            return await self._generate_hybrid_response(customer_profile, objection)
    
    async def _generate_coach_response(
        self,
        profile: Dict,
        objection: Optional[Dict]
    ) -> str:
        """Generuje wskazówki dla sprzedawcy"""
        
        prompt = f"""
PROFIL KLIENTA: {json.dumps(profile, ensure_ascii=False)}
OBIEKCJA: {json.dumps(objection, ensure_ascii=False) if objection else "Brak"}

Jako coach sprzedaży, podaj:
1. Konkretną odpowiedź na obiekcję (jeśli jest)
2. Kluczowe punkty do poruszenia
3. Słowa/frazy do użycia i uniknięcia
4. Następny krok w procesie

Bądź konkretny i praktyczny.
"""
        
        response = await self.generate(
            prompt=prompt,
            temperature=0.5,
            max_tokens=1000
        )
        
        return response["response"]
    
    async def close(self):
        """Zamyka połączenie z API"""
        await self.client.aclose()
