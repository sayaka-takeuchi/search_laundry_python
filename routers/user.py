from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database import get_db
from schemas.user import UserRegisterResponseSchema, UserRegisterSchema
from services import user

router = APIRouter()


@router.post("/", tags=["user"], response_model=UserRegisterResponseSchema)
def register_user(new_user: UserRegisterSchema, db: Session = Depends(get_db)):
    registerd_user = user.register_user(db=db, new_user=new_user)
    return UserRegisterResponseSchema.from_orm(registerd_user)
