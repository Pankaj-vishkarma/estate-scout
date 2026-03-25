from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid
from pymongo.errors import PyMongoError

from app.services.agent_service import run_agent
from app.config.db import db
from app.dependencies.auth_dependency import get_current_user

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


# ✅ Ensure index (performance)
db.sessions.create_index([("user_id", 1), ("created_at", -1)])


# 🔥 CHAT API (PRODUCTION READY)
@router.post("/chat")
def chat(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("user_id")

        # ✅ Validate user
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # ✅ Validate message
        message = request.message.strip()
        if not message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # 🔥 Run AI agent
        properties = run_agent(message, user_id)

        # 🔥 Get or create session
        session = db.sessions.find_one({"user_id": user_id}, sort=[("created_at", -1)])

        if not session:
            session_id = str(uuid.uuid4())

            db.sessions.insert_one(
                {
                    "session_id": session_id,
                    "user_id": user_id,
                    "messages": [],
                    "properties": [],
                    "history": [],
                    "created_at": datetime.utcnow(),
                }
            )
        else:
            session_id = session["session_id"]

        reply_text = f"I found {len(properties)} properties for you."

        # 🔥 SINGLE DB UPDATE (PERFORMANCE FIX)
        db.sessions.update_one(
            {"session_id": session_id},
            {
                "$push": {
                    "messages": {
                        "$each": [
                            {
                                "role": "user",
                                "content": message,
                                "createdAt": datetime.utcnow().isoformat(),
                            },
                            {
                                "role": "assistant",
                                "content": reply_text,
                                "createdAt": datetime.utcnow().isoformat(),
                            },
                        ]
                    },
                    "history": {
                        "query": message,
                        "properties": properties,
                        "created_at": datetime.utcnow(),
                    },
                },
                "$set": {"properties": properties},
            },
        )

        return {"reply": reply_text, "properties": properties}

    except PyMongoError as e:
        print(f"[Chat DB ERROR]: {e}")
        raise HTTPException(status_code=500, detail="Database error")

    except HTTPException:
        raise

    except Exception as e:
        print(f"[Chat ERROR]: {e}")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while processing your request.",
        )


# 🔥 HISTORY API (PRODUCTION READY)
@router.get("/history")
def get_history(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        session = db.sessions.find_one({"user_id": user_id}, sort=[("created_at", -1)])

        if not session:
            return {"messages": [], "properties": []}

        history = session.get("history", [])

        # 🔥 Efficient flatten
        all_properties = [
            prop
            for item in history
            for prop in item.get("properties", [])
            if isinstance(item.get("properties"), list)
        ]

        return {
            "messages": session.get("messages", []),
            "properties": all_properties,
        }

    except PyMongoError as e:
        print(f"[History DB ERROR]: {e}")
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        print(f"[History ERROR]: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch history",
        )
