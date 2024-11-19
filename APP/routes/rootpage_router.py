from fastapi import APIRouter

ROOTPAGE_ROUTER = APIRouter()

@ROOTPAGE_ROUTER.get("/")
async def read_root():
    return {"message": "Welcome to the API"}

