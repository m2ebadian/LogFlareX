from fastapi import FastAPI
from .database import init_db
from .routes import logs_routes, alerts_routes
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter
from .metrics import error_log_counter

app = FastAPI(
    title="LogflareX Backend",
    description="API for ingesting and viewing logs",
    version="0.1"
)


Instrumentator().instrument(app).expose(app)



@app.on_event("startup")
def on_startup():
    """
    Initialize the database tables when the application starts.
    Ensures all required tables exist before handling requests.
    """
    init_db()

app.include_router(logs_routes.router)
app.include_router(alerts_routes.router)

@app.get("/health")
async def health_check():
    """
    Health check endpoint for uptime monitoring.

    Returns:
        dict: {"status": "ok"} if the service is running.
    """
    return {"status": "ok"}

@app.get("/")
async def root():
    """
    Root endpoint to confirm the API is running.

    Returns:
        dict: {"message": "LogflareX API is running"}
    """

    return {"message": "LogflareX API is running"}