from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from .base import Base


class Talent(Base):
    __tablename__ = "talent"
    talent_id = Column(String, primary_key=True)
    talent_name = Column(String)
    talent_grade = Column(String)
    booking_grade = Column(String)
    operating_unit = Column(String)
    office_city = Column(String)
    office_postal_code = Column(String)
    job_manager_id = Column(String)
    job_manager_name = Column(String)

class TalentOut(BaseModel):
    talent_id: str
    talent_name : str
    talent_grade : str
    booking_grade : str
    operating_unit : str
    office_city : str
    office_postal_code : str
    job_manager_id : str
    job_manager_name : str

    class Config:
        orm_mode = True