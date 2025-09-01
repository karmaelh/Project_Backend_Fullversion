from sqlalchemy import Column, String, Integer, Date, Text
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    position = Column(String, nullable=True)
    department = Column(String, nullable=True)
    photoUrl = Column(String, nullable=True)
    hire_date = Column(Date)
    skills = Column(Text, nullable=True)
    current_project = Column(Text, nullable=True)
    languages_spoken = Column(Text, nullable=True)




