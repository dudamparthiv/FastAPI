from passlib.context import CryptContext
from fastapi import status,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
import jwt,secrets
from app import model
from jwt.exceptions import InvalidTokenError
from datetime import datetime,timedelta,timezone

pass_cxt = CryptContext(schemes=["bcrypt"],deprecated="auto")


get_db = model.get_db

def hashed(password):
    return pass_cxt.hash(password)

def verify(plan_password,hashed_password):
    return pass_cxt.verify(plan_password,hashed_password)

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login_user/")

def create_access_token(data:dict,expires_delta:timedelta | None =None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt =jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user_for_token(db,email:str):
    user = db.query(model.User).filter(model.User.email == email).first()
    if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    return user

def verify_token(token:str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=403, detail="Token is invalid or expired")
        return payload
    except InvalidTokenError:
        raise credentials_exception
     


def get_current_user(token:str = Depends(oauth2_scheme),db:model.Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = model.TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_current_user_for_token(db,email=token_data.email)
    if user is None:
            raise credentials_exception
    return user