from datetime import date, time, datetime
from typing import Optional
from pydantic import BaseModel, Field


class LaundryCreateSchema(BaseModel):
    laundry_name: str = Field(..., example="コインランドリー１号店")
    laundry_address: str = Field(..., example="愛知県豊橋市1-1")
    laundry_opening_date: date = Field(..., example=date.today())
    laundry_open_time: time = Field(..., example="00:00:00")
    laundry_close_time: time = Field(..., example="00:00:00")


class LaundryCreateResponseSchema(LaundryCreateSchema):
    laundry_id: int

    class Config:
        orm_mode = True


class LaundryUpdateSchema(LaundryCreateSchema):
    pass


class LaundryUpdateResponseSchema(LaundryCreateResponseSchema):
    pass


class LaundrySchema(LaundryCreateResponseSchema):
    laundry_image_name: Optional[str]
    is_deleted: bool
    deleted_at: Optional[datetime]
