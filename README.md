# Generative AI — Workspace

Yksi rivi: Työtila Generative AI -harjoituksille ja portfolio‑projekteille (RAG, prompt‑engineering, multimodal, deploy).

Tarkoitus
- Kerätä, testata ja julkaista Generative AI -demoja ja POC‑projekteja.
- Sisältää skriptit keskustelulokin keräämiseen, RAG‑proof‑of‑conceptit, multimodal‑demon ja deploy‑scaffoldin.

Kansiorakenne (suositus)
- README.md                ← tämä tiedosto
- .gitignore               ← estää .env, .venv, logs/ jne.
- .env.example             ← mallipohja salaisuuksille (ei arvoja)
- /scripts                 ← CLI‑skriptit (append_chat_log.py, clipboard_watcher.py)
- /logs                    ← lokit (yleensä ignored)
- /examples                ← testidatat ja esimerkkikutsut
- /app / /src              ← API / sovelluskoodi (FastAPI / Gradio)
- /deploy                  ← Dockerfile, docker‑compose, deploy‑scripts

Pika‑asennus (Linux/macOS / WSL)
1. Kloonaa repo ja luo virtuaaliympäristö
   git clone <repo-url>
   cd <repo>
   python -m venv .venv
   source .venv/bin/activate

2. Asenna riippuvuudet
   pip install -U pip
   pip install -r requirements.txt
   # tai jos ei requirements.txt:
   pip install transformers sentence-transformers langchain openai huggingface_hub \
               pinecone-client supabase gradio fastapi uvicorn

3. Lisää .env ‑tiedosto (kopioi .env.example)
   cp .env.example .env
   # täytä API‑avaimet: OPENAI_API_KEY, PINECONE_API_KEY, HUGGINGFACE_TOKEN, jne.

Käyttö — keskustelulokien tallennus
- Skripti: scripts/append_chat_log.py
- Esimerkki lisäämisestä:
  python scripts/append_chat_log.py --file logs/chat.log --author "Veijo" --message "Aloitetaan harjoitukset"
- Lisää leikepöydän sisältö (macOS):
  pbpaste | python scripts/append_chat_log.py --file logs/chat.log --author "Veijo"

Huom: logs/ on oletuksena .gitignore:ssa jotta lokit eivät päädy versionhallintaan.

Käyttö — playground ja demo
- Esimerkiksi paikallinen chat demo (FastAPI + Gradio):
  uvicorn app.main:app --reload
- Avaa selaimeen http://localhost:8000 tai Gradio‑URL.

Prompt‑logi ja versiointi
- Pidä prompt_log.csv tai prompt_log.jsonl (yksi objekti/rivi) kansiossa examples/ tai logs/
- Sarakkeet / kentät: date, task, prompt_id, prompt_text, model, params, result_summary, notes

Turvallisuus & hyvä käytös
- Älä commitoi .env tai salaisuuksia. Lisää .env ja logs/ .gitignoreen.
- Poista tai maskaa PII ennen lokien jakamista.
- Lisää prompt‑sanitization ja human‑in‑the‑loop kriittisiin päätöksiin.
- Rajoita editor‑oikeuksia julkisissa repossa.

Git‑käytännöt (suositus)
- Päähaara: main (tai trunk)
- Feature‑haarat: feature/day-xx‑<short>
- Commit‑viestit: lyhyt prefiksi + kuvaus, esim. "day03: add prompt variants"
- Tee usein committeja ja käytä PR‑tyyliä jos työskentelet muiden kanssa.

GitHub Copilot — vinkit VS Codeen
- Lisää tiedoston alkuun kommentti, joka kuvaa halutun toiminnallisuuden — Copilot ehdottaa koodia.
- Esimerkki: "# Generate a CLI script that appends messages to logs/chat.log with ISO8601 timestamps..."
- Hyväksy tai muokkaa ehdotuksia, testaa paikallisesti.

Hyviä jatkotoimia (prioriteetit)
1. JSONL‑muotoiset lokit analytiikkaa varten (yksi JSON objekti per rivi).  
2. Clipboard‑watcher (automaattinen lisäys leikepöydän päivityksestä).  
3. RAG POC: ingest -> vector DB (Pinecone/Supabase) -> retrieve -> LLM.  
4. Containerisoida backend (Dockerfile) ja deploy Cloud Run / Vercel.  
5. Case study / demo video + README + pricing / outreach template.

Esimerkki .env.example
OPENAI_API_KEY=
HUGGINGFACE_TOKEN=
PINECONE_API_KEY=
SUPABASE_URL=
SUPABASE_KEY=

Esimerkkikomentoja / Makefile‑taskit (voit lisätä Makefile)
- make venv     # luo ja aktivoi virtuaaliympäristön (per OS-komento)
- make install  # pip install -r requirements.txt
- make run      # uvicorn app.main:app --reload
- make log      # python scripts/append_chat_log.py --file logs/chat.log --author "Veijo"

Lisenssi
- Lisää haluamasi lisenssi (esim. MIT). Luo LICENSE‑tiedosto juureen.

Contributing
- Avaa issue ennen isompia muutoksia.
- Käytä feature‑haaroja ja tee selkeät PR‑kuvaukset.

Yhteystiedot
- Nimi: Veijo Kirkinen
- Portfolio / LinkedIn: https://www.linkedin.com/in/veijo-kirkinen-a86906194/

Muistiinpanot
- Tämä README on pohja. Päivitä sisältöä projektisi edetessä (dependencies, deploy‑ohjeet, contact).
- Tarvittaessa voin generoida valmiit scaffold‑tiedostot (Dockerfile, FastAPI scaffold, Makefile) — kirjoita "Luo scaffold".