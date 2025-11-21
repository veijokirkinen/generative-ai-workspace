#!/usr/bin/env python3
"""
Day 2 - 30 Prompt Experiments
Testaa 30 erilaista promptia systematisesti:
- Few-shot learning
- Instruction prompting 
- Role-based prompting
- Parameter variations
"""

import os
import sys
import csv
import datetime
from typing import Dict, Any
from dotenv import load_dotenv

# Lataa environment muuttujat
load_dotenv()

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

def run_30_prompt_experiments():
    """Aja 30 erilaista prompt-kokerilua"""
    print("🧪 === 30 PROMPT EXPERIMENTS ===")
    
    pipeline = setup_huggingface()
    if not pipeline:
        print("❌ Ei voida ajaa kokeita")
        return
    
    try:
        generator = pipeline("text-generation", model="gpt2")
        
        # CATEGORIA 1: INSTRUCTION PROMPTING (1-10)
        print("\n📝 Kategoria 1: Instruction Prompting")
        
        instructions = [
            "Write a professional email subject line for a meeting:",
            "Translate to French: Hello, how are you?",
            "Summarize this in one sentence: Artificial intelligence is transforming many industries.",
            "Complete this analogy: Bird is to sky as fish is to",
            "Generate a creative product name for a smart watch:",
            "Write a haiku about technology:",
            "Create a motivational quote about learning:",
            "Explain quantum computing in simple terms:",
            "Generate a unique business idea:",
            "Write a short story beginning: 'The door creaked open and...'"
        ]
        
        for i, prompt in enumerate(instructions, 1):
            try:
                result = generator(prompt, max_length=50, temperature=0.7, do_sample=True)
                log_prompt_result(
                    prompt=prompt,
                    model="gpt2",
                    params={"max_length": 50, "temperature": 0.7, "category": "instruction"},
                    result=result[0]['generated_text'],
                    notes=f"Instruction prompting test #{i}"
                )
                print(f"✅ Test {i}/30 completed")
            except Exception as e:
                print(f"❌ Test {i} failed: {e}")
        
        # CATEGORIA 2: FEW-SHOT LEARNING (11-20)
        print("\n🎯 Kategoria 2: Few-shot Learning")
        
        few_shot_prompts = [
            "Examples:\nInput: cat\nOutput: animal\nInput: rose\nOutput: flower\nInput: guitar\nOutput:",
            "Q: What is 2+2?\nA: 4\nQ: What is 5+3?\nA: 8\nQ: What is 7+6?\nA:",
            "Positive: I love this!\nNegative: I hate this.\nPositive: Amazing work!\nNegative:",
            "English: Hello\nSpanish: Hola\nEnglish: Thank you\nSpanish: Gracias\nEnglish: Goodbye\nSpanish:",
            "Problem: Find area of square with side 5\nSolution: 5*5 = 25\nProblem: Find area of square with side 8\nSolution:",
            "Formal: Good morning, sir.\nCasual: Hey there!\nFormal: I appreciate your assistance.\nCasual:",
            "City: Paris\nCountry: France\nCity: Tokyo\nCountry: Japan\nCity: London\nCountry:",
            "Input: happy\nEmotion: joy\nInput: angry\nEmotion: rage\nInput: scared\nEmotion:",
            "Singular: cat\nPlural: cats\nSingular: child\nPlural: children\nSingular: mouse\nPlural:",
            "Tech: AI\nDefinition: Artificial Intelligence\nTech: VR\nDefinition: Virtual Reality\nTech: IoT\nDefinition:"
        ]
        
        for i, prompt in enumerate(few_shot_prompts, 11):
            try:
                result = generator(prompt, max_length=len(prompt.split()) + 10, temperature=0.3)
                log_prompt_result(
                    prompt=prompt,
                    model="gpt2",
                    params={"max_length": len(prompt.split()) + 10, "temperature": 0.3, "category": "few-shot"},
                    result=result[0]['generated_text'],
                    notes=f"Few-shot learning test #{i}"
                )
                print(f"✅ Test {i}/30 completed")
            except Exception as e:
                print(f"❌ Test {i} failed: {e}")
        
        # CATEGORIA 3: ROLE-BASED PROMPTING (21-30)
        print("\n🎭 Kategoria 3: Role-based Prompting")
        
        role_prompts = [
            "You are a helpful teacher. Explain photosynthesis simply:",
            "You are a chef. Recommend a quick breakfast recipe:",
            "You are a travel guide. Suggest attractions in Paris:",
            "You are a fitness trainer. Give a 5-minute workout routine:",
            "You are a financial advisor. Explain the importance of saving:",
            "You are a tech support agent. Help with email setup:",
            "You are a creative writer. Start a mystery story:",
            "You are a doctor. Explain the benefits of exercise:",
            "You are a historian. Describe the Renaissance period briefly:",
            "You are a life coach. Give motivation for Monday morning:"
        ]
        
        for i, prompt in enumerate(role_prompts, 21):
            try:
                result = generator(prompt, max_length=70, temperature=0.8, do_sample=True)
                log_prompt_result(
                    prompt=prompt,
                    model="gpt2", 
                    params={"max_length": 70, "temperature": 0.8, "category": "role-based"},
                    result=result[0]['generated_text'],
                    notes=f"Role-based prompting test #{i}"
                )
                print(f"✅ Test {i}/30 completed")
            except Exception as e:
                print(f"❌ Test {i} failed: {e}")
                
    except Exception as e:
        print(f"❌ General error: {e}")

def main():
    """Main function"""
    print("🚀 Starting 30 Prompt Experiments...")
    print("This will take a few minutes...")
    print("=" * 50)
    
    run_30_prompt_experiments()
    
    print("\n✅ All 30 prompt experiments completed!")
    print("📊 Results saved to: logs/prompt_log.csv")
    print("\n🎯 Summary:")
    print("- Tests 1-10: Instruction prompting")
    print("- Tests 11-20: Few-shot learning")
    print("- Tests 21-30: Role-based prompting")

if __name__ == "__main__":
    main()