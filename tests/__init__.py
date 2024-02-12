from db.db import Base, engine
import db.models
import os

try:
    os.remove('sql_app.db')
except Exception:
    print("No previous database file found.\n")
print("Creating database ....")

Base.metadata.create_all(engine);