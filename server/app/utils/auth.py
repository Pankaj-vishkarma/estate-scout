from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "super_secret_key_change_this"  # ⚠️ change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7


# 🔐 HASH PASSWORD
def hash_password(password: str):
    try:
        # 🔥 FIX: bcrypt max length = 72 bytes
        password = password.encode("utf-8")[:72].decode("utf-8")
        return pwd_context.hash(password)
    except Exception as e:
        print(f"[HASH ERROR]: {e}")
        raise Exception("Password hashing failed")


# 🔐 VERIFY PASSWORD
def verify_password(plain_password: str, hashed_password: str):
    try:
        # 🔥 FIX: same truncation logic
        plain_password = plain_password.encode("utf-8")[:72].decode("utf-8")
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"[VERIFY ERROR]: {e}")
        return False


# 🔐 CREATE TOKEN
def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

        to_encode.update(
            {
                "exp": expire,
                "iat": datetime.utcnow(),  # 🔥 issued at
            }
        )

        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return token
    except Exception as e:
        print(f"[TOKEN CREATE ERROR]: {e}")
        return None


# 🔐 DECODE TOKEN
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        print(f"[TOKEN DECODE ERROR]: {e}")
        return None
