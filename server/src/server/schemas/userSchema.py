from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)  # Changed from hashed_password to password

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  # (Note: orm_mode was renamed to from_attributes in Pydantic v2)