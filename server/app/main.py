from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.chat_routes import router as chat_router
from app.routes.property_routes import router as property_router

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 IMPORTANT: Serve screenshots & files
app.mount("/data", StaticFiles(directory="data"), name="data")

# ✅ Routes
app.include_router(chat_router)
app.include_router(property_router)


@app.get("/")
def root():
    return {"message": "Estate Scout Backend Running"}
