from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.laundry import LaundryCreateResponseSchema, LaundryCreateSchema, LaundrySchema, LaundryUpdateResponseSchema, LaundryUpdateSchema
from schemas.result import Result
from services import laundry

router = APIRouter()


@router.get("/", tags=["laundry"], response_model=List[LaundrySchema])
def get_laundries(db: Session = Depends(get_db), offset: int = 0, limit: int = 100):
    laundries = laundry.get_laundries(db=db, offset=offset, limit=limit)
    return [LaundrySchema.from_orm(laundry) for laundry in laundries]


@router.post("/", tags=["laundry"], response_model=LaundryCreateResponseSchema)
def register_laundry_without_image(new_laundry: LaundryCreateSchema,
                                   db: Session = Depends(get_db)):
    registerd_laundry = laundry.register_laundry_without_image(
        db=db, new_laundry=new_laundry)
    return LaundryCreateResponseSchema.from_orm(registerd_laundry)


@router.post("/{laundry_id}/image", tags=["laundry"], response_model=Result)
async def register_laundry_image(laundry_id: int,
                                 laundry_image: UploadFile = File(...),
                                 db: Session = Depends(get_db)):
    await laundry.register_laundry_image(
        laundry_id=laundry_id, db=db, file=laundry_image)
    return Result(result=True)


@router.put("/{laundry_id}", tags=["laundry"], response_model=LaundryUpdateResponseSchema)
def update_laundry_without_image(laundry_id: int,
                                 new_laundry: LaundryUpdateSchema,
                                 db: Session = Depends(get_db)):
    updated_laundry = laundry.update_laundry_without_image(laundry_id=laundry_id,
                                                           new_laundry=new_laundry, db=db)

    return LaundryUpdateResponseSchema.from_orm(updated_laundry)


@router.delete("/{laundry_id}", tags=["laundry"], response_model=Result)
def delete_laundry(laundry_id: int, db: Session = Depends(get_db)):
    """
    フラグを用いて論理削除
    """
    laundry.delete_laundry(laundry_id=laundry_id, db=db)
    return Result(result=True)
