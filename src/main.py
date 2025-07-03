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

app = FastAPI(title="Ticketing API")

# Inicijaliziraj limiter s Redis backendom za rate limiting (koristimo IP adresu)
limiter = Limiter(key_func=get_remote_address)

# Registriraj handler za rate limit prekoračenje
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
app.include_router(stats.router, tags=["stats"])

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
    redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
