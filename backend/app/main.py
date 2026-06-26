from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status

from services.connection_service import ConnectionService

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
    try:
        message = connection_service.get_message(nickname=nickname)
        return {"Message": message}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Missing key: {e}")


@app.get("/list_sensors", response_model=list[str])
def list_sensors() -> list[str]:
    return connection_service.get_sensor_nickname_list()


@app.post("/send_message/{nickname}")
def send_actuator_message(nickname: str, message: str):
    try:
        connection_service.send_message(nickname=nickname, message=message)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Message could not be sent")


@app.get("/list_actuators", response_model=list[str])
def list_actuators() -> list[str]:
    return connection_service.get_actuator_nickname_list()
