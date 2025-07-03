import logging
from fastapi import APIRouter, Query, HTTPException, Request
from typing import Optional
from src.services.todos import fetch_tickets, fetch_ticket_by_id
from src.utils.ratelimit import rate_limit_decorator

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
@rate_limit_decorator("20/minute")
async def list_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    q: Optional[str] = Query(None, alias="search"),
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    request: Request = None
):
    logger.info(f"GET /tickets called with status={status}, priority={priority}, search={q}, limit={limit}, skip={skip}")
    try:
        tickets = await fetch_tickets()

        if status:
            tickets = [t for t in tickets if t.status == status]
            logger.info(f"Filtered tickets by status={status}, count={len(tickets)}")

        if priority:
            tickets = [t for t in tickets if t.priority == priority]
            logger.info(f"Filtered tickets by priority={priority}, count={len(tickets)}")

        if q:
            tickets = [t for t in tickets if q.lower() in t.title.lower()]
            logger.info(f"Filtered tickets by search query='{q}', count={len(tickets)}")

        paginated = tickets[skip: skip + limit]
        logger.info(f"Returning {len(paginated)} tickets after pagination")

        return paginated

    except Exception as e:
        logger.error(f"Error in list_tickets: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{ticket_id}")
@rate_limit_decorator("30/minute")
async def get_ticket(ticket_id: int, request: Request = None):
    logger.info(f"GET /tickets/{ticket_id} called")
    try:
        ticket = await fetch_ticket_by_id(ticket_id)
        logger.info(f"Ticket found with id={ticket_id}")
        return ticket
    except HTTPException as e:
        if e.status_code == 404:
            logger.warning(f"Ticket with id={ticket_id} not found")
        else:
            logger.error(f"HTTP error when fetching ticket id={ticket_id}: {e.detail}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Error in get_ticket with id={ticket_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
