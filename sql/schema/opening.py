import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey,DateTime, Float
from .base import Base


class Opening(Base):
    __tablename__ = "opening"
    id = Column(String, primary_key=True)
    client_id = Column(String, ForeignKey("client.id"))
    required_skills = Column(String)
    optional_skills = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    total_hours = Column(Float)
    talent_id = Column(String, ForeignKey("talent.talent_id"))
    original_id = Column(String)


class OpeningOut(BaseModel):
    id: str
    client_id : str
    required_skills : str
    optional_skills : str
    start_date : datetime.datetime
    end_date : datetime.datetime
    total_hours : float
    talent_id : str
    original_id : str

    class Config:
        orm_mode = True