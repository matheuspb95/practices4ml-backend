from .user import router as user_router
from .practices import router as practices_router
from .comments import router as comments_router
from .areas import router as areas_router
from .challenges import router as challenges_router

routers = [user_router, practices_router,
           comments_router, areas_router, challenges_router]
