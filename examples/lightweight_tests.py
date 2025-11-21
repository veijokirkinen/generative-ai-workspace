#!/usr/bin/env python3
"""
Day 2 - Kevyempi versio 30 prompt testistä
Kevyempi lähestymistapa pienemmällä mallilla
"""

import csv
import datetime
import os

def log_prompt_result(prompt: str, model: str, params: dict, result: str, notes: str = ""):
    """Tallentaa prompt-testin tuloksen CSV-tiedostoon"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    os.makedirs("logs", exist_ok=True)
    csv_path = "logs/prompt_log.csv"
    file_exists = os.path.exists(csv_path)
    
    with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['date', 'prompt', 'model', 'params', 'result', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'date': timestamp,
            'prompt': prompt,
            'model': model, 
            'params': str(params),
            'result': result,
            'notes': notes
        })

def run_lightweight_tests():
    """Aja kevyet testit ilman suurta mallia"""
    try:
        from transformers import pipeline
        
        # Käytä pienempää, nopeampaa mallia
        print("⚡ Alustetaan kevyt malli...")
        generator = pipeline("text-generation", model="distilgpt2")
        print("✅ DistilGPT2 valmis!")
        
        # Vain 10 testiä nopeasti
        test_prompts = [
            ("Hello, my name is", "basic-greeting"),
            ("The weather today is", "weather-completion"),
            ("Python is a programming language that", "tech-description"),
            ("Once upon a time", "story-start"),
            ("To cook pasta, first", "instruction-cooking"),
            ("Q: What is AI? A:", "qa-format"),
            ("Happy: Joyful, Sad:", "analogy-emotions"),
            ("Translate: Bonjour", "translation-request"), 
            ("Write a poem about", "creative-writing"),
            ("The meaning of life is", "philosophical-question")
        ]
        
        print(f"\n🧪 Ajataan {len(test_prompts)} testiä...")
        
        for i, (prompt, category) in enumerate(test_prompts, 1):
            try:
                # Yksinkertaiset parametrit
                result = generator(
                    prompt, 
                    max_length=30, 
                    num_return_sequences=1,
                    pad_token_id=generator.tokenizer.eos_token_id
                )
                
                generated_text = result[0]['generated_text']
                
                log_prompt_result(
                    prompt=prompt,
                    model="distilgpt2",
                    params={"max_length": 30, "category": category},
                    result=generated_text,
                    notes=f"Lightweight test #{i}/10"
                )
                
                print(f"✅ Test {i}/10: {category}")
                
            except Exception as e:
                print(f"❌ Test {i} failed: {e}")
                
    except Exception as e:
        print(f"❌ Ei voida ajaa testejä: {e}")

def add_manual_prompt_examples():
    """Lisää manuaalisesti 20 prompt-esimerkkiä dokumentaatioksi"""
    
    manual_examples = [
        # Few-shot examples
        ("Example: Cat -> Animal, Rose -> Flower, Guitar -> ?", "few-shot", "Musical instrument", "Few-shot pattern recognition"),
        ("English: Hello, Spanish: Hola, English: Thank you, Spanish: ?", "few-shot", "Gracias", "Language translation pattern"),
        
        # Instruction prompting  
        ("Write a professional email subject for a team meeting", "instruction", "Weekly Team Sync - Nov 21 Agenda", "Professional communication"),
        ("Explain quantum computing in simple terms", "instruction", "Using quantum properties for powerful computation", "Technical explanation"),
        
        # Role-based prompting
        ("You are a chef. Recommend a quick breakfast recipe:", "role-based", "Scrambled eggs with toast (5 minutes)", "Culinary expertise simulation"),
        ("You are a teacher. Explain photosynthesis simply:", "role-based", "Plants use sunlight to make food from CO2 and water", "Educational role-play"),
        
        # Creative prompting
        ("Complete this story: The door creaked open and...", "creative", "revealed a hidden library filled with glowing books", "Story continuation"),
        ("Generate a haiku about technology:", "creative", "Screens glow brightly / Human and machine unite / Future awakens", "Poetry generation"),
        
        # Analytical prompting  
        ("What are the pros and cons of remote work?", "analytical", "Pros: flexibility, no commute. Cons: isolation, communication challenges", "Balanced analysis"),
        ("Explain the cause and effect: Social media and mental health", "analytical", "Constant comparison and validation seeking can impact self-esteem", "Causal relationship"),
        
        # Parameter variations
        ("Tell me about Mars (high temperature=0.9):", "parameter-test", "Mars, the mysterious red planet, dances through space!", "High creativity"),
        ("Tell me about Mars (low temperature=0.1):", "parameter-test", "Mars is the fourth planet from the Sun in our solar system", "Low creativity"),
        
        # Different prompting styles
        ("Formal: Please provide information about...", "style-formal", "I would be pleased to assist with your inquiry", "Formal register"),
        ("Casual: Hey, what's up with...", "style-casual", "Oh hey! Yeah that's pretty interesting stuff", "Casual register"),
        
        # Chain-of-thought
        ("Let's think step by step: How to bake a cake?", "chain-of-thought", "1. Gather ingredients 2. Mix batter 3. Bake 4. Cool", "Sequential reasoning"),
        ("Problem: 2+2×3. Think step by step:", "chain-of-thought", "First multiply: 2×3=6, then add: 2+6=8", "Mathematical reasoning"),
        
        # Zero-shot vs one-shot
        ("Classify sentiment: I love this product!", "zero-shot", "Positive", "No examples given"),
        ("Positive: Amazing! Negative: Terrible. Classify: Great job!", "one-shot", "Positive", "One example provided"),
        
        # Domain-specific
        ("Medical: Symptoms of diabetes include", "domain-medical", "Increased thirst, frequent urination, fatigue", "Medical knowledge"),
        ("Legal: A contract requires", "domain-legal", "Offer, acceptance, consideration, mutual obligation", "Legal concepts")
    ]
    
    print(f"\n📚 Lisätään {len(manual_examples)} manuaalista esimerkkiä...")
    
    for prompt, category, result, notes in manual_examples:
        log_prompt_result(
            prompt=prompt,
            model="manual-example",
            params={"category": category, "type": "documentation"},
            result=result,
            notes=notes
        )
    
    print("✅ Manuaaliset esimerkit lisätty!")

def main():
    """Main function"""
    print("🚀 Day 2 - Kevyt Prompt Testing")
    print("=" * 40)
    
    # Aja kevyet AI-testit
    run_lightweight_tests()
    
    # Lisää manuaaliset esimerkit
    add_manual_prompt_examples()
    
    # Tulokset
    csv_path = "logs/prompt_log.csv"
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            total_tests = len(lines) - 1  # -1 for header
        
        print(f"\n🎯 YHTEENVETO:")
        print(f"✅ Yhteensä {total_tests} prompt-testiä suoritettu")
        print(f"📊 Tulokset: {csv_path}")
        print(f"📁 Kategoriat: basic, few-shot, instruction, role-based, creative, analytical")
        print(f"🔧 Mallit: gpt2, distilgpt2, manual-examples")
    
    print("\n🎉 Day 2 Vaihe 2 valmis!")

if __name__ == "__main__":
    main()