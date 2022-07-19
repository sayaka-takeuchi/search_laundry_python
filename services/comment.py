from sqlalchemy.orm import Session

from helpers.exceptions import raise_not_found
from models.comment import CommentModel
from schemas.comment import CommentCreateSchema


@raise_not_found
def get_comment(db: Session, comment_id: int):
    return db.query(CommentModel).get(comment_id)


def create_comment(db: Session, laundry_id: int, current_user_id: int, new_comment: CommentCreateSchema) -> CommentModel:
    comment = CommentModel(**new_comment.dict())
    comment.comment_laundry_id = laundry_id
    comment.comment_user_id = current_user_id
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(db: Session, comment_id: int):
    comment = get_comment(db=db, comment_id=comment_id)
    db.delete(comment)
    db.commit()
