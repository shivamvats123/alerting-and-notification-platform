from .admin import router as admin_router
from .user import router as user_router
from .analytics import router as analytics_router

__all__ = ['admin_router', 'user_router', 'analytics_router']