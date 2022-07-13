from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.orm import relationship
from database import Base


class LaundryModel(Base):
    __tablename__ = "laundry"

    laundry_id = Column(Integer, primary_key=True, auto_increment=True)
    laundry_name = Column(String(255), nullable=False)
    laundry_address = Column(String(255), nullable=False)
    laundry_opening_date = Column(Date, nullable=False)
    laundry_open_time = Column(Time, nullable=False)
    laundry_close_time = Column(Time, nullable=False)
    laundry_image_name = Column(String(255), nullable=True)

    laundry_comments = relationship("CommentModel",
                                    cascade="all, delete-orphan",
                                    lazy="dynamic",
                                    back_populates="comment_laundry")
    laundry_machine_types = relationship("LaundryToMachineTypeModel",
                                         back_populates="laundry_to_machine_type_laundry")
