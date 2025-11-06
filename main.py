from fastapi import  FastAPI,APIRouter
from routes.api.car_routes import router as car_router
from routes.api.motor_routes import router as motor_router
from routes.api.trasmission_routes import router as trasmission_router
from routes.api.user_routes import router as user_router

app = FastAPI(title="GearBox")
 
api_router = APIRouter()

api_router.include_router(car_router, prefix="/Cars", tags=["CARS"])
api_router.include_router(motor_router,prefix="/Motor",tags=["Motors"])
api_router.include_router(trasmission_router,prefix="/Trasmission",tags=["Trasmissions"])
api_router.include_router(user_router,prefix="/Auth",tags=["Users"])

app.include_router(api_router)

if __name__ =="__main__":
    import uvicorn
uvicorn.run("main:app", host="127.0.0.2", port="8000", log_level="info", reload="True")