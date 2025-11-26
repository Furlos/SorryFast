from fastapi import APIRouter

test_router = APIRouter()
@test_router.get("/")
async def root():
    return {"message": "PostgreSQL Profile Analyzer готов к работе", "docs": "/docs", "status": "OK"}


@test_router.get("/health")
async def health():
    return {"status": "healthy", "database": "connected"}