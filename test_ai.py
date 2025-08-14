from config import config
from services.ollama_client import OllamaClient
import asyncio
import json

async def debug_analysis():
    client = OllamaClient(config.OLLAMA_BASE_URL, config.OLLAMA_API_KEY, config.OLLAMA_MODEL)
    
    print("1. Check availability...")
    available = await client.check_availability()
    print(f"   Available: {available}")
    
    if available:
        print("2. Test direct generate...")
        try:
            result = await client.generate(
                prompt="Odpowiedz krotko po polsku: Tesla Model Y ma jaki zasieg?", 
                max_tokens=100
            )
            response_text = result.get("response", "")
            print(f"   Generate OK: {len(response_text)} chars")
            print(f"   Response: {response_text[:150]}...")
        except Exception as e:
            print(f"   Generate error: {e}")
    
    print("3. Test analyze_customer...")
    result = await client.analyze_customer("Chce Tesla ale martwie sie o zasieg")
    is_fallback = "Tesla to jedna z najbezpieczniejszych" in result.get("response", "")
    print(f"   Using: {'FALLBACK' if is_fallback else 'REAL AI'}")
    print(f"   Response: {result.get('response', '')}")

if __name__ == "__main__":
    asyncio.run(debug_analysis())
