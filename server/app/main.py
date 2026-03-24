from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.chat_routes import router as chat_router
from app.routes.property_routes import router as property_router

# ✅ NEW: Auth routes import
from app.routes.auth_routes import router as auth_router

app = FastAPI()

# ✅ CORS FIX (unchanged)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 IMPORTANT: Serve screenshots & files (unchanged)
app.mount("/data", StaticFiles(directory="data"), name="data")

# ✅ Routes (existing)
app.include_router(chat_router)
app.include_router(property_router)

# ✅ NEW: Auth routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


@app.get("/")
def root():
    return {"message": "Estate Scout Backend Running"}
