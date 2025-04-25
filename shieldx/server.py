from fastapi import FastAPI
import shieldx.controllers as Controllers
from shieldx.db import connect_to_mongo,close_mongo_connection, get_database
import uvicorn
import asyncio
from contextlib import asynccontextmanager
from shieldx.db.indexes import create_indexes
from shieldx.log import Log
import logging
# import LogRecord,INFO,ERROR,DEBUG,WARNING
import os
import time as T

SHIELDX_DEBUG = bool(int(os.environ.get("SHIELDX_DEBUG","1")))
SHIELDX_TITLE = os.environ.get("SHIELDX_TITLE","ShieldX API")
SHIELDX_API_PREFIX = os.environ.get("SHIELDX_API_PREFIX","/api/v1")
SHIELDX_HOST = os.environ.get("SHIELDX_HOST","0.0.0.0")
SHIELDX_PORT = int(os.environ.get("SHIELDX_PORT","20000"))
SHIELDX_MONGODB_MAX_RETRIES = int(os.environ.get("SHIELDX_MONGODB_MAX_RETRIES","5"))

def console_handler_filter(lr:logging.LogRecord):
    if SHIELDX_DEBUG:
        return SHIELDX_DEBUG
    
    return lr.levelno == logging.INFO or lr.levelno == logging.ERROR or lr.levelno == logging.WARNING
        

L = Log(
    name="shieldx-server",
    console_handler_filter= console_handler_filter
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    t1 = T.time()
    L.debug({
        "event":"CONNECTING.DB",
    })
    await connect_to_mongo()
        
    # Esperar hasta que la base de datos esté disponible
    for attempt in range(SHIELDX_MONGODB_MAX_RETRIES):  # Intentos máximos
        try:
            db = get_database()
            if db is not None:
                await create_indexes()
                L.info({
                    "event":"CONNECT.DB",
                    "attempt":attempt,
                    "time":T.time() - t1
                })
                break  # Salir del bucle si la base de datos está lista
            L.error({
                "event":"CONNECTING.MONGODB.FAILED",
                "attempts":attempt+1,
                "left_attempts": SHIELDX_MONGODB_MAX_RETRIES - attempt
            })
            
        except RuntimeError:
            L.debug({
                "event":"CONNECTING.DB.WAITING",
            })
            await asyncio.sleep(1)  # Esperar un segundo antes de intentar nuevamente
    
    yield 
    await close_mongo_connection()
    L.debug({
        "event":"CLOSE.MONGODB.CONNECTION",
        "time":T.time() - t1 
    })


app = FastAPI(
    title=SHIELDX_TITLE,
    lifespan=lifespan, 
    description="API para registrar y consultar eventos generados por microservicios.",
    contact={
        "name": "Equipo ShieldX",
        "email": "soporte@shieldx.io",
    })


# Include API routes from the service controller under /api/v1
# Rutas para la gestión de eventos generados por servicios
app.include_router(Controllers.events_router, prefix=SHIELDX_API_PREFIX,tags=["Eventos"],)
# Rutas para la gestión de triggers del sistema
app.include_router(Controllers.trigger_router, prefix=SHIELDX_API_PREFIX, tags=["Triggers"])
# Rutas para la gestión de tipos de eventos
app.include_router(Controllers.event_types_router, prefix=SHIELDX_API_PREFIX, tags=["Tipos de Evento"])
# Rutas para administrar la relación EventType <-> Trigger
app.include_router(Controllers.events_triggers_router, prefix=SHIELDX_API_PREFIX, tags=["Event-Triggers"])
# Rutas para manejar la relación jerárquica entre triggers (parent-child)
app.include_router(Controllers.triggers_triggers_router, prefix=SHIELDX_API_PREFIX, tags=["Triggers-Triggers"])
# Rutas para administrar la relación Trigger <-> Rule
app.include_router(Controllers.rules_trigger_router, prefix=SHIELDX_API_PREFIX, tags=["Trigger - Rule"])
# Rutas para CRUD de reglas
app.include_router(Controllers.rules_router, prefix=SHIELDX_API_PREFIX,  tags=["Rules"])


if __name__ == "__main__":
    uvicorn.run(app, host=SHIELDX_HOST, port=SHIELDX_PORT)
