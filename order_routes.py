from fastapi import APIRouter,Depends,status
from fastapi_jwt_auth import AuthJWT
from models import Order,User
from schema import OrderModel,OrderStatusModel
from fastapi.exceptions import HTTPException
from database import Session,engine
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
 
order_router = APIRouter(
    prefix= '/orders',
    tags=['order_tag']
)

session = Session(bind=engine)

@order_router.get("/")
async def hello(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
        

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
            )

    return {"Message" : "Hello World"}

@order_router.post("/order",status_code=status.HTTP_201_CREATED)
async def place_an_order(order:OrderModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
        

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
            )
    
    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username==current_user).first()

    new_order = Order(
        pizza_size = order.pizza_size,
        quantity = order.quantity
    )

    new_order.user = user

    session.add(new_order)

    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status 
    }

    return jsonable_encoder(response)


@order_router.get('/orders')
async def list_all_orders(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token"
            )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username==current_user).first()

    if user.is_staff:
        order = session.query(Order).all()

        return jsonable_encoder(order)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sorry!You are not a superuser"
    )

@order_router.get('/orders/{id}')
async def get_order_by_id(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
            )
    
    user= Authorize.get_jwt_subject()

    current_user = session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        order = session.query(Order).filter(Order.id==id).first()

        return jsonable_encoder(order)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sorry!You are not a superuser"
        )


@order_router.get('/user/orders')
async def get_user_orders(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
            )
    
    user = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(User.username==user).first()


    return jsonable_encoder(current_user.orders)


@order_router.get('/user/orders/{id}')
async def get_user_specific_orders(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
            )
    
    subject = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(User.username==subject).first()

    orders = current_user.orders 
    for o in orders:
        if o.id==id:
            return jsonable_encoder(o)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No order with such id"
        )

@order_router.put('/order/update/{id}/')
async def update_order(id:int,order:OrderModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    order_to_update = session.query(Order).filter(Order.id==id).first()

    order_to_update.quantity = order.quantity
    order_to_update.pizza_size = order.pizza_size

    response ={
            "id": order_to_update.id,
            "quantity": order_to_update.quantity,
            "pizza-size": order_to_update.pizza_size,
            "order-status": order_to_update.order_status
        }

    session.commit()

    return jsonable_encoder(response)


@order_router.patch('/order/update/{id}/')
async def update_order_status(id:int,order:OrderStatusModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    username1 = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(User.username==username1).first()

    if current_user.is_staff:
        order_to_update = session.query(Order).filter(Order.id==id).first()

        order_to_update.order_status=order.order_status

        response ={
            "id": order_to_update.id,
            "quantity": order_to_update.quantity,
            "pizza-size": order_to_update.pizza_size,
            "order-status": order_to_update.order_status
        }

        session.commit()

        return jsonable_encoder(response)


@order_router.delete('/order/delete/{id}/',status_code=status.HTTP_204_NO_CONTENT)
async def order_to_delete(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )


    order_delete = session.query(Order).filter(Order.id==id).first()

    session.delete(order_delete)

    session.commit()

    return order_delete
    