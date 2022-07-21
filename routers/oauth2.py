from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


from sqlalchemy.orm import Session
from starlette import status


from database import get_db
from helpers import auth_helper
from models.user import UserModel
from schemas.token import TokenSchema


router = APIRouter()


@router.post("/token", response_model=TokenSchema, tags=["oauth2"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    db_user = auth_helper.authenticate_user(db=db,
                                            email=form_data.username, password=form_data.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_helper.create_tokens(db=db, user=db_user)


@router.get("/refresh_token", response_model=TokenSchema, tags=["oauth2"])
async def refresh_token(current_user: UserModel = Depends(auth_helper.get_current_user_with_refresh_token),
                        db: Session = Depends(get_db)):
    """リフレッシュトークンでトークンを再取得"""
    return auth_helper.create_tokens(db=db, user=current_user)
