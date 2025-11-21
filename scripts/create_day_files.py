"""
Luo loput day*.txt tiedostot 14 päivän ohjelman mukaan
"""

import os
from pathlib import Path

# 14 päivän ohjelma
days_program = {
    5: {
        "title": "DOKUMENTOINTI & VIIKON RETROSPEKTIIVI",
        "duration": "4 tuntia",
        "target": "Siisti repo, kirjoita ensimmäisen viikon retrospektiivi ja parannussuunnitelma",
        "tasks": [
            "Päivitä README: miten ajaa projektia, dependencies, env-muuttujat",
            "Kirjoita Week 1 retrospective: mitä opit, mitä jäi kesken, mitkä promptit toimivat parhaiten",
            "Lisää TODO list viikolle 2"
        ],
        "deliverable": "README päivitetty, retrospective.md tiedosto",
        "commit": "day05: docs + week1 retrospective"
    },
    6: {
        "title": "EMBEDDINGS JA VECTOR DB SETUP",
        "duration": "4 tuntia", 
        "target": "Luo embeddings-workflow ja kytke vector DB (Pinecone tai Supabase)",
        "tasks": [
            "Valitse vector-DB ja tee ilmainen trial (Pinecone tai Supabase)",
            "Kirjoita skripti: scripts/ingest_docs.py",
            "Indeksoi ~50 dokumenttia (voit käyttää omia brändimateriaaleja tai demo-datasettiä)"
        ],
        "deliverable": "Ingest script + small indexed dataset",
        "commit": "day06: embeddings + vector db ingest"
    },
    7: {
        "title": "RAG POC",
        "duration": "4 tuntia",
        "target": "Rakentaa minimal RAG proof-of-concept: query → retrieve → prompt with context → answer",
        "tasks": [
            "Implement retrieval + reformat prompt: include top-k docs as context",
            "Testaa useilla kysymyksillä (FAQ tyyppiset) ja mittaa relevanttius", 
            "Lisää re-ranking (simple cosine re-rank) ja tallenna query/response log"
        ],
        "deliverable": "rag_demo/ with code + example queries + results",
        "commit": "day07: rag poc implemented"
    },
    8: {
        "title": "CHUNKING, METADATA JA PAREMPI RETRIEVAL",
        "duration": "4 tuntia",
        "target": "Paranna RAG: chunking, metadata, ja hybrid search",
        "tasks": [
            "Implementoi chunking (chunk size 500-800 chars, overlap 100)",
            "Lisää metadata (source, section, date) indeksointiin",
            "Testaa hybrid search: BM25 (if available) + embeddings"
        ],
        "deliverable": "Improved ingest script + tests",
        "commit": "day08: chunking + metadata"
    },
    9: {
        "title": "FINE-TUNING INTRODUCTION (LORA/PEFT)",
        "duration": "4 tuntia",
        "target": "Teoriat ja pieni käytännön kokeilu LoRA:lla pienen datan kanssa",
        "tasks": [
            "Lue LoRA/PEFT-opas (Hugging Face blog)",
            "Kokeile pienen datasetin LoRA-fine-tuning (esim. small llama-like model or opt-small on HF)",
            "Tallenna ennen/jälkeen esimerkit ja analysoi muutokset"
        ],
        "deliverable": "fine_tune/ repo with scripts + before_after_examples",
        "commit": "day09: lora experiment"
    },
    10: {
        "title": "CONTAINER & DEPLOY POC",
        "duration": "4 tuntia",
        "target": "Containerisoida RAG/chat app ja julkaista testipalvelimelle (Cloud Run/Vercel)",
        "tasks": [
            "Luo Dockerfile ja docker-compose (jos tarv)",
            "Testaa container paikallisesti: docker build -t rag-demo . && docker run -p 8000:8000 rag-demo",
            "Deploy: Vercel for front, Cloud Run for API tai Heroku"
        ],
        "deliverable": "Dockerfile + deployment README + live endpoint",
        "commit": "day10: dockerize + deploy steps"
    },
    11: {
        "title": "MULTIMODAL LISÄOMINAISUUS",
        "duration": "2 tuntia",
        "target": "Integroida basic image generation flow (brand images)",
        "tasks": [
            "Kokeile DALL·E/Stable Diffusion API generate (single prompt)",
            "Lisää endpoint generate_image ja tallenna kuvat / static folderiin"
        ],
        "deliverable": "images_demo/ with example outputs",
        "commit": "day11: image gen POC"
    },
    12: {
        "title": "MONITORING & COST TRACKING", 
        "duration": "2 tuntia",
        "target": "Laske token cost arvio ja lisää basic logging",
        "tasks": [
            "Lisää token counting ja cost per request laskuri",
            "Tallenna latency metrics (simple timestamp diffs)",
            "Tee yksinkertainen cost_estimate.md (1k requests, monthly)"
        ],
        "deliverable": "monitoring/ basic logs + cost_estimate.md",
        "commit": "day12: monitoring + cost calc"
    },
    13: {
        "title": "SECURITY & PROMPT-INJECTION TEST",
        "duration": "2 tuntia", 
        "target": "Perusturva ja adversarial-testit",
        "tasks": [
            "Implementoi simple input sanitization (strip html, remove suspicious tokens)",
            "Testaa prompt injection -tyyppisiä syötteitä ja dokumentoi vasteet",
            "Lisää human-in-the-loop flag for critical responses"
        ],
        "deliverable": "security_checks.md + example attacks and mitigations",
        "commit": "day13: security checks"
    },
    14: {
        "title": "PORTFOLIO MATERIAALI JA OUTREACH",
        "duration": "2 tuntia",
        "target": "Viimeistellä Week 1-2 deliverablet, kirjoittaa lyhyt case study ja valmistella outreach",
        "tasks": [
            "Kirjoita lyhyt case study (README/CASE_STUDY.md): ongelma, ratkaisu, tekninen arkkitehtuuri, tulokset",
            "Luo 2-3 demo-screenrecordia (Loom/OBS, 1-2 min)",
            "Valmistele outreach email template ja lista 5 potentiaalista kontaktoitavaa"
        ],
        "deliverable": "CASE_STUDY.md, demo-linkit ja outreach list",
        "commit": "day14: portfolio + outreach prep"
    }
}

def create_day_file(day_num, day_info):
    """Luo day*.txt tiedosto annetulla sisällöllä"""
    
    tasks_section = ""
    for i, task in enumerate(day_info["tasks"], 1):
        # Yksinkertainen task formatting ilman split-logiikkaa
        tasks_section += f"⏸️ {i}. TEHTÄVÄ {i}\n"
        tasks_section += f"   - {task}\n\n"
    
    content = f"""================================================================================
                      DAY {day_num:02d} - {day_info["title"]}
================================================================================

📅 PÄIVÄMÄÄRÄ: [Odottaa toteutusta]
⏱️ KESTO: ~{day_info["duration"]}
🎯 TAVOITE: {day_info["target"]}

================================================================================
                                  TEHTÄVÄLISTA
================================================================================

{tasks_section}
================================================================================
                              TAVOITTEET
================================================================================

🎯 TEKNISET TAVOITTEET:
   • {day_info["target"]}

🧠 OPPIMIS TAVOITTEET:
   • [Määritellään harjoituksen aikana]

📊 DELIVERABLE:
   • {day_info["deliverable"]}
   • Commit: "{day_info["commit"]}"

================================================================================
                            ODOTTAA TOTEUTUSTA...
================================================================================

[Tämä tiedosto päivitetään DAY {day_num} harjoitusten aikana]

================================================================================"""

    return content

if __name__ == "__main__":
    harjoitukset_dir = Path("harjoitukset")
    
    # Luo day05.txt - day14.txt
    for day_num in range(5, 15):
        day_file = harjoitukset_dir / f"day{day_num:02d}.txt"
        
        if not day_file.exists() and day_num in days_program:
            print(f"📝 Luodaan {day_file.name}...")
            content = create_day_file(day_num, days_program[day_num])
            
            with open(day_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   ✅ Luotu {day_file}")
    
    print("\n🎉 Kaikki day*.txt tiedostot luotu!")
    print("💡 Aja: python website/generate_site.py päivittääksesi verkkosivuston")