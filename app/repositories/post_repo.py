from sqlalchemy.orm import Session
from app.models.user import User
from app.models.post import Post
class PostRepository:
    @staticmethod
    def create_post(db: Session, user_id: int, text: str):
        post = Post(user_id=user_id, text=text)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def get_posts_by_user(db: Session, user_id: int):
        return db.query(Post).filter(Post.user_id == user_id).all()

    @staticmethod
    def delete_post(db: Session, post_id: int, user_id: int):
        post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
        if post:
            db.delete(post)
            db.commit()
        return post