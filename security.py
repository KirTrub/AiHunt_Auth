import os
import jwt
import uuid
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

SECRET = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ph = PasswordHasher()

def create_access_token(user_id: int, email: str) -> str:
    now = datetime.now(timezone.utc)
    access_jti = str(uuid.uuid4())
    
    access_payload = {
        "sub": str(user_id),
        "jti": access_jti,
        "iat": now,
        "exp": now + timedelta(minutes=15),
        "email": email,
        "type": "access"
    }
    access_token = jwt.encode(access_payload, SECRET, algorithm=ALGORITHM)
    return access_token

def create_refresh_token(user_id: int) -> str:
    refresh_payload = {
        "sub": str(user_id),
        "iat": datetime.now,
        "exp": datetime.now + timedelta(days=7),
        "type": "refresh"
    }

    refresh_token = jwt.encode(refresh_payload, SECRET, algorithm=ALGORITHM)
    
    return refresh_token

def hash_password(password: str) -> str:
    return ph.hash(password)

def check_password(plain: str, hashed: str) -> bool:
    try:
        return ph.verify(hashed, plain)
    except VerifyMismatchError:
        return False