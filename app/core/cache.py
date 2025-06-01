# app/core/cache.py

from cachetools import TTLCache
from typing import Dict

# Cache per user: key = user_id, value = list of posts
post_cache: Dict[int, TTLCache] = TTLCache(maxsize=1000, ttl=300)  # 5 minutes TTL
