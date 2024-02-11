from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    mime_types = ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                  "application/vnd.openxmlformats-officedocument.presentationml.presentation"]
    if (file.content_type in mime_types):
        addFileToDb(file)
        return {"response": "success"}
    return {"response": "failure"}

def addFileToDb(file: UploadFile):
    return None