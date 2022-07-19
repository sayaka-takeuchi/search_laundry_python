from datetime import datetime, timedelta


from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from models.user import UserModel
from schemas.token import TokenDataSchema
from schemas.user import UserSchema
SECRET_KEY = "c0b8f6326260be4cbbb506368ad34d7379b8e24ab094d4cf5356ea36df36f87c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
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


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user_by_email(db: Session, user_email: str) -> UserModel or None:
    return db.query(UserModel).filter(
        UserModel.user_mail_address == user_email).first()


async def get_current_active_user_model(jwt_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
        token_data = TokenDataSchema(email=user_email)
    except JWTError:
        raise credentials_exception
    db_user = get_user_by_email(db, token_data.email)
    if db_user is None:
        raise credentials_exception
    return db_user


def get_current_active_user(db_current_user: UserModel = Depends(get_current_active_user_model)) -> UserSchema:
    return UserSchema.from_orm(db_current_user)


def create_access_token(user: UserModel):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": user.user_mail_address, "exp": expire}
    encoded_jwt = jwt.encode(claims=data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
