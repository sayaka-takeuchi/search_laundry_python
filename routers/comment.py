from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database import get_db
from schemas.comment import CommentCreateSchema
from schemas.result import Result
from services import comment

router = APIRouter()


@router.delete("/{comment_id}", response_model=Result, tags=["comment"])
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment.delete_comment(db=db, comment_id=comment_id)
    return Result(result=True)
