from pydantic import BaseModel, EmailStr, Field, validator


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)

    # ✅ Clean inputs
    @validator("name")
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        return v

    @validator("password")
    def validate_password(cls, v):
        v = v.strip()
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)

    @validator("password")
    def validate_password(cls, v):
        return v.strip()
