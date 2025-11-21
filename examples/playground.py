#!/usr/bin/env python3
"""
Day 2 - AI Playground Script
Testaa OpenAI tai Hugging Face API:a eri prompteilla ja parametreilla.
Tallentaa tulokset prompt_log.csv tiedostoon.
"""

import os
import csv
import datetime
from typing import Dict, Any
from dotenv import load_dotenv

# Lataa environment muuttujat
load_dotenv()

def setup_openai():
    """Alustaa OpenAI API:n jos API-avain on saatavilla"""
    try:
        import openai
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if openai.api_key:
            print("✅ OpenAI API alustettu")
            return openai
        else:
            print("❌ OPENAI_API_KEY puuttuu .env tiedostosta")
            return None
    except ImportError:
        print("❌ OpenAI kirjasto ei ole asennettu")
        return None

def setup_huggingface():
    """Alustaa Hugging Face API:n"""
    try:
        from transformers import pipeline
        print("✅ Hugging Face Transformers alustettu")
        return pipeline
    except ImportError:
        print("❌ Transformers kirjasto ei ole asennettu")
        return None

def log_prompt_result(prompt: str, model: str, params: Dict[str, Any], result: str, notes: str = ""):
    """Tallentaa prompt-testin tuloksen CSV-tiedostoon"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Luo logs kansio jos ei ole olemassa
    os.makedirs("logs", exist_ok=True)
    
    # CSV tiedoston polku
    csv_path = "logs/prompt_log.csv"
    
    # Tarkista onko tiedosto olemassa (header)
    file_exists = os.path.exists(csv_path)
    
    with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['date', 'prompt', 'model', 'params', 'result', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Kirjoita header jos tiedosto on uusi
        if not file_exists:
            writer.writeheader()
        
        # Kirjoita data
        writer.writerow({
            'date': timestamp,
            'prompt': prompt,
            'model': model, 
            'params': str(params),
            'result': result,
            'notes': notes
        })
    
    print(f"📝 Tallennettu: {csv_path}")

def test_huggingface_basic():
    """Testaa Hugging Face API:a perusmalleilla"""
    pipeline = setup_huggingface()
    if not pipeline:
        return
    
    print("\n🤗 === HUGGING FACE TESTIT ===")
    
    # Test 1: Basic text generation
    try:
        generator = pipeline("text-generation", model="gpt2")
        prompt = "The future of artificial intelligence is"
        result = generator(prompt, max_length=50, num_return_sequences=1)
        generated_text = result[0]['generated_text']
        
        log_prompt_result(
            prompt=prompt,
            model="gpt2", 
            params={"max_length": 50, "num_return_sequences": 1},
            result=generated_text,
            notes="Basic text generation test"
        )
        
        print(f"Input: {prompt}")
        print(f"Output: {generated_text}")
        
    except Exception as e:
        print(f"❌ HuggingFace testi epäonnistui: {e}")

def test_openai_basic():
    """Testaa OpenAI API:a jos saatavilla"""
    openai = setup_openai()
    if not openai:
        print("⚠️ OpenAI API ei saatavilla, ohitetaan OpenAI testit")
        return
    
    print("\n🔥 === OPENAI TESTIT ===")
    
    # Test 1: Basic completion
    try:
        prompt = "Write a short poem about programming:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        
        result = response.choices[0].text.strip()
        
        log_prompt_result(
            prompt=prompt,
            model="text-davinci-003",
            params={"max_tokens": 100, "temperature": 0.7},
            result=result,
            notes="OpenAI basic completion test"
        )
        
        print(f"Input: {prompt}")
        print(f"Output: {result}")
        
    except Exception as e:
        print(f"❌ OpenAI testi epäonnistui: {e}")

def run_prompt_experiments():
    """Aja erilaisia prompt-kokeita"""
    print("\n🧪 === PROMPT EXPERIMENTS ===")
    
    pipeline = setup_huggingface()
    if not pipeline:
        print("❌ Ei voida ajaa kokeita ilman AI mallia")
        return
    
    # Few-shot learning example
    few_shot_prompt = """Examples:
    Happy -> Joyful
    Sad -> Melancholic  
    Angry -> Furious
    Excited ->"""
    
    try:
        generator = pipeline("text-generation", model="gpt2")
        result = generator(few_shot_prompt, max_length=len(few_shot_prompt.split()) + 5)
        
        log_prompt_result(
            prompt=few_shot_prompt,
            model="gpt2",
            params={"max_length": len(few_shot_prompt.split()) + 5, "technique": "few-shot"},
            result=result[0]['generated_text'],
            notes="Few-shot learning test - emotion mapping"
        )
        
        print("Few-shot test completed ✅")
        
    except Exception as e:
        print(f"❌ Few-shot testi epäonnistui: {e}")

def main():
    """Main function - aja kaikki testit"""
    print("🚀 Day 2 - AI Playground - Käynnistetään...")
    print("=" * 50)
    
    # Testaa eri API:t
    test_huggingface_basic()
    test_openai_basic() 
    run_prompt_experiments()
    
    print("\n✅ Playground testit suoritettu!")
    print("📊 Tulokset tallennettu: logs/prompt_log.csv")
    print("\nSeuraava: Luo 30 erilaista prompt-testiä manuaalisesti!")

if __name__ == "__main__":
    main()