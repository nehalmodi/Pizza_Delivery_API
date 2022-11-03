from fastapi import APIRouter

order_router = APIRouter(
    prefix= '/order',
    tags=['order_tag']
)

@order_router.get("/")
async def hello():
    return {"Message" : "Hello World"}
