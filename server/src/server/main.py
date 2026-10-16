import logging
from fastapi import FastAPI, Response, status
from server.core.config import settings
from server.db.database import Base, check_db , engine
from server.api.v1.users import router as user_router

logging.basicConfig(level=logging.INFO)


Base.metadata.create_all(bind=engine)  # Create tables if they don't exist
# openapi_url=None also turns off /docs and /redoc.
app = FastAPI(openapi_url=None if settings.ENV == "prod" else "/openapi.json")


app.include_router(user_router, prefix="/api/v1", tags=["users"])

@app.get("/health")
def health(response: Response):
    if not check_db():
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unhealthy"}
    return {"status": "healthy"}
