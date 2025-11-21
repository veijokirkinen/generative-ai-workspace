"""
OpenAI API Setup Helper - Generative AI Workspace
Testaa OpenAI API:n toimivuuden ja auttaa konfiguroinnissa.
"""

import os
from dotenv import load_dotenv

def check_openai_setup():
    """Tarkistaa OpenAI API:n konfiguraation ja testaa yhteyden."""
    
    print("🔍 Tarkistetaan OpenAI API setup...")
    print("="*50)
    
    # Lataa .env tiedosto
    load_dotenv()
    
    # Tarkista API key
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY puuttuu!")
        print("\n🔧 KORJAUSOHJEET:")
        print("1. Mene: https://platform.openai.com/api-keys")
        print("2. Luo uusi API key")
        print("3. Lisää se .env tiedostoon:")
        print("   OPENAI_API_KEY=your_actual_api_key_here")
        return False
    
    if api_key == "your_openai_api_key_here":
        print("⚠️  API key on vielä placeholder-arvo!")
        print("📝 Korvaa .env tiedostossa oikealla API keylla.")
        return False
    
    # Testaa OpenAI import
    try:
        import openai
        print("✅ OpenAI kirjasto asennettu")
    except ImportError:
        print("❌ OpenAI kirjasto puuttuu!")
        print("🔧 Asenna: pip install openai")
        return False
    
    # Testaa API yhteys
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Yksinkertainen testi
        print("🔌 Testataan API yhteyttä...")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'OpenAI API works!'"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ API toimii! Vastaus: {result}")
        print(f"💰 Käytetty tokeneita: {response.usage.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ API virhe: {str(e)}")
        if "authentication" in str(e).lower():
            print("🔑 Tarkista API key - se saattaa olla virheellinen")
        elif "quota" in str(e).lower():
            print("💳 API quota ylittynyt - tarkista laskutus")
        else:
            print("🌐 Tarkista internet-yhteys ja API status")
        return False

def show_usage_info():
    """Näyttää OpenAI API:n käytön tietoja."""
    print("\n💡 OPENAI API TIETOJA:")
    print("- gpt-3.5-turbo: ~$0.002/1000 tokenia")
    print("- gpt-4: ~$0.03/1000 tokenia") 
    print("- Uusille tileille usein $5 ilmaista krediittiä")
    print("- Seuraa kulutusta: https://platform.openai.com/usage")

if __name__ == "__main__":
    success = check_openai_setup()
    show_usage_info()
    
    if success:
        print("\n🎉 OpenAI API on valmis käyttöön!")
        print("💡 Voit nyt käyttää examples/playground.py:n OpenAI ominaisuuksia")
    else:
        print("\n🔧 Korjaa ongelmat ja aja skripti uudelleen")
        print("📖 Ohjeita: README.md tai examples/playground.py")