import pytest


@pytest.mark.asyncio
async def test_list_tickets_content(async_client):
    response = await async_client.get("/tickets/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        ticket = data[0]
        assert "id" in ticket
        assert "title" in ticket
        assert "status" in ticket
        assert "priority" in ticket
        assert "assignee" in ticket


@pytest.mark.asyncio
async def test_get_ticket_detail(async_client):
    response = await async_client.get("/tickets/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "title" in data
    assert "status" in data
    assert "priority" in data
    assert "assignee" in data
    assert "original" in data
    assert isinstance(data["original"], dict)


@pytest.mark.asyncio
async def test_get_ticket_by_id(async_client):
    response = await async_client.get("/tickets/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "title" in data
    assert "status" in data
    assert "priority" in data
    assert "assignee" in data
    assert "original" in data
    assert isinstance(data["original"], dict)


@pytest.mark.asyncio
async def test_get_ticket_not_found(async_client):
    response = await async_client.get("/tickets/999999")
    assert response.status_code == 404
