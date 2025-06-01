from sqlalchemy.orm import Session
from app.models.user import User
from app.models.post import Post

class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, user_id: int, text: str):
        post = Post(user_id=user_id, text=text)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def get_posts_by_user(self, user_id: int):
        return self.db.query(Post).filter(Post.user_id == user_id).all()

    def delete_post(self, post_id: int, user_id: int):
        post = self.db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
        if post:
            self.db.delete(post)
            self.db.commit()
        return post