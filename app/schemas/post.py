from pydantic import BaseModel, constr, Field

# Input model for creating posts
class PostCreate(BaseModel):
    text: constr(max_length=1_000_000)  # type: ignore

# Unified response model
class PostResponse(BaseModel):
    post_id: int
    text: str
    
    # class Config:
    #     from_attributes = True
    #     populate_by_name = True  # Allows using both field name and alias