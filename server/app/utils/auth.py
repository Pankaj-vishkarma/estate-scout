from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ ENV CONFIG (CRITICAL FIX)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 7))

# ❗ Crash early if missing
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set in environment variables")


# 🔐 HASH PASSWORD
def hash_password(password: str):
    try:
        password = password.encode("utf-8")[:72].decode("utf-8")
        return pwd_context.hash(password)
    except Exception as e:
        print(f"[HASH ERROR]: {e}")
        raise Exception("Password hashing failed")


# 🔐 VERIFY PASSWORD
def verify_password(plain_password: str, hashed_password: str):
    try:
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
                "iat": datetime.utcnow(),
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

    except Exception as e:
        print(f"[TOKEN UNKNOWN ERROR]: {e}")
        return None
