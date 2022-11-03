from database import engine
from models import Order, User, Base

Base.metadata.create_all(bind=engine)

