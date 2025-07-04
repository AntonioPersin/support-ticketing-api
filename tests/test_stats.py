import pytest


@pytest.mark.asyncio
async def test_get_ticket_stats(async_client):
    response = await async_client.get("/stats")

    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "open" in data
    assert "closed" in data
    assert "by_priority" in data
    assert all(p in data["by_priority"] for p in ["low", "medium", "high"])
