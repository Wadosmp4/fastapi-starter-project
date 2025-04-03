# Import all schemas here
from app.schemas.category import (
    CategoryCreate,  # noqa: F401
    CategoryDetailResponse,  # noqa: F401
    CategoryResponse,  # noqa: F401
    CategoryUpdate,  # noqa: F401
)
from app.schemas.comment import (
    CommentCreate,  # noqa: F401
    CommentDetailResponse,  # noqa: F401
    CommentResponse,  # noqa: F401
    CommentUpdate,  # noqa: F401
)
from app.schemas.post import (
    PostCreate,  # noqa: F401
    PostDetailResponse,  # noqa: F401
    PostResponse,  # noqa: F401
    PostUpdate,  # noqa: F401
)
from app.schemas.profile import (
    ProfileCreate,  # noqa: F401
    ProfileDetailResponse,  # noqa: F401
    ProfileResponse,  # noqa: F401
    ProfileUpdate,  # noqa: F401
)
from app.schemas.role import (
    RoleCreate,  # noqa: F401
    RoleDetailResponse,  # noqa: F401
    RoleResponse,  # noqa: F401
    RoleUpdate,  # noqa: F401
)
from app.schemas.user import UserCreate, UserResponse, UserUpdate  # noqa: F401
