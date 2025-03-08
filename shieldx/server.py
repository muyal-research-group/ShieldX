from fastapi import FastAPI
from shieldx.controllers import events_router
from shieldx.db import connect_to_mongo,close_mongo_connection
import uvicorn
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield 
    await close_mongo_connection()
app = FastAPI(title="CryptoMesh API",lifespan=lifespan)

# Include API routes from the service controller under /api/v1
app.include_router(events_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=20000)
