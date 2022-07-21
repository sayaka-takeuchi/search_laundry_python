from sqlalchemy.orm import Session

from helpers import auth_helper
from helpers.exceptions import raise_not_found
from models.user import UserModel
from schemas.user import UserRegisterSchema


@raise_not_found
def get_user(db: Session, user_id: int):
    return db.query(UserModel).get(user_id)


def register_user(db: Session, new_user: UserRegisterSchema):
    user = new_user.dict()
    hashed_password = auth_helper.get_password_hash(new_user.user_password)
    db_user = UserModel(**user)
    db_user.user_password = hashed_password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
