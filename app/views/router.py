from fastapi import APIRouter

from app.views.users.employee_view import router as users_router
from app.views.security.auth_view import router as auth_router

# Router
api_router = APIRouter(
    prefix="/api/v1",
)

# /users/*
api_router.include_router(users_router)

# /auth/*
api_router.include_router(auth_router)
