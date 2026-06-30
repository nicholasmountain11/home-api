from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status

from services.connection_service import ConnectionService

import os
from dotenv import load_dotenv

load_dotenv()

sensor_service: ConnectionService

SENSOR_PORT = int(os.environ["SENSOR_PORT"])
ACTUATOR_PORT = int(os.environ["ACTUATOR_PORT"])
HOST_IP = os.environ["LOCAL_HOST"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    global connection_service
    connection_service = ConnectionService(
        sensor_port=SENSOR_PORT, actuator_port=ACTUATOR_PORT, host_ip=HOST_IP
    )
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World!!!!"}


@app.get("/get_sensor_message/{nickname}")
def get_sensor_message(nickname: str):
    try:
        message = connection_service.get_message(nickname=nickname)
        return {"message": message}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Sensor '{nickname}' not found")
    except TimeoutError as e:
        raise HTTPException(status_code=408, detail=str(e))


@app.get("/list_sensors", response_model=list[str])
def list_sensors() -> list[str]:
    try:
        return connection_service.get_sensor_nickname_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/send_message/{nickname}")
def send_actuator_message(nickname: str, message: str):
    try:
        connection_service.send_message(nickname=nickname, message=message)
        return {"status": "sent"}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Actuator '{nickname}' not found")
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/list_actuators", response_model=list[str])
def list_actuators() -> list[str]:
    try:
        return connection_service.get_actuator_nickname_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
