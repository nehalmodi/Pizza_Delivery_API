from fastapi import APIRouter
from pydantic import BaseModel

auth_router = APIRouter(
    prefix='/auth',
    tags = ['auth_tag']
)

class Mul2(BaseModel):
    n: int = 0

@auth_router.get("/")
async def hello():
    return {"Message" : "Hello World of auth"}

