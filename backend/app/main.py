from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from services.connection import ConnectionService
from services.actuator import ActuatorService

sensor_service: ConnectionService
actuator_service: ActuatorService


@asynccontextmanager
async def lifespan(app: FastAPI):
    global sensor_service
    global actuator_service
    sensor_service = ConnectionService(sensor_port=8001, actuator_port=8002)
    actuator_service = ActuatorService(port=8002)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World!!!!"}


@app.get("/get_sensor_message/{nickname}")
def get_sensor_message(nickname: str):
    message = sensor_service.get_message(nickname=nickname)
    return {"Message": message}


@app.get("/list_sensors", response_model=list[str])
def list_sensors() -> list[str]:
    sensors = sensor_service.registry.keys()
    return sensors
