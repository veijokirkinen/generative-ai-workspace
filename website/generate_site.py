"""
Oppimispäiväkirja Website Generator
Generoi automaattisesti HTML-sivuston harjoitukset/ kansiosta ja lokeista.
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

def parse_day_file(file_path):
    """Parsii day*.txt tiedoston ja palauttaa strukturoitua dataa."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Etsi päivämäärä
    date_match = re.search(r'📅 PÄIVÄMÄÄRÄ: (.+)', content)
    date = date_match.group(1) if date_match else "Ei määritelty"
    
    # Etsi kesto  
    duration_match = re.search(r'⏱️ KESTO: (.+)', content)
    duration = duration_match.group(1) if duration_match else "Ei määritelty"
    
    # Etsi tavoite
    target_match = re.search(r'🎯 TAVOITE: (.+)', content)
    target = target_match.group(1) if target_match else "Ei määritelty"
    
    # Etsi onnistumisprosentti
    success_match = re.search(r'🏆 ONNISTUMINEN: (.+)', content)
    success = success_match.group(1) if success_match else "0%"
    
    # Etsi opitut asiat sektion
    learned_section = ""
    learned_match = re.search(r'OPITUT ASIAT.*?(?=={50,})', content, re.DOTALL)
    if learned_match:
        learned_section = learned_match.group(0)
    
    # Laske tehtäviä (✅ merkkien määrä)
    completed_tasks = len(re.findall(r'✅', content))
    pending_tasks = len(re.findall(r'⏸️', content))
    
    return {
        'date': date,
        'duration': duration, 
        'target': target,
        'success': success,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'learned_section': learned_section,
        'file_path': file_path
    }

def generate_day_page(day_num, day_data):
    """Generoi yksittäisen päivän HTML-sivun."""
    
    html = f"""
<!DOCTYPE html>
<html lang="fi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DAY {day_num:02d} — Oppimispäiväkirja</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <nav>
        <div class="container">
            <a href="../index.html">← Takaisin etusivulle</a>
        </div>
    </nav>
    
    <header>
        <div class="container">
            <h1>DAY {day_num:02d}</h1>
            <p class="subtitle">{day_data['target']}</p>
            <div class="day-meta">
                <span>📅 {day_data['date']}</span>
                <span>⏱️ {day_data['duration']}</span>  
                <span>🏆 {day_data['success']}</span>
            </div>
        </div>
    </header>
    
    <div class="container">
        <div class="content">
            <!-- Tässä olisi koko day*.txt sisältö formatoituna -->
            <div class="raw-content">
                <pre>{open(day_data['file_path'], 'r', encoding='utf-8').read()}</pre>
            </div>
        </div>
    </div>
</body>
</html>
"""
    return html

def update_website():
    """Päivittää koko verkkosivuston harjoitukset/ kansiosta."""
    
    print("🔄 Päivitetään oppimispäiväkirja verkkosivusto...")
    
    harjoitukset_dir = Path("harjoitukset")
    website_dir = Path("website") 
    days_dir = website_dir / "days"
    
    # Luo days-kansio
    days_dir.mkdir(exist_ok=True)
    
    # Käy läpi kaikki day*.txt tiedostot
    day_files = sorted(harjoitukset_dir.glob("day*.txt"))
    days_data = {}
    
    for day_file in day_files:
        # Etsi päivänumero
        day_match = re.search(r'day(\d+)\.txt', day_file.name)
        if day_match:
            day_num = int(day_match.group(1))
            print(f"  📄 Käsitellään {day_file.name}...")
            
            # Parsii päivän data
            day_data = parse_day_file(day_file)
            days_data[day_num] = day_data
            
            # Generoi päivän sivu
            day_html = generate_day_page(day_num, day_data)
            day_page_path = days_dir / f"day{day_num:02d}.html"
            
            with open(day_page_path, 'w', encoding='utf-8') as f:
                f.write(day_html)
            
            print(f"    ✅ Luotu {day_page_path}")
    
    # Päivitä tilastot index.html:ään
    total_days = len(days_data)
    completed_days = sum(1 for d in days_data.values() if "100%" in d['success'])
    
    print(f"📊 Päivitetty sivusto: {completed_days}/{total_days} päivää valmis")
    print(f"🌐 Avaa: website/index.html")

def generate_navigation():
    """Luo navigaation kaikille päiville."""
    nav_html = ""
    harjoitukset_dir = Path("harjoitukset")
    day_files = sorted(harjoitukset_dir.glob("day*.txt"))
    
    for day_file in day_files:
        day_match = re.search(r'day(\d+)\.txt', day_file.name)
        if day_match:
            day_num = int(day_match.group(1))
            nav_html += f'<a href="days/day{day_num:02d}.html">DAY {day_num:02d}</a>\n'
    
    return nav_html

if __name__ == "__main__":
    # Vaihda työhakemisto oikeaan paikkaan
    os.chdir(Path(__file__).parent.parent)
    update_website()
    print("\n🎉 Verkkosivusto päivitetty onnistuneesti!")
    print("💡 Avaa website/index.html selaimessa nähdäksesi tuloksen.")