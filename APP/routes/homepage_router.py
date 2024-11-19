from fastapi import APIRouter, Depends
from APP.functions import validate_jwt
HOMEPAGE_ROUTER = APIRouter()

@HOMEPAGE_ROUTER.get("/homepage")
async def homepage(current_user: str = Depends(validate_jwt)):
    return "homepage. current user is " + current_user
