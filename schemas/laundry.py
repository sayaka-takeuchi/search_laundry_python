from datetime import date, time, datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from models.machine_type import MachineType


class LaundryMachineTypeSchema(BaseModel):
    """
    LaundryToMachineTypeModelに入るデータ
    """
    laundry_to_machine_type_machine_type_id: MachineType = Field(
        alias="machine_type")
    laundry_to_machine_type_machine_count: int = Field(alias="machine_count")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class LaundryCreateSchema(BaseModel):
    laundry_name: str = Field(..., example="コインランドリー１号店")
    laundry_address: str = Field(..., example="愛知県豊橋市1-1")
    laundry_opening_date: date = Field(..., example=date.today())
    laundry_open_time: time = Field(..., example="00:00:00")
    laundry_close_time: time = Field(..., example="00:00:00")
    laundry_machine_types: List[LaundryMachineTypeSchema] = Field(
        ..., description="ランドリーの機械の情報、機械の種類と台数が入っている")

    class Config:
        orm_mode = True


class LaundryCreateResponseSchema(LaundryCreateSchema):
    laundry_id: int


class LaundryUpdateSchema(LaundryCreateSchema):
    pass


class LaundryUpdateResponseSchema(LaundryCreateResponseSchema):
    pass


class LaundrySchema(LaundryUpdateResponseSchema):
    laundry_image_name: Optional[str]
    is_deleted: bool
    deleted_at: Optional[datetime]
