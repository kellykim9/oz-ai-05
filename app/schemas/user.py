from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# 회원가입 요청 스키마
class UserCreate(BaseModel):
    username: str  
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str
    department: Optional[str] = None
    gender: Optional[str] = None # 'M' or 'F'
    phone_number: Optional[str] = None

# 로그인 요청 스키마
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 회원 정보 수정 스키마 (PATCH용 - 모두 선택적 값)
class UserUpdate(BaseModel):
    department: Optional[str] = None
    phone_number: Optional[str] = None

# 사용자 응답 스키마
class UserResponse(BaseModel):
    id: int
    username: str  
    email: EmailStr
    name: str
    department: Optional[str] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True