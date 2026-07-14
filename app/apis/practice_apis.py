import re
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, EmailStr, field_validator

router = APIRouter(prefix="/practice_api")

# 회원 목록 (기본 데이터)
user_list = [
    {
        "id": 1,
        "name": "홍길동",
        "age": 24,
        "email": "gildong24@example.com",
        "password": "Password1234!!"
    },
    {
        "id": 2,
        "name": "장문복",
        "age": 21,
        "email": "moonluck12@example.com",
        "password": "Check1321!"
    },
    {
        "id": 3,
        "name": "임우진",
        "age": 31,
        "email": "limousine33@example.com",
        "password": "lwsPAssword12@"
    }
]

# --- 규칙(Pydantic) 정의 ---

def validate_password_str(v: str) -> str:
    if not (8 <= len(v) <= 20):
        raise ValueError("비밀번호는 8자~20자 사이여야 합니다.")
    if not re.search(r"[A-Z]", v):
        raise ValueError("대문자가 최소 1개 이상 필요합니다.")
    if not re.search(r"[a-z]", v):
        raise ValueError("소문자가 최소 1개 이상 필요합니다.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
        raise ValueError("특수문자가 최소 1개 이상 필요합니다.")
    return v

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=10)
    age: int = Field(..., ge=14)
    email: EmailStr = Field(..., max_length=30)
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password_str(v)

class UserUpdate(BaseModel):
    age: Optional[int] = Field(None, ge=14)
    email: Optional[EmailStr] = Field(None, max_length=30)
    password: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validate_password_str(v)
        return v

# --- API 기능들 ---

# 1. 모든 회원 정보 목록 조회
@router.get("/users")
def get_all_users():
    return [
        {"id": u["id"], "name": u["name"], "age": u["age"], "email": u["email"]}
        for u in user_list
    ]

# 2. 특정 회원 정보 조회
@router.get("/users/{user_id}")
def get_user(user_id: int):
    for user in user_list:
        if user["id"] == user_id:
            return {"id": user["id"], "name": user["name"], "age": user["age"], "email": user["email"]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="유효한 id가 아닙니다.")

# 3. 회원 정보 추가
@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    for user in user_list:
        if user["email"] == user_data.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 이메일입니다.")
    
    next_id = max([u["id"] for u in user_list]) + 1 if user_list else 1
    new_user = {
        "id": next_id, "name": user_data.name, "age": user_data.age,
        "email": user_data.email, "password": user_data.password
    }
    user_list.append(new_user)
    return {"id": new_user["id"], "name": new_user["name"], "age": new_user["age"], "email": new_user["email"]}

# 4. 회원 정보 수정
@router.put("/users/{user_id}")
def update_user(user_id: int, user_data: UserUpdate):
    if user_data.age is None and user_data.email is None and user_data.password is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="수정할 항목이 입력되지 않았습니다.")
        
    target_user = None
    for user in user_list:
        if user["id"] == user_id:
            target_user = user
            break
            
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="유효한 id가 아닙니다.")
        
    if user_data.age is not None:
        target_user["age"] = user_data.age
    if user_data.email is not None:
        for user in user_list:
            if user["id"] != user_id and user["email"] == user_data.email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 사용 중인 이메일입니다.")
        target_user["email"] = user_data.email
    if user_data.password is not None:
        target_user["password"] = user_data.password
        
    return {"age": target_user["age"], "email": target_user["email"]}

# 5. 회원 정보 삭제
@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    for idx, user in enumerate(user_list):
        if user["id"] == user_id:
            user_list.pop(idx)
            return {"detail": "성공적으로 삭제되었습니다."}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="유효한 id가 아닙니다.")