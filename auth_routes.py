from fastapi import APIRouter, status
from pydantic import BaseModel
from database import engine, Session
from schema import SignUpModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

auth_router = APIRouter(
    prefix='/auth',
    tags = ['auth_tag']
)

session = Session(bind=engine)

class Mul2(BaseModel):
    n: int = 0

@auth_router.get("/")
async def hello():
    return {"Message" : "Hello World of auth"}

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email==user.email).first()

    if db_email is not None :
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="User with the email already exist"
        )
    
    db_username = session.query(User).filter(User.username==user.username).first()

    if db_username is not None :
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="User with the username already exist"
        )

    new_user = User(
        username = user.username,
        email = user.email,
        password = generate_password_hash(user.password),
        is_active = user.is_active,
        is_staff = user.is_staff
    )

    session.add(new_user)

    session.commit()

    return new_user



