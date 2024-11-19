from fastapi import APIRouter, Depends, HTTPException
from prisma import Prisma

DELETEALL_USERS_ROUTER = APIRouter()
db = Prisma()


@DELETEALL_USERS_ROUTER.delete("/admin/delete_all_users")
async def delete_all_users():
    try:
        await db.connect()
        await db.user.delete_many()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        await db.disconnect()
        
