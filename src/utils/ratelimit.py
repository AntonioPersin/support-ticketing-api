from fastapi import Request
from functools import wraps

def rate_limit_decorator(limit: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, request: Request, **kwargs):
            limiter = request.app.state.limiter
            route_limiter = limiter.limit(limit)
            decorated_func = route_limiter(func)
            return await decorated_func(*args, request=request, **kwargs)
        return wrapper
    return decorator
