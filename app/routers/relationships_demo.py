from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.models.comment import Comment
from app.models.post import Post, PostCategory
from app.models.profile import Profile
from app.models.user import User


router = APIRouter(prefix='/relationships-demo', tags=['Relationships Demo'])


@router.get('/one-to-many/')
def one_to_many_relationship(db: Session = Depends(get_db)):
    """Demonstrate one-to-many relationship: User -> Posts

    A user can have multiple posts, but each post belongs to only one user.
    """
    # Query a user and their posts
    user = db.query(User).first()

    if not user:
        # Create a demo user if none exists
        user = User(
            email='demo@example.com',
            username='demouser',
            hashed_password='hashed_password_demo',  # noqa: S106
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create some posts for this user
        posts = [
            Post(title='First Post', content='Content of first post', user_id=user.id),
            Post(
                title='Second Post',
                content='Content of second post',
                user_id=user.id,
            ),
        ]
        db.add_all(posts)
        db.commit()

        # Refresh the user to get the related posts
        db.refresh(user)

    # Return the user and their posts
    return {
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'posts': [
            {
                'id': post.id,
                'title': post.title,
                'content': post.content,
            }
            for post in user.posts
        ],
        'relationship_type': 'one-to-many',
    }


@router.get('/many-to-one/')
def many_to_one_relationship(db: Session = Depends(get_db)):
    """Demonstrate many-to-one relationship: Posts -> User

    Many posts can belong to one user.
    """
    # Query posts and their author
    posts = db.query(Post).limit(5).all()

    if not posts:
        # If no posts, return empty list
        return {'posts': [], 'relationship_type': 'many-to-one'}

    # Return posts with their author
    return {
        'posts': [
            {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author': {
                    'id': post.author.id,
                    'username': post.author.username,
                },
            }
            for post in posts
        ],
        'relationship_type': 'many-to-one',
    }


@router.get('/one-to-one/')
def one_to_one_relationship(db: Session = Depends(get_db)):
    """Demonstrate one-to-one relationship: User <-> Profile

    A user has one profile and a profile belongs to one user.
    """
    # Query a user and their profile
    user = db.query(User).first()

    if not user:
        # Return empty response if no user found
        return {'message': 'No user found', 'relationship_type': 'one-to-one'}

    # Check if user has a profile
    if hasattr(user, 'profile') and user.profile is not None:
        profile = user.profile
    else:
        # Create a profile for the user
        profile = Profile(
            user_id=user.id,
            bio='This is a demo profile',
            website='https://example.com',
            location='Demo City',
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    # Return the user and their profile
    return {
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'profile': {
            'id': profile.id,
            'bio': profile.bio,
            'website': profile.website,
            'location': profile.location,
        },
        'relationship_type': 'one-to-one',
    }


@router.get('/many-to-many/')
def many_to_many_relationship(db: Session = Depends(get_db)):
    """Demonstrate many-to-many relationship: Posts <-> Categories

    Posts can have multiple categories, and categories can have multiple posts.
    """
    # Check if we have categories and posts
    categories = db.query(Category).all()
    posts = db.query(Post).all()

    # Create categories if none exist
    if not categories:
        categories = [
            Category(name='Technology', description='Tech related posts'),
            Category(name='Travel', description='Travel related posts'),
            Category(name='Food', description='Food and cooking posts'),
        ]
        db.add_all(categories)
        db.commit()
        for category in categories:
            db.refresh(category)

    # Ensure we have posts
    if not posts:
        return {'message': 'No posts found', 'relationship_type': 'many-to-many'}

    # Add categories to posts if not already assigned
    for post in posts[:2]:  # Only use first two posts for demo
        # Check if the post already has categories
        existing_categories = db.query(PostCategory).filter(PostCategory.post_id == post.id).all()
        if not existing_categories:
            # Create association objects instead of using .extend()
            for category in categories[:2]:  # Assign first two categories
                post_category = PostCategory(post_id=post.id, category_id=category.id)
                db.add(post_category)

    db.commit()

    # Query posts with their categories
    posts_with_categories = db.query(Post).limit(5).all()

    # Return posts with their categories
    return {
        'posts': [
            {
                'id': post.id,
                'title': post.title,
                'categories': [
                    {
                        'id': category.id,
                        'name': category.name,
                    }
                    for category in post.categories
                ],
            }
            for post in posts_with_categories
        ],
        'categories': [
            {
                'id': category.id,
                'name': category.name,
                'post_count': len(category.posts),
            }
            for category in categories
        ],
        'relationship_type': 'many-to-many',
    }


@router.get('/self-referential/')
def self_referential_relationship(db: Session = Depends(get_db)):
    """Demonstrate self-referential relationship: Comment -> Comment

    Comments can have replies (other comments).
    """
    # Check if we have posts
    post = db.query(Post).first()

    if not post:
        return {'message': 'No posts found', 'relationship_type': 'self-referential'}

    # Check if post has comments
    if not post.comments:
        # Create a parent comment
        user = db.query(User).first()
        if not user:
            return {
                'message': 'No users found',
                'relationship_type': 'self-referential',
            }

        parent_comment = Comment(
            content='This is a parent comment',
            user_id=user.id,
            post_id=post.id,
        )
        db.add(parent_comment)
        db.commit()
        db.refresh(parent_comment)

        # Create some replies to the parent comment
        replies = [
            Comment(
                content='This is a reply to the parent comment',
                user_id=user.id,
                post_id=post.id,
                parent_id=parent_comment.id,
            ),
            Comment(
                content='This is another reply to the parent comment',
                user_id=user.id,
                post_id=post.id,
                parent_id=parent_comment.id,
            ),
        ]
        db.add_all(replies)
        db.commit()

        # Refresh the parent comment to get the related replies
        db.refresh(parent_comment)

    # Query comments with their replies
    parent_comments = db.query(Comment).filter(Comment.parent_id.is_(None)).all()

    # Return comments with their replies
    return {
        'comments': [
            {
                'id': comment.id,
                'content': comment.content,
                'replies': [
                    {
                        'id': reply.id,
                        'content': reply.content,
                    }
                    for reply in comment.replies
                ],
            }
            for comment in parent_comments
        ],
        'relationship_type': 'self-referential',
    }
