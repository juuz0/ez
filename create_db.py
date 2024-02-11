from db.db import Base, engine
import db.models

print("Creating database ....")

Base.metadata.create_all(engine);