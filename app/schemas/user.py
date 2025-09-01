
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date  

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    position: Optional[str] = None
    department: Optional[str] = None
    photoUrl: Optional[str] = None
    hire_date: Optional[date] = None
    skills: Optional[str] = None  
    current_project: Optional[str] = None
    languages_spoken: Optional[str] = None  


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    position: Optional[str] = None
    department: Optional[str] = None
    photoUrl: Optional[str] = None
    hire_date: Optional[date] = None
    skills: Optional[str] = None
    current_project: Optional[str] = None
    languages_spoken: Optional[str] = None


    model_config = ConfigDict(from_attributes=True)



