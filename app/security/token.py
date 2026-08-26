from jose import JWTError, jwt
from datetime import datetime,timezone,timedelta

SECRET_KEY = "library-secret-key-change-me"     
ALGORITHM = "HS256"                    
ACCESS_TOKEN_EXPIRE_MINUTES = 30       

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])