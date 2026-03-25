from pydantic import BaseModel, Field, validator


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)

    # ✅ Clean + validate input
    @validator("message")
    def validate_message(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be empty")
        return v


class ChatResponse(BaseModel):
    reply: str
