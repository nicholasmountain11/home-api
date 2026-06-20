from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from services.connection import ConnectionService

sensor_service: ConnectionService


@asynccontextmanager
async def lifespan(app: FastAPI):
    global connection_service
    connection_service = ConnectionService(sensor_port=8001, actuator_port=8002)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World!!!!"}


@app.get("/get_sensor_message/{nickname}")
def get_sensor_message(nickname: str):
    message = connection_service.get_message(nickname=nickname)
    return {"Message": message}


@app.get("/list_sensors", response_model=list[str])
def list_sensors() -> list[str]:
    sensors = connection_service.registry.keys()
    return sensors


@app.post("/send_message/{nickname}")
def send_actuator_message(nickname: str, message: str):
    connection_service.send_message(nickname=nickname, message=message)
