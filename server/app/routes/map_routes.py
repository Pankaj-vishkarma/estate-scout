from fastapi import APIRouter, Query, HTTPException

router = APIRouter()

images = [
    "/images/apartment1.jpg",
    "/images/apartment2.jpg",
    "/images/apartment3.jpg",
    "/images/apartment4.jpg",
    "/images/apartment5.jpg",
    "/images/apartment6.jpg",
    "/images/apartment7.jpg",
    "/images/apartment8.jpg",
    "/images/apartment9.jpg",
    "/images/apartment10.jpg",
    "/images/apartment11.jpg",
    "/images/apartment12.jpg",
    "/images/apartment13.jpg",
]


@router.get("/map-simulator")
def get_map_image(q: str = Query(default="default")):
    try:
        # ✅ Validate input
        query = q.strip() if q else "default"

        if not images:
            raise HTTPException(status_code=500, detail="No images available")

        # ✅ deterministic selection
        index = len(query) % len(images)

        return {"image": images[index]}

    except Exception as e:
        print(f"[Map Route ERROR]: {e}")
        return {"image": images[0] if images else None}
