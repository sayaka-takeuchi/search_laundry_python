from datetime import datetime
from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from helpers import gcp_helper
from helpers.exceptions import raise_not_found
from helpers.file_helper import save_upload_file
from models.laundry import LaundryModel
from schemas.laundry import LaundryCreateSchema, LaundryUpdateSchema

LAUNDRY_IMAGE_DIR_PATH = 'static/uploads/laundry/'


@raise_not_found
def get_laundry(laundry_id: int, db: Session):
    return db.query(LaundryModel).get(laundry_id)


def get_laundries(db: Session, offset: int = 0, limit: int = 100) -> List[LaundryModel]:
    return db.query(LaundryModel).filter(
        LaundryModel.is_deleted.is_(False)
    ).offset(offset).limit(limit).all()


def register_laundry_without_image(db: Session, new_laundry: LaundryCreateSchema) -> LaundryModel:
    db_laundry = LaundryModel(**new_laundry.dict())
    db.add(db_laundry)
    db.commit()
    db.refresh(db_laundry)
    return db_laundry


def update_laundry_without_image(db: Session, laundry_id: int,
                                 new_laundry: LaundryUpdateSchema) -> LaundryModel:
    db_laundry: LaundryModel = get_laundry(db=db, laundry_id=laundry_id)
    db_laundry = LaundryModel(**new_laundry.dict())
    db_laundry.laundry_id = laundry_id
    db.commit()
    print("db_laundry", db_laundry)
    print("aiuaiuhfgarey89t3oijagrji")
    return db_laundry


def delete_laundry(db: Session, laundry_id: int):
    laundry: LaundryModel = get_laundry(db=db, laundry_id=laundry_id)
    laundry.is_deleted = True
    laundry.deleted_at = datetime.utcnow()
    db.commit()


async def register_laundry_image(laundry_id: int, db: Session, file: UploadFile):
    db_laundry: LaundryModel = get_laundry(db=db, laundry_id=laundry_id)
    # 画像更新時は元の画像を削除してから更新する
    if db_laundry.laundry_image_name is not None:
        gcp_helper.delete_blob(bucket_name=gcp_helper.BucketName.laundry_images,
                               blob_name=db_laundry.laundry_image_name)
    filename_without_extension = file.filename
    file_type = file.content_type.split("/")[1]
    file_name = datetime.utcnow().strftime("%Y%m%d%H%M%SZ-") + \
        filename_without_extension + file_type
    file_path = LAUNDRY_IMAGE_DIR_PATH + filename_without_extension
    await save_upload_file(upload_file=file,
                           dir_path=LAUNDRY_IMAGE_DIR_PATH, file_path=file_path)
    gcp_helper.upload_blob(storage_object_name=file_name, source_file_name=file_path,
                           bucket_name=gcp_helper.BucketName.laundry_images)
    db_laundry.laundry_image_name = file_name
    db.commit()
    return db_laundry
