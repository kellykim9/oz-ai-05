from sqlalchemy import Column, Integer, String
from app.core.db.databases import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(50), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    phone_number = Column(String(50), nullable=True)
    department = Column(String(50), nullable=True)
    gender = Column(String(20), nullable=True)  
    is_active = Column(Integer, default=1)