from fastapi import APIRouter
from app.config.db import properties_collection
from app.schemas.property_schema import property_serializer

router = APIRouter()


@router.get("/properties")
def get_properties():
    try:
        # 🔥 FIX 1: Latest properties only (sorted by newest)
        properties = list(properties_collection.find().sort("_id", -1).limit(2))

        # 🔥 FIX 2: Serialize properly
        return [property_serializer(p) for p in properties]

    except Exception as e:
        print(f"[Property Route ERROR]: {e}")
        return []
