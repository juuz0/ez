from db import models, db
from fastapi import FastAPI, UploadFile, HTTPException, APIRouter, Depends
from .user_manage import get_current_user
from typing import Annotated
from schema.schema import User, Role

router = APIRouter()

@router.post("/uploadfile/", status_code=201)
async def create_upload_file(file: UploadFile, current_user: Annotated[User, Depends(get_current_user)]):
    mime_types = ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                  "application/vnd.openxmlformats-officedocument.presentationml.presentation"]
    if (current_user.role == Role.OPS.name):
        raise HTTPException(401, detail="only OPS user can upload files")
    if (file.content_type not in mime_types):
        raise HTTPException(401, detail="file type is not allowed")
    is_file_added = await add_file_to_db(file)
    if (is_file_added):
        return {"message": "file added successfully"}
    raise HTTPException(500, detail="failed to add file into DB")

async def add_file_to_db(file: UploadFile) -> bool:
    session = db.SessionLocal()
    try:
        file_contents = await file.read()
        file_name = file.filename
        db_file = models.FileModal(filename = file_name, contents = file_contents)
        session.add(db_file)
        session.commit()
        session.refresh(db_file)
        return True
    finally:
        session.close()
