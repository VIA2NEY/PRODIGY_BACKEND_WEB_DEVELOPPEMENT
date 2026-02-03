import uuid
from sqlalchemy import Column, Integer, String, CHAR
from app.database.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=True, default=0)
    
    password_hash = Column(String(255), nullable=False)

    role = Column(String(50), nullable=False, default="user")
    # roles possibles : user | admin | owner