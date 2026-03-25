from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.utils.auth import decode_token

security = HTTPBearer(auto_error=False)  # ✅ safer


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        # ✅ Check header exists
        if not credentials or not credentials.credentials:
            raise HTTPException(status_code=401, detail="Authorization token missing")

        token = credentials.credentials.strip()

        # ✅ Basic token validation
        if not token:
            raise HTTPException(status_code=401, detail="Invalid token")

        # 🔥 Decode token
        payload = decode_token(token)

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        return payload  # ✅ unchanged

    except HTTPException:
        raise

    except Exception as e:
        print(f"[AUTH DEP ERROR]: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")
