from fastapi import FastAPI
from .routes import router
from .database import init_db

app = FastAPI(
    title="LogflareX Backend",
    description="API for ingesting and viewing logs",
    version="0.1"
)

# Initialize database tables at startup
@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "LogflareX API is running"}