from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.dependencies.auth import get_db, get_current_user
from app.services.post_service import PostService
from app.schemas.post import PostCreate, PostResponse
from app.models.user import User

router = APIRouter()
post_service: PostService = Depends()

MAX_PAYLOAD_SIZE = 1 * 1024 * 1024  # 1 MB

@router.post("/add-post", response_model=PostResponse)
async def add_post(
    request: Request,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends()
):
    # Check payload size before parsing
    body = await request.body()
    if len(body) > MAX_PAYLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Payload size exceeds 1 MB limit"
        )

    try:
        post_data = PostCreate.parse_raw(await request.body())
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # Get only the needed data from service
    created_post = await post_service.create_post(post_data, current_user.id)
    
    # Return explicit response
    return PostResponse(
        post_id=created_post.id,
        text=created_post.text
    )


@router.get("/get-posts", response_model=list[PostResponse])
async def get_posts(
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends()
):
    posts = await post_service.get_user_posts(current_user.id)
    return posts

@router.delete("/{post_id}", response_model=None)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends()
):
    return await post_service.remove_post(current_user.id, post_id)