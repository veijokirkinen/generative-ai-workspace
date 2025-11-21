# App Directory

Tässä kansiossa on sovelluskoodia - API:t, web-käyttöliittymät ja backend-komponentit.

## Suunniteltu rakenne:
```
app/
├── main.py              # FastAPI pääsovellus
├── api/                 # API endpoints
│   ├── __init__.py
│   ├── chat.py         # Chat API
│   ├── rag.py          # RAG endpoints
│   └── models.py       # Pydantic mallit
├── core/               # Ydintoiminnot
│   ├── __init__.py
│   ├── config.py       # Konfiguraatio
│   ├── database.py     # Tietokantayhteydet
│   └── security.py     # Turvallisuus
├── services/           # Business logic
│   ├── __init__.py
│   ├── llm_service.py  # LLM integraatio
│   ├── rag_service.py  # RAG implementaatio
│   └── vector_store.py # Vektoritietokanta
└── ui/                 # Frontend (Gradio/Streamlit)
    ├── __init__.py
    ├── chat_ui.py      # Chat-käyttöliittymä
    └── admin_ui.py     # Admin-paneeli
```

## Teknologiat:
- **FastAPI** - REST API
- **Gradio** - Nopea UI prototyyppeihin
- **Streamlit** - Dashboard ja admin
- **Pydantic** - Data validointi