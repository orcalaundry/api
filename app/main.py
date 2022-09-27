from fastapi import FastAPI

from app import routers

app = FastAPI()

app.include_router(routers.machine)
app.include_router(routers.esp)
app.include_router(routers.raspi)
