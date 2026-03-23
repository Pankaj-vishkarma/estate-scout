from fastapi import APIRouter
from pydantic import BaseModel
from app.services.agent_service import run_agent

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):
    try:
        properties = run_agent(request.message)

        # 🔥 IMPORTANT FIX: return proper reply
        return {"reply": f"I found {len(properties)} properties for you."}

    except Exception as e:
        print(f"[Chat ERROR]: {e}")
        return {"reply": "Something went wrong while processing your request."}
