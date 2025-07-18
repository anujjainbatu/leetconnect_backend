from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, leaderboard, profile
from .config import settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LeetConnect API", 
    version="1.0.0",
    description="A FastAPI backend for LeetConnect Chrome extension"
)

# CORS: allow our Chrome extension origin to call these APIs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth.router)
app.include_router(leaderboard.router)
app.include_router(profile.router)

# Initialize database indexes on startup
# Disabled for serverless deployment to avoid event loop conflicts
# @app.on_event("startup")
# async def on_startup():
#     try:
#         from .db import ensure_indexes
#         await ensure_indexes()
#         logger.info("Database indexes created successfully")
#     except Exception as e:
#         logger.error(f"Failed to create database indexes: {e}")

# Add a health check endpoint
@app.get("/")
async def health_check():
    return {"status": "healthy", "message": "LeetConnect API is running"}

# Add a version endpoint
@app.get("/api/version")
async def get_version():
    return {"version": "1.0.0", "api": "LeetConnect"}

# Add an info endpoint
@app.get("/api/info")
async def get_info():
    return {
        "name": "LeetConnect Backend",
        "version": "1.0.0",
        "description": "FastAPI backend for LeetConnect Chrome extension",
        "endpoints": {
            "health": "/",
            "docs": "/docs",
            "auth": "/auth/*",
            "leaderboard": "/leaderboard/*",
            "profile": "/profile/*"
        }
    }

# Export the app for Vercel
handler = app
