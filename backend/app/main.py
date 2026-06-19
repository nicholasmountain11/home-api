from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from backend.app.services import SensorService, ActuatorService

sensor_service: SensorService
actuator_service: ActuatorService


@asynccontextmanager
async def lifespan(app: FastAPI):
    global sensor_service
    global actuator_service
    sensor_service = SensorService(port=8001)
    actuator_service = ActuatorService(port=8002)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World!!!!"}


@app.get("/service_test")
def test_service(service: SensorService = Depends()):
    message = service.message()
    return {"Message": f"{message}"}


@app.post("/listen_for_sensors")
def listen_for_sensors(service: SensorService = Depends()):
    message = service.receive()
    return {"Message": message}
