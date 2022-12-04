from sqlalchemy import Column, Integer, String
from .base import Base


class Client(Base):
    __tablename__ = "client"
    id = Column(String, primary_key=True)
    name = Column(String)
    industry = Column(String)