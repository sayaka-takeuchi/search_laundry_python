from datetime import datetime
from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from helpers import gcp_helper
from helpers.exceptions import raise_not_found
from helpers.file_helper import save_upload_file
from models.laundry import LaundryModel
from models.laundry_to_machine_type_model import LaundryToMachineTypeModel
from schemas.laundry import LaundryCreateSchema, LaundryMachineTypeSchema, LaundryUpdateSchema

LAUNDRY_IMAGE_DIR_PATH = 'static/uploads/laundry/'


@raise_not_found
def get_laundry(laundry_id: int, db: Session):
    return db.query(LaundryModel).get(laundry_id)


def get_laundries(db: Session, offset: int = 0, limit: int = 100) -> List[LaundryModel]:
    return db.query(LaundryModel).filter(
        LaundryModel.is_deleted.is_(False)
    ).offset(offset).limit(limit).all()


def register_laundry_without_image(db: Session, new_laundry: LaundryCreateSchema) -> LaundryModel:
    dect_new_laundry = new_laundry.dict()
    del dect_new_laundry["laundry_machine_types"]
    db_laundry = LaundryModel(**dect_new_laundry)
    db.add(db_laundry)
    db.flush()
    for machine_info in new_laundry.laundry_machine_types:
        register_laundry_machine_type(laundry_id=db_laundry.laundry_id,
                                      db=db,
                                      machine_info=machine_info, commit=False)
    db.commit()
    return db_laundry


def register_laundry_machine_type(laundry_id: int, db: Session, machine_info: LaundryMachineTypeSchema, commit=True):
    db_laundry_to_machine = LaundryToMachineTypeModel(
        laundry_to_machine_type_laundry_id=laundry_id,
        laundry_to_machine_type_machine_type_id=machine_info.laundry_to_machine_type_machine_type_id,
        laundry_to_machine_type_machine_count=machine_info.laundry_to_machine_type_machine_count
    )
    db.add(db_laundry_to_machine)
    if commit:
        db.commit()


def update_laundry_without_image(db: Session, laundry_id: int,
                                 new_laundry: LaundryUpdateSchema) -> LaundryModel:
    db_laundry: LaundryModel = get_laundry(db=db, laundry_id=laundry_id)
    new_laundry_dict = new_laundry.dict()
    del new_laundry_dict["laundry_machine_types"]
    db_laundry = LaundryModel(**new_laundry_dict)
    db_laundry.laundry_id = laundry_id
    db.commit()
    return db_laundry


def delete_laundry(db: Session, laundry_id: int):
    laundry: LaundryModel = get_laundry(db=db, laundry_id=laundry_id)
    laundry.is_deleted = True
    laundry.deleted_at = datetime.utcnow()
    db.commit()


async def register_laundry_image(laundry_id: int, db: Session, file: UploadFile):
    db_laundry: LaundryModel = get_laundry(db=db, laundry_id=laundry_id)
    if len(file.filename.split(".")) > 1:
        file_name = datetime.utcnow().strftime("%Y%m%d%H%M%SZ-") + file.filename
    else:
        file_type = file.content_type.split("/")[1]
        file_name = datetime.utcnow().strftime("%Y%m%d%H%M%SZ-") + \
            file.filename + "." + file_type

    file_path = LAUNDRY_IMAGE_DIR_PATH + file_name
    await save_upload_file(upload_file=file,
                           dir_path=LAUNDRY_IMAGE_DIR_PATH, file_path=file_path)
    gcp_helper.upload_blob(storage_object_name=file_name, source_file_name=file_path,
                           bucket_name=gcp_helper.BucketName.laundry_images)
    # 画像更新時は元の画像を削除してからdbのlaundry_image_nameを更新する
    if db_laundry.laundry_image_name is not None:
        gcp_helper.delete_blob(bucket_name=gcp_helper.BucketName.laundry_images,
                               blob_name=db_laundry.laundry_image_name)
    db_laundry.laundry_image_name = file_name
    db.commit()
    return db_laundry
