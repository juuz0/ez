from sqlalchemy import Column, Integer, String, LargeBinary
from db.db import Base


class FileModal(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    contents = Column(LargeBinary)

class UserModal(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)