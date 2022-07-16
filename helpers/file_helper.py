import os
import shutil
from fastapi import UploadFile


async def save_upload_file(upload_file: UploadFile, dir_path: str, file_path: str):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)
