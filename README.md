# 🎫 Ticketing API

RESTful FastAPI aplikacija za upravljanje "ticketima" s podrškom za pretragu, filtriranje, caching, rate limiting, logiranje, agregirane statistike i statičku dokumentaciju.

---

## 🚀 Značajke

- ✅ Paginacija, filtriranje i pretraga ticketa
- ✅ Detaljni prikaz ticketa s punim JSON sadržajem
- ✅ Agregirane statistike (/stats)
- ✅ Redis-based caching
- ✅ Rate limiting (slowapi)
- ✅ Health check endpoint za k8s/Docker
- ✅ Docker + docker-compose podrška (uključuje Redis servis)
- ✅ CI workflow (GitHub Actions)
- ✅ Statička HTML dokumentacija preko Redoc
- ✅ Makefile za razvojne taskove

---

## 📁 Struktura projekta

.
├── src/                       # Izvorni kod aplikacije
│   ├── api/                   # Endpointi (tickets, stats)
│   ├── services/              # Logika za dohvat i obradu podataka
│   ├── utils/                 # Dekorator za rate limiting
│   ├── models.py              # Pydantic modeli
│   └── main.py                # Ulazna točka aplikacije
├── tests/                     # Testovi
├── docs/                      # Statička dokumentacija (docs.html)
├── .env                       # Konfiguracija varijabli okruženja
├── Dockerfile                 # Docker konfiguracija za aplikaciju
├── docker-compose.yml         # Docker konfiguracija za servise (API + Redis)
├── Makefile                   # Make taskovi (run/lint/test/build)
├── requirements.txt           # Python ovisnosti
└── .github/
    └── workflows/
        └── ci.yml             # CI workflow definicija (GitHub Actions)


---

## ⚙️ Postavljanje okruženja

### 1. Kloniraj repozitorij

```bash
git clone https://github.com/AntonioPersin/support-ticketing-api.git
cd support-ticketing-api
```

### 2. Kreiraj .env datoteku (na temelju primjera)

```bash
cp .env.example .env
```

---

## 🐳 Docker (Preporučeni način)

Pokreni aplikaciju i Redis s Docker Compose:

```bash
docker-compose up --build
```

### Aplikacija će biti dostupna na:

API: http://localhost:8000

Dokumentacija (Swagger): http://localhost:8000/docs

Dokumentacija (Redoc): http://localhost:8000/docs.html

Health check: http://localhost:8000/health

---

## 🧰 Makefile taskovi

```bash
make run         # Pokreni aplikaciju lokalno (uvicorn)
make lint        # Pokreni flake8 linter
make test        # Pokreni pytest testove
make build       # Build Docker image (ticketing-api)
make docker-up   # Pokreni servise (API + Redis) u pozadini
make docker-down # Zaustavi docker-compose servise
```

---

## 🧪 Testiranje

Testovi koriste pytest, httpx, te fastapi_cache.backends.InMemoryBackend.

Lokalno:

```bash
pytest tests
```

---

## 🧪 CI (GitHub Actions)

CI pipeline pokreće se automatski na svakom push/pull_request prema grani main:

Pokreće Redis servis

Instalira ovisnosti

Pokreće linting (flake8)

Pokreće testove (pytest)

---

## 🔐 Varijable okruženja (.env)

```markdown
| Varijabla  | Opis                   | Zadana vrijednost |
|------------|------------------------|-------------------|
| REDIS_HOST | Hostname Redis servera | localhost         |
| REDIS_PORT | Port Redis servera     | 6379              |

```

---

## 🧾 API Dokumentacija

Swagger: http://localhost:8000/docs

Redoc (custom statička): http://localhost:8000/docs.html

OpenAPI JSON: http://localhost:8000/openapi.json

---

## 📦 Build info

Python 3.11

FastAPI 0.111.0

Redis 7 (via Docker)

Caching: fastapi-cache2

Rate limiting: slowapi

Testing: pytest, httpx, pytest-asyncio

Linting: flake8

---

## 📝 License

Ovaj projekt koristi MIT licencu.