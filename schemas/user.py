from pydantic import BaseModel, constr


class UserBaseSchema(BaseModel):
    user_nickname: str
    user_mail_address: str

    class Config:
        orm_mode = True


class UserRegisterSchema(UserBaseSchema):
    user_password: constr(min_length=8)


class UserRegisterResponseSchema(UserBaseSchema):
    user_id: int
    user_password: str



class UserSchema(UserRegisterResponseSchema):
    pass
