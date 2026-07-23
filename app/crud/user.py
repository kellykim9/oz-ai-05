from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str):
    """이메일로 사용자를 조회합니다."""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: int):
    """ID로 사용자를 조회합니다."""
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate):
    """새로운 사용자를 생성합니다 (비밀번호 Argon2 해싱 적용)."""
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,  # <-- 이 부분을 추가해 주세요!
        email=user_in.email,
        hashed_password=hashed_password,
        name=user_in.name,
        department=user_in.department,
        gender=user_in.gender,
        phone_number=user_in.phone_number
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, db_user: User, user_in: UserUpdate):
    """사용자 정보를 수정합니다 (전달된 필드만 반영)."""
    update_data = user_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, db_user: User):
    """사용자를 삭제(탈퇴)합니다."""
    await db.delete(db_user)
    await db.commit()
    return db_user