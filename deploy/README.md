# Deploy Directory

Tässä kansiossa on deployment-skriptit, Docker-konfiguraatiot ja pilvipalvelu-setupit.

## Suunniteltu rakenne:
```
deploy/
├── Dockerfile           # Container image määritys
├── docker-compose.yml   # Multi-container setup
├── requirements.txt     # Python riippuvuudet
├── cloud/              # Pilvipalvelu konfiguraatiot
│   ├── gcp/            # Google Cloud Platform
│   ├── aws/            # Amazon Web Services
│   └── vercel/         # Vercel deployment
├── scripts/            # Deployment skriptit
│   ├── build.sh        # Buildi skripti
│   ├── deploy.sh       # Deployment skripti
│   └── rollback.sh     # Rollback skripti
└── config/             # Environment-kohtaiset configit
    ├── production.env
    ├── staging.env
    └── development.env
```

## Deployment kohteita:
- **Docker** - Containerisaatio
- **Google Cloud Run** - Serverless containers
- **Vercel** - Frontend ja API deployment  
- **Railway** - Full stack hosting
- **Render** - Web services