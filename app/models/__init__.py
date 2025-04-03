# Import all models here
# This way when we import Base to alembic env.py all models are also will be imported
# and changes applied to migration script

from app.database import Base  # noqa: F401
from app.models.category import Category  # noqa: F401
from app.models.comment import Comment  # noqa: F401
from app.models.post import Post, PostCategory  # noqa: F401
from app.models.profile import Profile  # noqa: F401
from app.models.role import Role, UserRole  # noqa: F401

# Import all models
from app.models.user import User  # noqa: F401
