from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

# ✅ Load env
load_dotenv()

# ✅ ENV variables
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
DATA_DIR = os.getenv("DATA_DIR", "data")

from app.routes.chat_routes import router as chat_router
from app.routes.property_routes import router as property_router
from app.routes.auth_routes import router as auth_router
from app.routes.map_routes import router as map_router

# ✅ App config
app = FastAPI(title="Estate Scout AI Backend", version="1.0.0")

# ✅ Ensure data folder exists
os.makedirs(DATA_DIR, exist_ok=True)

# ✅ CORS (env-based)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Static files (env-based)
app.mount("/data", StaticFiles(directory=DATA_DIR), name="data")

# ✅ Routes
app.include_router(chat_router)
app.include_router(property_router)
app.include_router(map_router)
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


# ✅ Root
@app.get("/")
def root():
    return {"message": "Estate Scout Backend Running"}


# ✅ Health check
@app.get("/health")
def health():
    return {"status": "ok"}
