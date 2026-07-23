from passlib.context import CryptContext

# Argon2 알고리즘을 사용하기 위한 패스워드 컨텍스트 설정
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """평문 비밀번호와 해시된 비밀번호가 일치하는지 확인합니다."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """평문 비밀번호를 Argon2 알고리즘으로 해싱합니다."""
    return pwd_context.hash(password)