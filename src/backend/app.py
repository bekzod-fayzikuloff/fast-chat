from fastapi import FastAPI

from .api import router
from .database import engine
from .tables import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router=router)
