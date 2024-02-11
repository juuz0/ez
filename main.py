from db import models, db
from fastapi import FastAPI, UploadFile, HTTPException
import uvicorn

app = FastAPI()

@app.post("/uploadfile/", status_code=201)
async def create_upload_file(file: UploadFile):
    mime_types = ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                  "application/vnd.openxmlformats-officedocument.presentationml.presentation"]
    if (file.content_type not in mime_types):
        raise HTTPException(400, detail="file type is not allowed")
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


if __name__ == "__main__":
    port = int(8000)
    app_module = "main:app"
    uvicorn.run(app_module, host="0.0.0.0", port=port, reload=True)