from sqlalchemy import Column, Integer, String
from database import Base

class Registration(Base):
    __tablename__ = "registration"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)