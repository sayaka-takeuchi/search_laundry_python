from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models.user import UserModel
from schemas.user import UserSchema
from services.user import get_user

SECRET_KEY = "c0b8f6326260be4cbbb506368ad34d7379b8e24ab094d4cf5356ea36df36f87c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 90
ACCESS_TOKEN_TOKEN_TYPE = "access_token"
REFRESH_TOKEN_TOKEN_TYPE = "refresh_token"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(db: Session, email: str, password: str) -> UserModel or None:
    db_user = get_user_by_email(db=db, user_email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.user_password):
        return None
    return db_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_refresh_token(token: str, db: Session):
    db_user = db.query(UserModel).filter(
        UserModel.user_refresh_token == token).first()
    if not db_user:
        return None
    return db_user


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user_by_email(db: Session, user_email: str) -> UserModel or None:
    return db.query(UserModel).filter(
        UserModel.user_mail_address == user_email).first()


def create_tokens(db: Session, user: UserModel):
    access_token_expire = datetime.utcnow(
    ) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    access_token_payload = {
        "user_id": user.user_id, "exp": access_token_expire, "token_type": "access_token"}
    refresh_token_payload = {
        "user_id": user.user_id, "exp": refresh_token_expire, "token_type": "refresh_token"}

    access_token = jwt.encode(
        claims=access_token_payload, key=SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode(
        claims=refresh_token_payload, key=SECRET_KEY, algorithm=ALGORITHM)

    user.user_refresh_token = refresh_token
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


def get_current_user_from_token(token: str = Depends(oauth2_scheme),
                                db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    token_type = payload.get("token_type")

    # TODO 本当はここでtoken_typeを引数で持ってきたいが1つ前のget_current_userとget_current_user_with_refresh_tokenのDepends内で引数を渡す渡し方がわからなかった
    # # トークンタイプが一致することを確認
    # if payload['token_type'] != token_type:
    #     raise HTTPException(status_code=401, detail=f'トークンタイプ不一致')

    user_id = payload.get("user_id")
    db_user: UserModel = get_user(db=db, user_id=user_id)

    # リフレッシュトークンの場合、受け取ったものとDBに保存されているものが一致するか確認
    if token_type == REFRESH_TOKEN_TOKEN_TYPE and db_user.user_refresh_token != token:
        raise HTTPException(status_code=401, detail='リフレッシュトークン不一致')

    return db_user


async def get_current_user(current_user: UserModel = Depends(get_current_user_from_token)) -> UserSchema:
    """アクセストークンからログイン中のユーザーを取得
    Dependsは独立した関数の中では使えない(基本的にはルートで使用する)
    ただし、Dependsで繋がっている関数であればルートでなくても使用可能
    https://github.com/tiangolo/fastapi/issues/1693#issuecomment-665833384
    """
    return UserSchema.from_orm(current_user)


async def get_current_user_with_refresh_token(current_user: UserModel = Depends(get_current_user_from_token)) -> UserSchema:
    """リフレッシュトークンからログイン中のユーザーを取得"""
    return current_user
