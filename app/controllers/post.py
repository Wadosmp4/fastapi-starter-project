from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

from app.controllers.base import BaseCRUDController
from app.exceptions import NotFoundException
from app.models.post import Post
from app.schemas.post import PostCreate, PostDetailResponse, PostUpdate


class PostController(BaseCRUDController[Post, PostCreate, PostUpdate]):
    """
    Post-specific CRUD controller with additional post-related operations.
    """

    def __init__(self):
        super().__init__(Post)

    def get_posts_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Post]:
        """
        Get all posts by a specific user.

        Args:
            db: Database session
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of posts by the user
        """
        return self.get_multi(db, skip=skip, limit=limit, filters={'user_id': user_id}, order_by=desc(Post.created_at))

    def get_posts_by_category(self, db: Session, category_id: int, skip: int = 0, limit: int = 100) -> list[Post]:
        """
        Get all posts in a specific category.

        Args:
            db: Database session
            category_id: Category ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of posts in the category
        """
        return self.get_multi(
            db, skip=skip, limit=limit, filters={'category_id': category_id}, order_by=desc(Post.created_at)
        )

    def get_published_posts(self, db: Session, skip: int = 0, limit: int = 100) -> list[Post]:
        """
        Get all published posts.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of published posts
        """
        return self.get_multi(
            db, skip=skip, limit=limit, filters={'is_published': True}, order_by=desc(Post.created_at)
        )

    def get_with_author_and_category(self, db: Session, post_id: int) -> PostDetailResponse:
        """
        Get a post with its author and category loaded.

        Args:
            db: Database session
            post_id: Post ID

        Returns:
            PostDetailResponse with author and category

        Raises:
            NotFoundException: If post not found
        """
        post = (
            db.query(Post)
            .options(joinedload(Post.author), joinedload(Post.category))
            .filter(Post.id == post_id)
            .first()
        )

        if not post:
            raise NotFoundException(f'Post with id {post_id} not found')

        return PostDetailResponse.from_orm(post)

    def publish_post(self, db: Session, post_id: int) -> Post:
        """
        Publish a post.

        Args:
            db: Database session
            post_id: Post ID to publish

        Returns:
            Updated post instance
        """
        post = self.get(db, post_id)
        return self.update(db, db_obj=post, obj_in={'is_published': True})

    def unpublish_post(self, db: Session, post_id: int) -> Post:
        """
        Unpublish a post.

        Args:
            db: Database session
            post_id: Post ID to unpublish

        Returns:
            Updated post instance
        """
        post = self.get(db, post_id)
        return self.update(db, db_obj=post, obj_in={'is_published': False})

    def search_posts(self, db: Session, search_term: str, skip: int = 0, limit: int = 100) -> list[Post]:
        """
        Search posts by title or content.

        Args:
            db: Database session
            search_term: Search term
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching posts
        """
        from sqlalchemy import or_

        query = db.query(Post).filter(or_(Post.title.ilike(f'%{search_term}%'), Post.content.ilike(f'%{search_term}%')))

        return query.order_by(desc(Post.created_at)).offset(skip).limit(limit).all()

    def get_recent_posts(self, db: Session, limit: int = 10) -> list[Post]:
        """
        Get the most recent posts.

        Args:
            db: Database session
            limit: Maximum number of records to return

        Returns:
            List of recent posts
        """
        return self.get_multi(db, skip=0, limit=limit, filters={'is_published': True}, order_by=desc(Post.created_at))


# Create a singleton instance
post_controller = PostController()
