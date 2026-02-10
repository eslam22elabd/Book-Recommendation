from fastapi import APIRouter
from src.api.v1.endpoints import books

api_router = APIRouter()
api_router.include_router(books.router, tags=["books"])
