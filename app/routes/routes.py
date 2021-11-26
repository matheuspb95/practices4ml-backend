from .user import router as user_router
from .practices import router as practices_router
from .comments import router as comments_router

routers = [user_router, practices_router, comments_router]
