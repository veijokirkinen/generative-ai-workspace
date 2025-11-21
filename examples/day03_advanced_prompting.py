"""
DAY 3 - Advanced Prompt Engineering
Edistyneet prompt-tekniikat ja parameter tuning
"""

import os
import pandas as pd
import json
from datetime import datetime
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from dotenv import load_dotenv

# Lataa environment variables
load_dotenv()

class AdvancedPromptTester:
    def __init__(self):
        print("🚀 DAY 3 - Advanced Prompt Engineering")
        print("="*60)
        
        # Initialize models
        self.setup_huggingface()
        self.setup_openai()
        
        # Results storage
        self.results = []
        self.csv_path = "logs/day03_advanced_prompts.csv"
        
    def setup_huggingface(self):
        """Setup Hugging Face model"""
        print("🤗 Alustetaan Hugging Face GPT2...")
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        self.tokenizer.pad_token = self.tokenizer.eos_token
        print("✅ GPT2 valmis!")
        
    def setup_openai(self):
        """Setup OpenAI (jos käytettävissä)"""
        self.openai_available = False
        api_key = os.getenv('OPENAI_API_KEY')
        
        if api_key and api_key != "your_openai_api_key_here":
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=api_key)
                self.openai_available = True
                print("✅ OpenAI API valmis (säästäväiseen käyttöön)")
            except Exception as e:
                print(f"⚠️  OpenAI setup epäonnistui: {e}")
        else:
            print("ℹ️  OpenAI ei käytettävissä - käytetään vain Hugging Face")
    
    def test_temperature_variations(self):
        """Test 1: Temperature parameter tuning"""
        print("\n🌡️  === TEST 1: TEMPERATURE VARIATIONS ===")
        
        base_prompt = "The future of artificial intelligence will"
        temperatures = [0.1, 0.5, 1.0, 1.5]
        
        for temp in temperatures:
            print(f"📊 Testing temperature {temp}...")
            
            # Hugging Face test
            response = self.generate_hf_response(
                base_prompt, 
                temperature=temp,
                max_new_tokens=100
            )
            
            self.log_result({
                'test_category': 'temperature_variation',
                'prompt': base_prompt,
                'temperature': temp,
                'model': 'gpt2',
                'response': response,
                'notes': f'Temperature {temp} test - creativity vs consistency'
            })
            
            print(f"   Temperature {temp}: {response[:100]}...")
        
        print("✅ Temperature tests completed!")
    
    def test_chain_of_thought(self):
        """Test 2: Chain-of-thought prompting"""
        print("\n🧠 === TEST 2: CHAIN-OF-THOUGHT PROMPTING ===")
        
        # Mathematical reasoning test
        math_problems = [
            {
                'problem': "A store sells apples for $2 per kg. If I buy 3.5 kg, how much do I pay?",
                'cot_prompt': "A store sells apples for $2 per kg. If I buy 3.5 kg, how much do I pay?\n\nLet me think step by step:\n1) Price per kg = $2\n2) Amount bought = 3.5 kg\n3) Total cost = price per kg × amount\n4) Total cost = $2 × 3.5 = $7\n\nTherefore, I pay $7."
            },
            {
                'problem': "If a train travels 60 km in 45 minutes, what is its speed in km/h?",
                'cot_prompt': "If a train travels 60 km in 45 minutes, what is its speed in km/h?\n\nLet me work through this step by step:\n1) Distance = 60 km\n2) Time = 45 minutes = 45/60 hours = 0.75 hours\n3) Speed = Distance ÷ Time\n4) Speed = 60 km ÷ 0.75 hours = 80 km/h\n\nThe train's speed is 80 km/h."
            }
        ]
        
        for i, problem in enumerate(math_problems, 1):
            print(f"📊 Testing CoT problem {i}...")
            
            # Direct prompt without CoT
            direct_response = self.generate_hf_response(
                problem['problem'],
                temperature=0.3,
                max_new_tokens=150
            )
            
            self.log_result({
                'test_category': 'direct_reasoning',
                'prompt': problem['problem'],
                'temperature': 0.3,
                'model': 'gpt2',
                'response': direct_response,
                'notes': 'Direct reasoning without chain-of-thought'
            })
            
            # Chain-of-thought prompt
            cot_response = self.generate_hf_response(
                problem['cot_prompt'] + "\n\nNow solve a similar problem:",
                temperature=0.3,
                max_new_tokens=150
            )
            
            self.log_result({
                'test_category': 'chain_of_thought',
                'prompt': problem['cot_prompt'] + "\n\nNow solve a similar problem:",
                'temperature': 0.3,
                'model': 'gpt2',
                'response': cot_response,
                'notes': 'Chain-of-thought reasoning with step-by-step breakdown'
            })
            
            print(f"   Direct: {direct_response[:80]}...")
            print(f"   CoT: {cot_response[:80]}...")
        
        print("✅ Chain-of-thought tests completed!")
    
    def test_system_vs_user_roles(self):
        """Test 3: System vs User message optimization"""
        print("\n👤 === TEST 3: SYSTEM VS USER ROLES ===")
        
        scenarios = [
            {
                'task': 'Creative writing',
                'system_prompt': "You are a creative writing assistant. Write engaging, descriptive content with vivid imagery.",
                'user_prompt': "Write a short description of a mysterious forest."
            },
            {
                'task': 'Technical explanation',
                'system_prompt': "You are a technical expert. Explain complex topics clearly and accurately with examples.",
                'user_prompt': "Explain what machine learning is."
            },
            {
                'task': 'Business analysis',
                'system_prompt': "You are a business consultant. Provide strategic, data-driven insights.",
                'user_prompt': "What are the main benefits of remote work for companies?"
            }
        ]
        
        for scenario in scenarios:
            print(f"📊 Testing {scenario['task']}...")
            
            # System + User combined (simulated with context)
            combined_prompt = f"System: {scenario['system_prompt']}\nUser: {scenario['user_prompt']}\nAssistant:"
            
            response = self.generate_hf_response(
                combined_prompt,
                temperature=0.7,
                max_new_tokens=200
            )
            
            self.log_result({
                'test_category': 'system_user_roles',
                'prompt': combined_prompt,
                'temperature': 0.7,
                'model': 'gpt2',
                'response': response,
                'notes': f'System+User role test for {scenario["task"]}'
            })
            
            print(f"   {scenario['task']}: {response[:100]}...")
        
        print("✅ System vs User role tests completed!")
    
    def test_parameter_ab_testing(self):
        """Test 4: A/B parameter testing"""
        print("\n🧪 === TEST 4: A/B PARAMETER TESTING ===")
        
        base_prompt = "Write a professional email to a client about project completion."
        
        # 6 parameter variants
        variants = [
            {'name': 'Conservative', 'temp': 0.2, 'top_p': 0.8, 'max_tokens': 150},
            {'name': 'Balanced', 'temp': 0.5, 'top_p': 0.9, 'max_tokens': 200},
            {'name': 'Creative', 'temp': 0.8, 'top_p': 0.95, 'max_tokens': 250},
            {'name': 'Focused', 'temp': 0.3, 'top_p': 0.7, 'max_tokens': 100},
            {'name': 'Diverse', 'temp': 1.0, 'top_p': 0.95, 'max_tokens': 300},
            {'name': 'Precise', 'temp': 0.1, 'top_p': 0.5, 'max_tokens': 120}
        ]
        
        for variant in variants:
            print(f"📊 Testing {variant['name']} variant...")
            
            response = self.generate_hf_response(
                base_prompt,
                temperature=variant['temp'],
                max_new_tokens=variant['max_tokens']
            )
            
            self.log_result({
                'test_category': 'ab_testing',
                'prompt': base_prompt,
                'temperature': variant['temp'],
                'top_p': variant.get('top_p', 0.9),
                'max_tokens': variant['max_tokens'],
                'variant_name': variant['name'],
                'model': 'gpt2',
                'response': response,
                'notes': f'A/B test variant: {variant["name"]}'
            })
            
            print(f"   {variant['name']}: {response[:80]}...")
        
        print("✅ A/B parameter testing completed!")
    
    def test_advanced_patterns(self):
        """Test 5: Advanced prompting patterns"""
        print("\n🎨 === TEST 5: ADVANCED PROMPT PATTERNS ===")
        
        # Meta-prompting
        meta_prompt = """You are an expert prompt engineer. Create a prompt that would generate a compelling product description for a smart home device.

The prompt should include:
1. Clear instructions
2. Target audience specification  
3. Key features to highlight
4. Tone and style guidelines

Generated prompt:"""
        
        meta_response = self.generate_hf_response(
            meta_prompt,
            temperature=0.6,
            max_new_tokens=200
        )
        
        self.log_result({
            'test_category': 'meta_prompting',
            'prompt': meta_prompt,
            'temperature': 0.6,
            'model': 'gpt2',
            'response': meta_response,
            'notes': 'Meta-prompting: creating prompts about creating prompts'
        })
        
        # Few-shot chain-of-thought
        few_shot_cot = """Examples of step-by-step problem solving:

Problem: Calculate 15% tip on $48 bill
Solution: 
Step 1: Convert 15% to decimal: 15% = 0.15
Step 2: Multiply bill by tip rate: $48 × 0.15 = $7.20
Answer: The tip is $7.20

Problem: How many hours in 3 days and 4 hours?
Solution:
Step 1: Convert days to hours: 3 days = 3 × 24 = 72 hours  
Step 2: Add extra hours: 72 + 4 = 76 hours
Answer: 76 hours

Problem: A car uses 8L fuel for 100km. How much for 350km?
Solution:"""
        
        few_shot_response = self.generate_hf_response(
            few_shot_cot,
            temperature=0.4,
            max_new_tokens=150
        )
        
        self.log_result({
            'test_category': 'few_shot_cot',
            'prompt': few_shot_cot,
            'temperature': 0.4,
            'model': 'gpt2',
            'response': few_shot_response,
            'notes': 'Few-shot chain-of-thought with mathematical reasoning'
        })
        
        print("✅ Advanced pattern tests completed!")
    
    def generate_hf_response(self, prompt, temperature=0.7, max_new_tokens=150):
        """Generate response using Hugging Face model"""
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=500)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    attention_mask=torch.ones_like(inputs)
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Remove original prompt from response
            response = response[len(prompt):].strip()
            
            return response
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def log_result(self, result_data):
        """Log result to CSV and memory"""
        result_data['timestamp'] = datetime.now().isoformat()
        result_data['day'] = 3
        
        # Add to memory
        self.results.append(result_data)
        
        # Save to CSV
        df = pd.DataFrame([result_data])
        
        # Append to existing CSV or create new
        try:
            existing_df = pd.read_csv(self.csv_path)
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass  # First time, create new file
        
        df.to_csv(self.csv_path, index=False)
    
    def generate_summary(self):
        """Generate summary of all tests"""
        print("\n📊 === DAY 3 SUMMARY ===")
        
        total_tests = len(self.results)
        categories = {}
        
        for result in self.results:
            category = result['test_category']
            categories[category] = categories.get(category, 0) + 1
        
        print(f"✅ Total tests completed: {total_tests}")
        print(f"📋 Test categories:")
        for category, count in categories.items():
            print(f"   • {category}: {count} tests")
        
        print(f"💾 Results saved to: {self.csv_path}")
        print(f"📁 CSV file size: {os.path.getsize(self.csv_path)} bytes")
        
        return {
            'total_tests': total_tests,
            'categories': categories,
            'csv_path': self.csv_path
        }
    
    def run_all_tests(self):
        """Run all Day 3 advanced prompt engineering tests"""
        print("🎯 Starting Day 3 Advanced Prompt Engineering Tests...")
        print("⏱️  Estimated time: 10-15 minutes")
        print()
        
        # Run all test suites
        self.test_temperature_variations()
        self.test_chain_of_thought()
        self.test_system_vs_user_roles() 
        self.test_parameter_ab_testing()
        self.test_advanced_patterns()
        
        # Generate summary
        summary = self.generate_summary()
        
        print("\n🎉 DAY 3 ADVANCED PROMPT ENGINEERING COMPLETE!")
        print(f"📊 Generated {summary['total_tests']} advanced test cases")
        print("🚀 Ready for portfolio presentation!")
        
        return summary

if __name__ == "__main__":
    tester = AdvancedPromptTester()
    results = tester.run_all_tests()