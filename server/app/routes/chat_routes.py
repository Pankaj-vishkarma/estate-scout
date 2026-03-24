from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid

from app.services.agent_service import run_agent
from app.config.db import db

# ✅ NEW: Auth dependency
from app.dependencies.auth_dependency import get_current_user

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


# 🔥 CHAT API (USER-SPECIFIC)
@router.post("/chat")
def chat(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("user_id")  # ✅ IMPORTANT

        properties = run_agent(request.message, user_id)

        # 🔥 GET USER SESSION (NOT GLOBAL)
        session = db.sessions.find_one({"user_id": user_id}, sort=[("created_at", -1)])

        # 🔥 CREATE SESSION IF NOT EXISTS
        if not session:
            session_id = str(uuid.uuid4())
            db.sessions.insert_one(
                {
                    "session_id": session_id,
                    "user_id": user_id,  # ✅ NEW
                    "messages": [],
                    "properties": [],
                    "history": [],
                    "created_at": datetime.utcnow(),
                }
            )
        else:
            session_id = session["session_id"]

        # 🔥 SAVE USER MESSAGE
        db.sessions.update_one(
            {"session_id": session_id},
            {
                "$push": {
                    "messages": {
                        "role": "user",
                        "content": request.message,
                        "createdAt": datetime.utcnow().isoformat(),
                    }
                }
            },
        )

        # 🔥 SAVE ASSISTANT MESSAGE
        reply_text = f"I found {len(properties)} properties for you."

        db.sessions.update_one(
            {"session_id": session_id},
            {
                "$push": {
                    "messages": {
                        "role": "assistant",
                        "content": reply_text,
                        "createdAt": datetime.utcnow().isoformat(),
                    }
                }
            },
        )

        # 🔥 SAVE LATEST PROPERTIES
        db.sessions.update_one(
            {"session_id": session_id},
            {"$set": {"properties": properties}},
        )

        # 🔥 SAVE HISTORY ENTRY (USER-SPECIFIC)
        db.sessions.update_one(
            {"session_id": session_id},
            {
                "$push": {
                    "history": {
                        "query": request.message,
                        "properties": properties,
                        "created_at": datetime.utcnow(),
                    }
                }
            },
        )

        return {"reply": reply_text, "properties": properties}

    except Exception as e:
        print(f"[Chat ERROR]: {e}")
        return {"reply": "Something went wrong while processing your request."}


# 🔥 HISTORY API (USER-SPECIFIC)
@router.get("/history")
def get_history(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("user_id")  # ✅ IMPORTANT

        # 🔥 GET USER SESSION ONLY
        session = db.sessions.find_one({"user_id": user_id}, sort=[("created_at", -1)])

        if not session:
            return {"messages": [], "properties": []}

        history = session.get("history", [])

        # 🔥 COMBINE ALL PROPERTIES
        all_properties = []
        for item in history:
            props = item.get("properties", [])
            if isinstance(props, list):
                all_properties.extend(props)

        return {
            "messages": session.get("messages", []),
            "properties": all_properties,
        }

    except Exception as e:
        print(f"[History ERROR]: {e}")
        return {"messages": [], "properties": []}
