# Demo Script for AI Multi-Language Translator
# Run this after starting the main application (python app.py)

import requests
import json
import time

# Test the translation API
def test_translation():
    print("🌍 Testing AI Multi-Language Translator API")
    print("=" * 50)
    
    # Test cases with different languages
    test_cases = [
        {"text": "Hello, how are you today?", "target": "hi", "description": "English to Hindi"},
        {"text": "Bonjour, comment allez-vous?", "target": "en", "description": "French to English"},
        {"text": "Hola, ¿cómo estás?", "target": "en", "description": "Spanish to English"},
        {"text": "This is a beautiful day", "target": "fr", "description": "English to French"},
        {"text": "Machine learning is fascinating", "target": "es", "description": "English to Spanish"},
    ]
    
    base_url = "http://localhost:5000"
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n🔄 Test {i}: {case['description']}")
        print(f"📝 Input: {case['text']}")
        
        try:
            response = requests.post(
                f"{base_url}/translate",
                json={
                    "text": case["text"],
                    "target_lang": case["target"]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "translated_text" in result:
                    print(f"✅ Output: {result['translated_text']}")
                    print(f"🔍 Detected: {result.get('source_language', 'Unknown')}")
                else:
                    print(f"❌ Error: {result.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {str(e)}")
        
        time.sleep(1)  # Small delay between requests
    
    print(f"\n🎉 Translation testing completed!")
    print(f"🌐 Web interface: {base_url}")
    print(f"📖 Features available:")
    print(f"   • Auto language detection")
    print(f"   • 30+ language support")
    print(f"   • Voice input & output")
    print(f"   • Real-time translation")
    print(f"   • Copy & swap functions")

if __name__ == "__main__":
    test_translation()
