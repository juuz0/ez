from db import models, db
from fastapi import FastAPI, UploadFile, HTTPException
import uvicorn
from routes import file_manage, user_manage

app = FastAPI()
app.include_router(file_manage.router)
app.include_router(user_manage.router)

if __name__ == "__main__":
    port = int(8000)
    app_module = "main:app"
    uvicorn.run(app_module, host="0.0.0.0", port=port, reload=True)