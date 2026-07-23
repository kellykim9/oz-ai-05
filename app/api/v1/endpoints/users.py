from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.db.databases import get_db  # 비동기 세션을 반환하는 함수라 가정
from app.schemas.user import UserCreate, UserLogin, UserUpdate, UserResponse
from app.crud import user as crud_user
from app.core.security import verify_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """회원가입 엔드포인트"""
    existing_user = await crud_user.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )
    return await crud_user.create_user(db=db, user_in=user_in)

@router.post("/login")
async def login(user_in: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    """로그인 엔드포인트"""
    user = await crud_user.get_user_by_email(db, email=user_in.email)
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )
    return {"message": "로그인 성공", "user_id": user.id, "email": user.email}

@router.get("/me", response_model=UserResponse)
async def get_my_info(user_id: int, db: AsyncSession = Depends(get_db)):
    """내 정보 조회 엔드포인트"""
    user = await crud_user.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    return user

@router.patch("/me", response_model=UserResponse)
async def update_my_info(user_id: int, user_in: UserUpdate, db: AsyncSession = Depends(get_db)):
    """내 정보 수정 엔드포인트"""
    user = await crud_user.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    return await crud_user.update_user(db=db, db_user=user, user_in=user_in)

@router.delete("/me")
async def delete_my_info(user_id: int, db: AsyncSession = Depends(get_db)):
    """회원 탈퇴 엔드포인트"""
    user = await crud_user.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    await crud_user.delete_user(db=db, db_user=user)
    return {"message": "회원 탈퇴가 완료되었습니다."}