from sqlalchemy import Column, Integer, String
from database import Base

class UserValue(Base):
    __tablename__ = "user_values"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    value = Column(String, nullable=False)
