from fastapi import APIRouter, HTTPException
from bson import ObjectId
from pymongo.errors import PyMongoError

from app.schemas.user_schema import UserCreate, UserLogin
from app.config.db import db
from app.utils.auth import hash_password, verify_password, create_access_token

router = APIRouter()

users_collection = db["users"]

# ✅ Ensure index (runs once, safe)
users_collection.create_index("email", unique=True)


# 🔐 REGISTER
@router.post("/register")
async def register(user: UserCreate):
    try:
        # ✅ Normalize email
        email = user.email.strip().lower()

        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = hash_password(user.password)

        users_collection.insert_one(
            {
                "name": user.name.strip(),
                "email": email,
                "password": hashed_password,
            }
        )

        return {"message": "User registered successfully"}

    except PyMongoError as e:
        print(f"[AUTH DB ERROR]: {e}")
        raise HTTPException(status_code=500, detail="Database error")


# 🔐 LOGIN
@router.post("/login")
async def login(user: UserLogin):
    try:
        email = user.email.strip().lower()

        db_user = users_collection.find_one({"email": email})

        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        if not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        token = create_access_token(
            {
                "user_id": str(db_user["_id"]),
                "email": db_user["email"],
            }
        )

        return {
            "access_token": token,
            "user": {
                "id": str(db_user["_id"]),
                "name": db_user["name"],
                "email": db_user["email"],
            },
        }

    except PyMongoError as e:
        print(f"[AUTH DB ERROR]: {e}")
        raise HTTPException(status_code=500, detail="Database error")
