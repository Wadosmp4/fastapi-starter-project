# Import all models here
# This way when we import Base to alembic env.py all models are also will be imported
# and changes applied to migration script

from app.database import Base  # noqa: F401

# example
# from app.models.users import Users  # noqa: ERA001
