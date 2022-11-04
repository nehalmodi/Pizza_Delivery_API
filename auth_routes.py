from fastapi import APIRouter
from pydantic import BaseModel
from database import engine, Session
from schema import SignUpModel
from models import User

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

@auth_router.post("/signup")
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email==user.email).first()



