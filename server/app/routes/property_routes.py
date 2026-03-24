from fastapi import APIRouter
from app.config.db import properties_collection
from app.schemas.property_schema import property_serializer

router = APIRouter()


@router.get("/properties")
def get_properties():
    try:
        # 🔥 FIX 1: REMOVE LIMIT (IMPORTANT)
        properties = list(properties_collection.find().sort("_id", -1))

        # 🔥 DEBUG (CHECK IMAGE FIELD)
        print("[API] Raw Properties:", properties)

        # 🔥 FIX 2: Serialize properly
        result = [property_serializer(p) for p in properties]

        print("[API] Serialized Properties:", result)

        return result

    except Exception as e:
        print(f"[Property Route ERROR]: {e}")
        return []
