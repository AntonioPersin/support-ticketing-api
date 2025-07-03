import pytest
from src.services.todos import fetch_tickets, fetch_ticket_by_id

@pytest.mark.asyncio
@pytest.mark.usefixtures("initialize_cache")
async def test_fetch_tickets_returns_list():
    tickets = await fetch_tickets()
    assert isinstance(tickets, list)
    assert tickets
    first = tickets[0]
    assert hasattr(first, "id")
    assert hasattr(first, "title")
    assert hasattr(first, "status")

@pytest.mark.asyncio
@pytest.mark.usefixtures("initialize_cache")
async def test_fetch_ticket_by_id_valid():
    ticket = await fetch_ticket_by_id(1)
    assert ticket.id == 1
    assert ticket.title
    assert ticket.original
    assert isinstance(ticket.original, dict)

@pytest.mark.asyncio
@pytest.mark.usefixtures("initialize_cache")
async def test_fetch_ticket_by_id_invalid():
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await fetch_ticket_by_id(999999)
    assert exc_info.value.status_code == 404
