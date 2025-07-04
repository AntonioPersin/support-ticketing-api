import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from src.api import tickets, stats
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pathlib

# Učitaj varijable iz .env u okolinu
load_dotenv()

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

# Postavke logiranja
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Postavi direktorij i datoteku
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"

app = FastAPI(title="Ticketing API")

# Inicijaliziraj limiter s Redis backendom za rate limiting (koristimo IP
# adresu)
limiter = Limiter(key_func=get_remote_address)

# Registriraj handler za rate limit prekoračenje
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
app.include_router(stats.router, tags=["stats"])

# Montiraj 'docs' direktorij (gdje je HTML)
app.mount("/docs-static", StaticFiles(directory=DOCS_DIR), name="docs")


@app.get("/")
@limiter.limit("10/minute")  # Limit root na 10 zahtjeva po minuti (primjer)
async def root(request: Request):
    logger.info("Root endpoint called")
    return {"message": "Ticketing API is running"}


@app.get("/health")
@limiter.limit("20/minute")  # Limit healthcheck na 20/min
async def health_check(request: Request):
    logger.info("Health check endpoint called")
    return {"status": "ok"}


@app.on_event("startup")
async def startup():
    redis_client = redis.Redis(
        host=redis_host,
        port=redis_port,
        decode_responses=True)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")


@app.get("/docs.html", include_in_schema=False)
async def custom_docs():
    path = DOCS_DIR / "docs.html"
    logger.info(f"Serving docs from: {path}")
    with open(path, "r") as f:
        content = f.read()
    logger.info(f"Docs content length: {len(content)}")
    return HTMLResponse(content=content)
