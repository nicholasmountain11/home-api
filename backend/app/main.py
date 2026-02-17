from fastapi import Depends, FastAPI

from app.services.connection import ConnectionService

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World!!!!"}


@app.get("/service_test")
def test_service(service: ConnectionService = Depends()):
    message = service.message()
    return {"Message": f"{message}"}
