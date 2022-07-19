from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


from sqlalchemy.orm import Session
from starlette import status


from database import get_db
from helpers import auth_helper
from schemas.token import TokenSchema


router = APIRouter()


@router.post("/token", response_model=TokenSchema, tags=["oauth2"])
async def token_from_email_and_password(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    db_user = auth_helper.authenticate_user(
        db=db, email=form_data.username, password=form_data.password)
    print("db_user", db_user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_helper.create_access_token(db_user)
    print("access_token", access_token)
    return {"access_token": access_token, "token_type": "bearer"}
