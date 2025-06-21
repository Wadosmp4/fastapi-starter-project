from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

from app.controllers.base import BaseCRUDController
from app.exceptions import NotFoundException
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentDetailResponse, CommentUpdate, UserInComment


class CommentController(BaseCRUDController[Comment, CommentCreate, CommentUpdate]):
    """
    Comment-specific CRUD controller with additional comment-related operations.
    """

    def __init__(self):
        super().__init__(Comment)

    def get_comments_by_post(self, db: Session, post_id: int, skip: int = 0, limit: int = 100) -> list[Comment]:
        """
        Get all comments for a specific post.

        Args:
            db: Database session
            post_id: Post ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of comments for the post
        """
        return self.get_multi(
            db, skip=skip, limit=limit, filters={'post_id': post_id}, order_by=desc(Comment.created_at)
        )

    def get_comments_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Comment]:
        """
        Get all comments by a specific user.

        Args:
            db: Database session
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of comments by the user
        """
        return self.get_multi(
            db, skip=skip, limit=limit, filters={'user_id': user_id}, order_by=desc(Comment.created_at)
        )

    def get_top_level_comments(self, db: Session, skip: int = 0, limit: int = 100) -> list[Comment]:
        """
        Get all top-level comments (no parent).

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of top-level comments
        """
        return self.get_multi(
            db, skip=skip, limit=limit, filters={'parent_id': None}, order_by=desc(Comment.created_at)
        )

    def get_replies(self, db: Session, parent_id: int, skip: int = 0, limit: int = 100) -> list[Comment]:
        """
        Get all replies to a specific comment.

        Args:
            db: Database session
            parent_id: Parent comment ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of reply comments
        """
        return self.get_multi(
            db, skip=skip, limit=limit, filters={'parent_id': parent_id}, order_by=desc(Comment.created_at)
        )

    def get_with_author_and_replies(self, db: Session, comment_id: int) -> CommentDetailResponse:
        """
        Get a comment with its author and replies loaded.

        Args:
            db: Database session
            comment_id: Comment ID

        Returns:
            CommentDetailResponse with author and replies

        Raises:
            NotFoundException: If comment not found
        """
        comment = (
            db.query(Comment)
            .options(joinedload(Comment.author), joinedload(Comment.replies))
            .filter(Comment.id == comment_id)
            .first()
        )

        if not comment:
            raise NotFoundException(f'Comment with id {comment_id} not found')

        # Format the response
        result = CommentDetailResponse.from_orm(comment)
        result.author = UserInComment(
            id=comment.author.id,
            username=comment.author.username,
        )

        return result

    def create_reply(self, db: Session, parent_id: int, obj_in: CommentCreate) -> Comment:
        """
        Create a reply to an existing comment.

        Args:
            db: Database session
            parent_id: Parent comment ID
            obj_in: Comment creation data

        Returns:
            Created reply comment

        Raises:
            NotFoundException: If parent comment not found
        """
        # Verify parent comment exists
        parent_comment = self.get(db, parent_id)
        if not parent_comment:
            raise NotFoundException(f'Parent comment with id {parent_id} not found')

        # Create reply with parent_id
        reply_data = obj_in.dict()
        reply_data['parent_id'] = parent_id

        return self.create(db, obj_in=CommentCreate(**reply_data))

    def get_comment_tree(self, db: Session, comment_id: int) -> CommentDetailResponse:
        """
        Get a comment with its full reply tree.

        Args:
            db: Database session
            comment_id: Comment ID

        Returns:
            CommentDetailResponse with full reply tree
        """
        return self.get_with_author_and_replies(db, comment_id)


# Create a singleton instance
comment_controller = CommentController()
