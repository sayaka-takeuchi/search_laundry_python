from pydantic import BaseModel


class CommentCreateSchema(BaseModel):
    comment_body: str

    class Config:
        orm_mode = True
