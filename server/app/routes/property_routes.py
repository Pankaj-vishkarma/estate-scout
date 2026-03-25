from fastapi import APIRouter, Depends, HTTPException
from app.config.db import properties_collection
from app.schemas.property_schema import property_serializer
from app.dependencies.auth_dependency import get_current_user
from pymongo.errors import PyMongoError

router = APIRouter()


@router.get("/properties")
def get_properties(
    limit: int = 20,
    current_user: dict = Depends(get_current_user),
):
    try:
        user_id = current_user.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # ✅ Pagination safety
        limit = min(max(limit, 1), 100)

        # 🔥 User-specific + pagination
        properties_cursor = (
            properties_collection.find({"user_id": user_id})
            .sort("_id", -1)
            .limit(limit)
        )

        properties = list(properties_cursor)

        # ✅ Serialize
        result = [property_serializer(p) for p in properties]

        return result

    except PyMongoError as e:
        print(f"[Property DB ERROR]: {e}")
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        print(f"[Property Route ERROR]: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch properties")
