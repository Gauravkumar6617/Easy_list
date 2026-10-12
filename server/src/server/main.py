from fastapi import FastAPI
from src.server.db.database import HealthCheck
app=FastAPI(
    docs_url="/docs"
)

@app.get("/")
def healthCheck():
    db_status = HealthCheck()
    if db_status:
        return {"status": "healthy"}
    else:
        return {"status": "unhealthy"}