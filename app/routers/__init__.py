# Import all routers here
from app.routers.categories import router as categories_router
from app.routers.comments import router as comments_router
from app.routers.posts import router as posts_router
from app.routers.profiles import router as profiles_router
from app.routers.relationships_demo import router as relationships_demo_router
from app.routers.roles import router as roles_router
from app.routers.users import router as users_router


# Define __all__ to explicitly export these routers
__all__ = [
    'categories_router',
    'comments_router',
    'posts_router',
    'profiles_router',
    'relationships_demo_router',
    'roles_router',
    'users_router',
]
