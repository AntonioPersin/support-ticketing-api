import logging
from fastapi import APIRouter, Request
from src.services.todos import fetch_tickets
from src.utils.ratelimit import rate_limit_decorator

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/stats")
@rate_limit_decorator("10/minute")
async def get_ticket_stats(request: Request = None):
    logger.info("GET /stats called")
    try:
        tickets = await fetch_tickets()

        total = len(tickets)
        open_ = sum(1 for t in tickets if t.status == "open")
        closed = total - open_

        by_priority = {"low": 0, "medium": 0, "high": 0}
        for t in tickets:
            by_priority[t.priority] += 1

        stats = {
            "total": total,
            "open": open_,
            "closed": closed,
            "by_priority": by_priority
        }
        logger.info(f"Stats calculated: {stats}")
        return stats

    except Exception as e:
        logger.error(f"Error while fetching stats: {e}", exc_info=True)
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="Internal Server Error")
