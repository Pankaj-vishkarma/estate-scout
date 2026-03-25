from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routes.chat_routes import router as chat_router
from app.routes.property_routes import router as property_router
from app.routes.auth_routes import router as auth_router
from app.routes.map_routes import router as map_router


# ✅ App config (production ready)
app = FastAPI(title="Estate Scout AI Backend", version="1.0.0")

# ✅ Ensure data folder exists (CRASH FIX)
os.makedirs("data", exist_ok=True)

# ✅ CORS (production safe)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # 🔥 replace with frontend URL in production
        # "https://your-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Serve static files (safe)
app.mount("/data", StaticFiles(directory="data"), name="data")

# ✅ Routes
app.include_router(chat_router)
app.include_router(property_router)
app.include_router(map_router)
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


# ✅ Root
@app.get("/")
def root():
    return {"message": "Estate Scout Backend Running"}


# ✅ Health check (for Render)
@app.get("/health")
def health():
    return {"status": "ok"}
