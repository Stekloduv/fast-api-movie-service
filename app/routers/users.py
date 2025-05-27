from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from app.database import get_db
from app.routers.auth import require_admin

router = APIRouter()


@router.get("/users/")
async def read_users():
    return {"message": "List of users"}


@router.post("/users/{user_id}/make_admin")
async def make_admin(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_admin),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user_obj = result.scalar_one_or_none()
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    user_obj.role = "admin"
    await db.commit()
    return {"detail": "User is now an admin"}
