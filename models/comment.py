from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime
from sqlalchemy.orm import relationship

from database import Base


class CommentModel(Base):
    """
    ランドリーのコメントに関するデータを格納するモデル
    """
    __tablename__ = "comment"
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    comment_body = Column(Text, nullable=False)
    comment_created_at = Column(
        DateTime, nullable=False, default=datetime.utcnow)

    comment_user_id = Column(Integer,
                             ForeignKey("user.user_id",
                                        ondelete="CASCADE",
                                        name="comment__comment_user_id_fk"),
                             nullable=False)
    comment_laundry_id = Column(Integer,
                                ForeignKey("laundry.laundry_id",
                                           ondelete="CASCADE",
                                           name="comment__comment_laundry_id_fk"),
                                nullable=False)

    comment_user = relationship("UserModel", back_populates="user_comments")
    comment_laundry = relationship("LaundryModel",
                                   back_populates="laundry_comments")
