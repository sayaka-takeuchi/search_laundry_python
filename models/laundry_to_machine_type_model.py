from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

from database import Base

from models.machine_type import MachineType


class LaundryToMachineTypeModel(Base):
    """
    LaundryクラスとMachineTypeクラスの中間テーブル
    コインランドリーに設置されている機械と設置台数を記録する
    """

    __tablename__ = 'laundry_to_machine_type'
    laundry_to_machine_type_laundry_id = Column(Integer,
                                                ForeignKey(
                                                    'laundry.laundry_id', ondelete='CASCADE'),
                                                primary_key=True, nullable=False)
    laundry_to_machine_type_machine_type_id = Column(Enum(MachineType),
                                                     primary_key=True, nullable=False)
    laundry_to_machine_type_machine_count = Column(
        Integer, nullable=False, default=1)
    laundry_to_machine_type_laundry = relationship(
        'LaundryModel', back_populates='laundry_machine_types')
