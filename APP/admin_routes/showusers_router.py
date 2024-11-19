from fastapi import APIRouter, Depends, HTTPException
from prisma import Prisma

SHOWUSERS_ROUTER = APIRouter()
db = Prisma()


@SHOWUSERS_ROUTER.get("/admin/all_users")
async def show_all_users():
    try:
        await db.connect()
        users = await db.user.find_many()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        await db.disconnect()
        
