from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

from database import Base


class UserModel(Base):
    __tablename__ = "user"

    """
    登録されたユーザーの情報を格納するモデル
    """

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_nickname = Column(String(255), nullable=False)
    user_mail_address = Column(String(255), nullable=False)
    user_password = Column(String(255), nullable=False)
    user_refresh_token = Column(String(255), nullable=False, default="")
    user_comments = relationship("CommentModel",
                                 cascade="all, delete-orphan",
                                 lazy="dynamic",
                                 back_populates="comment_user")
