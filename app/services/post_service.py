# app/services/post_service.py

from app.repositories.post_repo import PostRepository
from app.schemas.post import PostCreate
from app.core.cache import post_cache

class PostService:
    def __init__(self, post_repo: PostRepository = PostRepository()):
        self.post_repo = post_repo

    async def create_post(self, post_data: PostCreate, user_id: int):
        post_id = await self.post_repo.create_post(post_data, user_id)
        if user_id in post_cache:
            del post_cache[user_id]  # Invalidate cache
        return {
            "id": post_id,
            "text": post_data.text
        }

    async def get_user_posts(self, user_id: int):
        if user_id in post_cache:
            return post_cache[user_id]  # ✅ Return from cache

        posts = await self.post_repo.get_posts_by_user(user_id)
        post_cache[user_id] = posts  # ✅ Store in cache
        return posts
    async def remove_post(self, user_id: int, post_id: int):
        post = await self.post_repo.delete_post(post_id, user_id)
        if post and user_id in post_cache:
            del post_cache[user_id]
