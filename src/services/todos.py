import httpx
import logging
from fastapi import HTTPException
from typing import List
from src.models import Ticket, TicketDetail
from fastapi_cache.decorator import cache

logger = logging.getLogger(__name__)

DUMMY_TODOS_URL = "https://dummyjson.com/todos"
DUMMY_USERS_URL = "https://dummyjson.com/users"

@cache(expire=60)
async def fetch_todos() -> List[dict]:
    logger.info("Fetching todos from external API")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(DUMMY_TODOS_URL)
            resp.raise_for_status()
            data = resp.json()
            todos = data.get("todos", [])
            logger.info(f"Fetched {len(todos)} todos")
            return todos
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch todos: {e}")
            raise HTTPException(status_code=502, detail="Failed to fetch todos from external service")

@cache(expire=60)
async def fetch_users() -> dict:
    logger.info("Fetching users from external API")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(DUMMY_USERS_URL)
            resp.raise_for_status()
            data = resp.json()
            users = {user["id"]: user["username"] for user in data.get("users", [])}
            logger.info(f"Fetched {len(users)} users")
            return users
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch users: {e}")
            raise HTTPException(status_code=502, detail="Failed to fetch users from external service")

def compute_priority(id_: int) -> str:
    priorities = ["low", "medium", "high"]
    priority = priorities[id_ % 3]
    logger.debug(f"Computed priority '{priority}' for id {id_}")
    return priority

async def fetch_tickets() -> List[Ticket]:
    todos = await fetch_todos()
    users = await fetch_users()

    tickets = []
    for todo in todos:
        ticket = Ticket(
            id=todo["id"],
            title=todo["todo"],
            status="closed" if todo["completed"] else "open",
            priority=compute_priority(todo["id"]),
            assignee=users.get(todo["userId"], None),
            description=todo["todo"][:100] if todo.get("todo") else None
        )
        tickets.append(ticket)

    logger.info(f"Constructed {len(tickets)} Ticket objects")
    return tickets

@cache(expire=60)
async def fetch_ticket_by_id(ticket_id: int) -> TicketDetail:
    logger.info(f"Fetching ticket by ID: {ticket_id}")
    async with httpx.AsyncClient() as client:
        try:
            todo_resp = await client.get(f"{DUMMY_TODOS_URL}/{ticket_id}")
            if todo_resp.status_code == 404:
                logger.warning(f"Ticket with ID {ticket_id} not found")
                raise HTTPException(status_code=404, detail="Ticket not found")
            todo_resp.raise_for_status()
            todo = todo_resp.json()

            user_resp = await client.get(f"{DUMMY_USERS_URL}/{todo['userId']}")
            user_resp.raise_for_status()
            user = user_resp.json()

            ticket = TicketDetail(
                id=todo["id"],
                title=todo["todo"],
                status="closed" if todo["completed"] else "open",
                priority=compute_priority(todo["id"]),
                assignee=user["username"],
                description=todo["todo"][:100] if todo.get("todo") else None,
                original=todo
            )

            logger.info(f"Successfully fetched ticket ID {ticket_id}")
            return ticket

        except httpx.HTTPError as e:
            logger.error(f"Error fetching ticket ID {ticket_id}: {e}")
            raise HTTPException(status_code=502, detail="Failed to fetch ticket from external service")
