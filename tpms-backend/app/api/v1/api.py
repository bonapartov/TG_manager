from fastapi import APIRouter

from app.api.v1.endpoints import auth, channels, posts

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(channels.router, prefix="/channels", tags=["channels"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])

# TODO: Add these endpoints when implemented
# from app.api.v1.endpoints import users, audit, metrics
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
# api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])